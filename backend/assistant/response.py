from database import connect_to_cassandra, save_answer_question
from cassandra_vectorstore import connect_vstore
from rag_pipeline import rag_tool

from langchain.agents import AgentExecutor, create_openai_tools_agent
from cassandra.cluster import Cluster
from langchain_community.vectorstores import Cassandra
from langchain_community.utilities.cassandra import SetupMode
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.tools.retriever import create_retriever_tool

from dotenv import load_dotenv
import logging
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL")
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE")

def get_ai_response(user_input):
    """Process user input and return an AI response."""
    try:
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
            You are a legal assistant specialized in finding and explaining laws precisely. 
            Whenever you provide an answer that refers to a specific law or article, **immediately cite the article code and title**, right after mentioning it, along with a brief explanation of what the article stipulates in relation to the situation described.
            You should base your answer only on the information below. If the information is not there, **do not make it up**, just say that you did not find enough data.
            Focus solely on providing the correct answer.
            Speak only in Portuguese.

            **Available Context**:
            {context}  # This context includes detailed legal references, including article codes and titles.

            **User Input**:
            {input}

            **Instructions for Responding**:
            - **Contextualize** the answer based on the information provided.
            - **Explain clearly and objectively**, especially when citing laws.
            - **When referring to laws or articles**, immediately cite the **article code** and **title**, for example:
                - "Artigo 213º do Código Civil - 'Divórcio e separação de bens'"
            - **If the answer is inconclusive or more data or documents are required, state that more context is needed.**
            - **If the cited article is not directly applicable, explain why it is not relevant.**

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
            temperature=0.8
        )

        agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt_template)
        agent_executor = AgentExecutor(agent=agent, tools=tools)

        retrieved_docs = tool.invoke(user_input)
        context = "".join([doc for doc in retrieved_docs])

        result = agent_executor.invoke({"input": user_input, "context": context, "agent_scratchpad": ""})
        response = result["output"]

        save_answer_question(session=session, input_history=[user_input], answers_history=[response])

        return response
    
    except Exception as e:
        logging.error(f"Error initializing the system: {e}")
    
    finally:
        if session:
            session.shutdown()