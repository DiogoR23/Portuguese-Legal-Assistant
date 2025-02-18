from langchain.tools.retriever import create_retriever_tool
from langchain_community.retrievers import BM25Retriever
import logging
from cassandra.query import SimpleStatement


# def retrive_laws(vstore, ):


def create_retriever_from_cassandra(vstore, name, description):
    """Create a Retriever from cassandra Vector Store."""
    try:
        retriever = vstore.as_retriever()

        retriever_tool = create_retriever_tool(
            retriever=retriever,
            name=name,
            description=description
        )

        return retriever_tool

    except Exception as e:
        logging.error(f"Error creating retriever: {e}")


def check_vector_store_data(session):
    query = SimpleStatement("SELECT * FROM cassandra.vector_store;")
    rows = session.execute(query)

    for row in rows:
        print(row)