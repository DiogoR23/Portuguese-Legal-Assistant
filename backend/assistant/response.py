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
from langchain.prompts import PromptTemplate

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
    try:
        # Initialize Intent Detector
        detecor = IntentDetector()
        intent = detecor.detect(user_input)

        # Îf it is a simple greeting, do not call the RAG service
        if intent == "greeting":
            return "Olá! Em que posso ajudá-lo hoje? Sinta-se à vontade para colocar a sua dúvida ou questão jurídica."

        # If the input is unknown
        if intent == "unknown":
            return "Sou um assistente jurídico especializado na legislação Portuguesa. Por favor, coloque a sua dúvida jurídica para que eu possa ajudá-lo."

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

        input_variables = ["input", "context", "agent_scratchpad"]

        template = """
            Você é um Assistente Jurídico especializado em leis portuguesas.

            **Função Principal:**
            - Responder de forma clara, precisa e objetiva, com base na legislação portuguesa e no contexto fornecido.
            - Identificar o artigo de lei mais relevante sempre que possível.

            **Comportamento Esperado:**
            - Cite o artigo de lei relevante, se disponível, no formato: "Artigo [número]º do [Código] - '[Título do artigo]'".
            - Nunca invente informações; se o contexto não tiver dados suficientes, informe educadamente o utilizador.

            **Nota obrigatória ao final da resposta:**
            > "Esta resposta foi gerada por um Assistente de Inteligência Artificial. Para aconselhamento jurídico definitivo, recomenda-se a consulta a um advogado ou profissional especializado na área."

            **Contexto:**
            {context}

            **Pergunta do Utilizador:**
            {input}

            **Instruções de Resposta:**
            - Contextualize a resposta com base nos dados fornecidos.
            - Seja claro, objetivo e cordial.
            - Inclua sempre a nota final de responsabilidade.

            {agent_scratchpad}
    """

        prompt_template = PromptTemplate(
            input_variables=input_variables,
            template=template
        )

        llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            base_url=BASE_URL,
            model="RichardErkhov/mistralai_-_Mistral-7B-Instruct-v0.3-gguf",
            temperature=0.0,
            frequency_penalty=0.2,
            presence_penalty=0.0
        )

        agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt_template)
        agent_executor = AgentExecutor(agent=agent, tools=tools)

        retrieved_docs = tool.invoke(user_input)
        context = "".join([doc for doc in retrieved_docs])

        result = agent_executor.invoke({"input": user_input,"context": context, "agent_scratchpad": ""})
        response = result["output"]

        return response
    
    except Exception as e:
        logging.error(f"Error initializing the system: {e}")
        return f"Error: {e}", []
    
    finally:
        if session:
            session.shutdown()