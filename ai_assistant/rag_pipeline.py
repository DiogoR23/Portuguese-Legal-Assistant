from langchain.tools.retriever import create_retriever_tool
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
import logging
from cassandra.query import SimpleStatement


def retriever_law(session, keyspace):
    try:
        query = f"SELECT id_articles, url, title, content FROM {keyspace}.articles"
        data = session.execute(f"SELECT * FROM {keyspace}.articles")

        docs = [
            Document(
                page_content=entry['content'],
                metadata={'title': entry['title'], 'url': entry['url']}
            )
            for entry in data
        ]

        retriever_bm25 = BM25Retriever.from_documents(documents=docs)
        retriever_bm25.k = 10

        return retriever_bm25
    
    except Exception as e:
        logging.error(f"Error creating BM25Retriever: {e}")


def hybrid_retriever(vstore, name, description):
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