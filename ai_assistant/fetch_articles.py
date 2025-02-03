from cassandra.query import BatchStatement
import logging
import os
import uuid


def sanitize_string(input_string):
    """Sanitizes the string by removing invalid Unicode characters."""
    return input_string.encode('utf-8', 'ignore').decode('utf-8')


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

                sanitized_answer = sanitize_string(answer)
                ai_query = """
                        INSERT INTO cassandra.ai_answers (id_answers, content_answers)
                        VALUES (%s, %s)
                        """

                ai_batch.add(ai_query, (id_answers, sanitized_answer))
        session.execute(ai_batch)

    except Exception as e:
        logging.debug(f"Saving answers error: {e}")

    # Saving User questions to cassandra's Database, answers's table
    user_batch = BatchStatement()
    try:
        for user_input in input_history:
            if user_input:
                id_question = uuid.uuid4()

                sanitized_question = sanitize_string(user_input)
                user_query = """
                        INSERT INTO cassandra.user_questions (id_question, content_question)
                        VALUES (%s, %s)
                        """

                user_batch.add(user_query, (id_question, sanitized_question))
        session.execute(user_batch)

    except Exception as e:
        logging.debug(f"Saving questions error: {e}")


def fetch_articles_from_cassandra(session):
    """Fetches articles from the specified keyspace."""
    keyspace = os.getenv("CASSANDRA_KEYSPACE")

    query = f"SELECT id_articles, url, title, content FROM {keyspace}.articles;"
    rows = session.execute(query)

    articles = [{"id_articles": str(row.id_articles), "url": row.url, "title": row.title, "content": row.content} for row in rows]

    return articles


def fetch_answers_from_cassandra(session):
    """Fetches answers from the specified keyspace."""
    keyspace = os.getenv("CASSANDRA_KEYSPACE")

    query = f"SELECT id_answers, content_answers FROM {keyspace}.ai_answers;"
    rows = session.execute(query)

    answers = [{"id_answer": str(row.id_answers), "content_answers": row.content_answers} for row in rows]

    return answers


def fetch_questions_from_cassandra(session):
    """Fetches questions from the specified keyspace."""
    keyspace = os.getenv("CASSANDRA_KEYSPACE")

    query = f"SELECT id_question, content_question FROM {keyspace}.ai_questions;"

    rows = session.execute(query)
    questions = [{"id_question": str(row.id_question), "content_question": row.content_question} for row in rows]

    return questions


def load_data_chat_format(articles):
    """Formats article data for chat display."""
    data = ""
    for article in articles:
        data += str(f"ID: {article['id_articles']}\nURL: {article['url']}\nTitle: {article['title']}\nContent: {article['content']}\n\n")

    return data