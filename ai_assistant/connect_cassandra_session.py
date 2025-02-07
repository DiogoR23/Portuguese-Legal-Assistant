import logging
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
import uuid
from cassandra.query import BatchStatement

class ConnectCassandraSession():
    """Class to connect to the session for our DataBase, to access the data."""

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def __init__(self, username, password):
        self.auth_provider = PlainTextAuthProvider(username=username, password=password)
        self.cluster = Cluster(['127.0.0.1'], auth_provider=self.auth_provider)

        self.session = self.cluster.connect()
        logging.info("Successfully connected to Cassandra.")
    
    def view_data(self, table):
        """Views data from a specific table."""
        if self.session is None:
            logging.error("No active session. Please check the connection.")
            return

        query = f"SELECT * FROM cassandra.{table} LIMIT 10;"
        rows = self.session.execute(query)
        logging.info(f"Data from table '{table}':")
        for row in rows:
            logging.info(row)
    
    def drop_table(self, table_name):
        """Drops a table if it exists."""
        if self.session is None:
            logging.error("No active session. Please check the connection.")
            return

        self.session.execute(f"DROP TABLE IF EXISTS cassandra.{table_name}")
    
    def clear_table(self, table_name):
        """Clear the information of a specific Cassandra table."""
        if self.session is None:
            logging.error("No active session. Please check the connection.")
            return

        self.session.execute(f"TRUNCATE cassandra.{table_name}")
    
    def keyspace_remove(self, keyspace):
        """Removes a keyspace."""
        if self.session is None:
            logging.error("No active session. Please check the connection.")
            return

        try:
            self.session.execute(f"DROP KEYSPACE {keyspace}")
        except Exception as e:
            logging.error(f"Error removing keyspace: {e}")
    
    def check_vector_store(self):
        """Check the data in the vector store."""
        try:
            query = "SELECT * FROM cassandra.vector_store;"
            rows = self.session.execute(query)

            for row in rows:
                logging.info(row)
        
        except Exception as e:
            logging.error(f"Error checking vector store data: {e}")
    

    def save_answers_question(self, input_history, answers_history):
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
            for answers in answers_history:
                if answers:
                    id_answers = uuid.uuid4()

                    ai_query = """
                            INSERT INTO cassandra.ai_answers (id_answers, content_answers)
                            VALUES (%s, %s)
                            """

                    ai_batch.add(ai_query, (id_answers, answers))
            
            self.session.execute(ai_batch)
        
        except Exception as e:
            logging.error(f"Saving answers error: {e}")
    
        # Saving User questions to cassandra's Database, answers's table
        user_batch = BatchStatement()
        try:
            for questions in input_history:
                if questions:
                    id_question = uuid.uuid4()

                    user_query = """
                            INSERT INTO cassandra.user_questions (id_question, content_question)
                            VALUES (%s, %s)
                            """

                    user_batch.add(user_query, id_question)
            
            self.session.execute(user_batch)
        
        except Exception as e:
            logging.error(f"Saving questions error: {e}")

    
    def close(self):
        """Close the connection to Cassandra."""
        self.cluster.shutdown()
        logging.info("Connection to Cassandra closed.")