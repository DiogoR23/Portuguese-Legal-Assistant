from dotenv import load_dotenv
import os
from langchain.tools.retriever import create_retriever_tool
from .connect_database import connect_to_cassandra
from .connect_database import save_answer_question
from langchain_community.vectorstores import Cassandra
from langchain_openai import OpenAIEmbeddings
import logging
from langchain_community.utilities.cassandra import SetupMode
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from .cassandra_vectorstore import connect_vstore

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL")
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE")
USERNAME = os.getenv("CASSANDRA_USERNAME")
PASSWORD = os.getenv("CASSANDRA_PASSWORD")


def main():
# TODO: Setup Code
    ai_color = "\033[36m"
    reset_color = "\033[0m"

    ai_answer = []
    user_question = []

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
                      "Ensure your responses are precise and useful, and provide your answers in english in case the user talks in english or other language besides portuguese, or portuguese in case the user talks in portuguese.\n\n"
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

        while True:
            print(f"{ai_color}\n{'-'*15} Welcome, ask something to our newest PLaws.ai! Type 'q' to quit! {'-'*15}\n")
            user_input = input("-> ")
            print(f"\n{'-'*95}\n{reset_color}")

            if user_input == "q" or user_input == "quit":
                break

            result = agent_executor.invoke({"input": user_input, "agent_scratchpad": ""})
            response = result["output"]

            print(f"{ai_color}\n{'-'*30} Jarvis Response {'-'*30}\n")
            print(f"-> {response}")
            print(f"\n{'-'*75}\n{reset_color}")

            ai_answer.append(response)
            user_question.append(user_input)

    except Exception as e:
        logging.error(f"Error initializing the system: {e}")

    finally:
        if 'session' in locals() and session is not None:
            save_answer_question(session=session, input_history=user_question, answers_history=ai_answer)
            session.shutdown()

if __name__ == "__main__":
    main()
