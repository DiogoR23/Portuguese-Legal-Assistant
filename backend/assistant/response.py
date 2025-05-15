"""
response.py

This module defines the function get_ai_response, responsible for processing user input
and generating a legal response using a RAG (Retrieval-Augmented Generation) architecture
specialized in Portuguese law.

The function handles:
- Connecting to Cassandra database and vector store.
- Building a LangChain agent with a retriever tool.
- Processing the user input and generating a structured, professional answer.
- Incorporating an intent detection layer to classify the user input before generating a response.

This function is used in the main application to handle user queries and provide legal information.
"""

from .database import connect_to_cassandra
from .cassandra_vectorstore import connect_vstore
from .rag_pipeline import rag_tool
from .intent_detector import IntentDetector

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

from dotenv import load_dotenv
import logging
import os


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL")
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE")


def get_ai_response(user_input: str):
    """
    Processes the user's input and returns an AI-generated response based on Portuguese law.

    Args:
        user_input (str): The input message from the user.

    Returns:
        str: The AI-generated response, or a greeting or error message depending on the intent detected.
    """

    session = None
    tool = None
    vstore = None
    agent_executor = None

    try:
        # Initialize Intent Detector
        detecor = IntentDetector()
        intent = detecor.detect(user_input)

        # Îf it is a simple greeting, do not call the RAG service
        if intent == "greeting":
            return str("Olá! Em que posso ajudá-lo hoje? Sinta-se à vontade para colocar a sua dúvida ou questão jurídica.")

        # If the input is unknown
        if intent == "unknown":
            return str("Sou um assistente jurídico especializado na legislação Portuguesa. Por favor, coloque a sua dúvida jurídica para que eu possa ajudá-lo.")

        # If the input is legal_query, than call the LLM and RAG to answer the question 
        session = connect_to_cassandra()

        vstore = connect_vstore(session=session)

        name = 'law_search'
        description = (
            """Search for information about Portuguese laws.
            For any questions about some law or some doubts the user has about Portuguese rules, you must use this tool!
            You must cite the article, with the article code and his title, every time your answer refers to a specific law or article."""
        )

        tool = rag_tool(
            session=session,
            name=name,
            description=description,
            keyspace=CASSANDRA_KEYSPACE,
            vstore=vstore
        )
        tools = [tool]

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "És um Assistente Jurídico especializado em leis Portuguesas. Só podes falar de assuntos relacionados com Portugal. "
                "No caso do utilizador querer saber assuntos de outro país, deves informar que não tens conhecimento, pois foste treinada exclusivamente com base na legislação portuguesa. "
                "Baseia-te preferencialmente no contexto fornecido. "
                "Sempre que possível, cita os artigos relevantes no formato: 'Artigo [n.º] do [Código] - [Título]'. "
                "Se não houver um artigo claro, responde com base na interpretação geral da legislação aplicável. "
                "Se não encontrares dados suficientes, oferece uma explicação geral baseada em conhecimento jurídico comum, e indica que o utilizador deve procurar aconselhamento profissional. "
                "Evita estruturas como múltipla escolha, 'Sim/Não', ou tokens técnicos como [INST]. "
                "Responde com clareza, em linguagem natural e acessível. "
                "No fim, adiciona esta nota OBRIGATÓRIA: "
                "> Esta resposta foi gerada por um Assistente de IA. Para aconselhamento jurídico definitivo, consulte alguém dentro dessa área."
            ),
            HumanMessagePromptTemplate.from_template(
                "Contexto:\n{context}\n\nPergunta do Utilizador:\n{input}\n\n{agent_scratchpad}"
            )
        ])

        llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            base_url=BASE_URL,
            model="TheBloke/zephyr-7B-beta-GGUF",
            temperature=0.2,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            max_tokens=2048
        )

        agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools)

        retrieved_docs = tool.invoke(user_input)
        context = "\n\n".join(
            doc.page_content.strip()[:1000]
            for doc in retrieved_docs
            if hasattr(doc, 'page_content') and doc.page_content
        )

        result = agent_executor.invoke({"input": user_input,"context": context, "agent_scratchpad": ""})
        response = result["output"]

        return response

    except Exception as e:
        logging.error(f"Error initializing the system: {e}")
        return f"Error: {e}"

    finally:
        if session:
            session.shutdown()