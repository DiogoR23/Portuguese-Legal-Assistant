"""
database.py

This module defines functions for interacting with a Cassandra database.
It includes functions to connect to the database, view data, drop tables, clear tables, remove keyspaces, check table structure, and save user input and AI responses to the database.

The functions are designed to be used in a legal assistant application, where user questions and AI answers are stored in a Cassandra database for further analysis and retrieval.

The functions are:
- connecto to cassandra: Establishes a connection to the Cassandra database.
- view_data: Views data from a specific table and keyspace.
- drop_table: Drops a table if it exists.
- clear_table: Clears the information of a specific Cassandra table.
- keyspace_remove: Removes a keyspace.
- check_table: Shows the columns for the corresponding keyspace table.
- save_answer_questions: Saves user input (questions) and AI responses to the corresponding keyspace table.
"""

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os
import logging
import uuid
from cassandra.query import BatchStatement


def connect_to_cassandra():
    """Establishes a connection to Cassandra and returns the session."""
    auth_provider = PlainTextAuthProvider(username=os.getenv("CASSANDRA_USERNAME"), password=os.getenv("CASSANDRA_PASSWORD"))
    cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)
    session = cluster.connect()

    logging.info("Successfully connected to Cassandra.")

    return session

def view_data(session, table):
    """Views data from a specific table and keyspace."""
    if session is None:
        logging.error("No active session. Please check the connection.")
        return

    query = "SELECT * FROM cassandra.%s LIMIT 10;" % table
    rows = session.execute(query)
    logging.info(f"Data from table '{table}':")
    for row in rows:
        logging.info(row)


def drop_table(session, table_name):
    """Drops a table if it exists."""
    if session is None:
        logging.error("No active session. Please check the connection.")
        return

    session.execute("DROP TABLE IF EXISTS cassandra.%s" % table_name)


def clear_table(session, table_name):
    """Clear the information of a specific Cassandra table."""
    if session is None:
        logging.error("No active session. Please check the connection.")
        return

    session.execute("TRUNCATE cassandra.%s" % table_name)


def keyspace_remove(session, keyspace):
    """Removes a keyspace."""
    if session is None:
        logging.error("No active session. Please check the connection.")
        return

    try:
        session.execute("DROP KEYSPACE %s" % keyspace)
    except Exception as e:
        logging.error(f"Error removing keyspace: {e}")

def check_table(session, keyspace, table):
    """Show the columns for the corresponding keyspace table."""
    if session is None:
        logging.error("No active session. Please check the connection.")
        return

    try:
        session.execute("DESCRIBE TABLE %s.%s" % (keyspace, table))
    except Exception as e:
        logging.error(f"Error describing table: {e}")

def save_answer_question(input_history : list[str], answers_history : list[str], session):
    """
    Saves user input (questions) and AI responses to the corresponding keyspace table.
    The input_history and answers_history, must be a list, so the function can iterable, and send the information to cassandra's database.

    @param input_history -> Must be a List of strings
    @param answers_history -> Must be a list of string
    @param session -> Must be a Cassandra Session

    Example:

    .. code-block:: python
        # Save AI responses and User input to a list first
        answers_history = []
        input_history = []

        while true:
            user_input = input("User -> ")

            # The rest of the code here

            # Get the AI responses
            response_content = completion.choices[0].message

            # Add data to the list
            answers_history.append(response_content)
            input_history.append(user_input)

        # Save the data using the function
        save_answer_question(
            input_history=input_history,
            answers_history=answers_history,
            session=session
        )
    """
    # Saving AI answers to cassandra's Database, question's table
    ai_batch = BatchStatement()
    try:
        for answer in answers_history:
            if answer:
                id_answers = uuid.uuid4()

                ai_query = """
                        INSERT INTO cassandra.ai_answers (id_answers, content_answers)
                        VALUES (%s, %s)
                        """

                ai_batch.add(ai_query, id_answers)
        session.execute(ai_batch)

    except Exception as e:
        logging.debug(f"Saving answers error: {e}")

    # Saving User questions to cassandra's Database, answers's table
    user_batch = BatchStatement()
    try:
        for user_input in input_history:
            if user_input:
                id_question = uuid.uuid4()

                user_query = """
                        INSERT INTO cassandra.user_questions (id_question, content_question)
                        VALUES (%s, %s)
                        """

                user_batch.add(user_query, id_question)
        session.execute(user_batch)

    except Exception as e:
        logging.debug(f"Saving questions error: {e}")