from cassandra.cluster import Cluster
from dotenv import load_dotenv
import os
from langchain.tools.retriever import create_retriever_tool
from .database import connect_to_cassandra
from .cassandra_vectorstore import connect_vstore
from .database import save_answer_question
from langchain_community.vectorstores import Cassandra
from langchain_openai import OpenAIEmbeddings
import logging
from langchain_community.utilities.cassandra import SetupMode
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL")

def get_ai_response(user_input):
    """Process user input and return an AI response."""
    try:
        session = connect_to_cassandra()

        vstore = connect_vstore(session=session)
        retriever = vstore.as_retriever(search_kwargs={"k": 100})
        tool = create_retriever_tool(
            retriever=retriever,
            name="law_search_tool",
            description=("""Search for information about Portuguese laws.
                            For any questions about some law or some doubts the user has about Portugues rules, you must use this tool!"""
                        )
        )
        tools = [tool]

        prompt_template = PromptTemplate(
            input_variables=["input", "agent_scratchpad"],
            template=("You are an intelligent assistant specialized in Portuguese law."
                        "Your role is to provide accurate and detailed information about Portuguese laws using the provided database."
                        "When answering user queries, refer to specific laws and articles where applicable."
                        "Ensure your responses are precise and useful.\n\n"
                        "Query: {input}\n"
                        "{agent_scratchpad}")
        )

        llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            base_url=BASE_URL,
            model="LM Studio Community/Meta-Llama-3-8B-Instruct-GGUF",
            temperature=0.8
        )

        agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt_template)
        agent_executor = AgentExecutor(agent=agent, tools=tools)

        result = agent_executor.invoke({"input": user_input, "agent_scratchpad": ""})
        response = result["output"]

        save_answer_question(session=session, input_history=[user_input], answers_history=[response])

        return response
    
    except Exception as e:
        logging.error(f"Error initializing the system: {e}")
    
    finally:
        if session:
            session.shutdown()