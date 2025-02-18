import os
from dotenv import load_dotenv
import logging
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Cassandra
from langchain_community.utilities.cassandra import SetupMode


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL")
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE")
USERNAME = os.getenv("CASSANDRA_USERNAME")
PASSWORD = os.getenv("CASSANDRA_PASSWORD")


def connect_vstore(session):
    """
    Crete a Cassandra vector Store from a session.
    """
    logging.info("Creating OpenAI Embeddings...")
    embeddings = OpenAIEmbeddings(
        api_key=OPENAI_API_KEY,
        base_url=BASE_URL,
        model="nomic-ai/nomic-embed-text-v1.5-GGUF",
        check_embedding_ctx_length=False,
        dimensions=1024
    )

    logging.info("Creating Cassandra vector Store...")
    vstore = Cassandra(
        session=session,
        table_name="vector_store",
        embedding=embeddings,
        keyspace=CASSANDRA_KEYSPACE,
        setup_mode=SetupMode.SYNC
    )

    logging.info("Cassandra vector store created successfully.")

    return vstore