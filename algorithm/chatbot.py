from dotenv import load_dotenv
import os
from ai_assistant.connect_database import connect_to_cassandra
from ai_assistant.connect_database import save_answer_question
from ai_assistant.rag_pipeline import rag_tool
from langchain_community.vectorstores import Cassandra
from langchain_openai import OpenAIEmbeddings
import logging
from langchain_community.utilities.cassandra import SetupMode
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from ai_assistant.cassandra_vectorstore import connect_vstore

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


        name = 'law_search_tool'
        description = (
            """Search for information about Portuguese laws.
            For any questions about some law or some doubts the user has about Portugues rules, you must use this tool!"""
        )

        tool = rag_tool(
            session=session,
            name=name,
            description=description,
            keyspace=CASSANDRA_KEYSPACE,
            vstore=vstore
        )
        tools = [tool]

        prompt_template = PromptTemplate(
            input_variables=["input", "context", "agent_scratchpad"],
            template=("You are a legal assistant specializedin Portuguese laws. \n\n."
                      "The user asked the following questions: \n{input}\n\n"
                      "Here are some articles of law that may be helpful:\n{context}\n\n"
                      "Based on this information, provide an accurate and clear answer, citing the relevant articles."
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

            retrieved_docs = tool.invoke(user_input)

            context = "".join([doc for doc in retrieved_docs])

            result = agent_executor.invoke({"input": user_input, "context": context, "agent_scratchpad": ""})
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
