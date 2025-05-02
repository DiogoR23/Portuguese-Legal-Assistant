"""
rag_pipeline.py

This module defines the functions responsible for creating a RAG (Retrieval-Augmented Generation) pipeline
using a hybrid retriever. The pipeline combines a BM25 retriever with a vector store retriever to provide a more comprehensive retrieval mechanism.

The function include:
- bm25_Retriever: Creates a BM25 retriever from the data in the Cassandra database.
- hybrid_retriever: Combines the BM25 retriever and the vector store retriever into a hybrid retriever using EnsembleRetriever.
- rag_tool: Creates a retriever tool using the hybrid retriever and returns it for use in the RAG pipeline.
"""

from langchain.tools.retriever import create_retriever_tool
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
import logging


def bm25_Retriever(session, keyspace):
    try:
        query = f"SELECT id_articles, url, title, content FROM {keyspace}.articles"
        data = session.execute(query)

        docs = [
            Document(
                page_content=row.content,
                metadata={'title': row.title, 'url': row.url}
            )
            for row in data
        ]

        retriever_bm25 = BM25Retriever.from_documents(documents=docs)
        retriever_bm25.k = 30

        return retriever_bm25

    except Exception as e:
        logging.error(f"Error creating BM25Retriever: {e}")
        return None


def hybrid_retriever(session, vstore, keyspace):
    try:
        retriever_bm25 = bm25_Retriever(session=session, keyspace=keyspace)
        vstore_retriever = vstore.as_retriever(search_kwargs={"k": 20})

        hybrid_retriever = EnsembleRetriever(
            retrievers=[retriever_bm25, vstore_retriever],
            weights=[0.5, 0.5]
        )

        return hybrid_retriever
    
    except Exception as e:
        logging.error(f"Error creating Hybrid Retriever: {e}")
        return None


def rag_tool(session, name, keyspace, description, vstore):
    try:
        retriever = hybrid_retriever(session=session, vstore=vstore, keyspace=keyspace)

        if retriever is None:
            logging.error(f"Hybrid retriever could not be created")
            return None

        tool = create_retriever_tool(
            retriever=retriever,
            name=name,
            description=description
        )

        return tool
    
    except Exception as e:
        logging.info(f"Error creating retriever tool: {e}")
        return None