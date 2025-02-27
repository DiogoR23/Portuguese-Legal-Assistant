import logging
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.query import BatchStatement
import uuid


class CreateCassandraSession():
    """Class to create a session to the service where our Database is stored."""

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def __init__(self, username, password):
        """Initialize the connection to Cassandra."""
        auth_provider = PlainTextAuthProvider(username=username, password=password)
        self.cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider,
                          load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='datacenter1'),
                          protocol_version=5)

        self.session = self.cluster.connect()

        self._create_keyspaces_and_tables()


    def _create_keyspaces_and_tables(self):
        """Create the keyspaces and tables if they don't exist."""
        try:
            # Create Keyspace
            self.session.execute("""
            CREATE KEYSPACE IF NOT EXISTS cassandra
            WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 }
            """)

            # Create Tables
            self.session.execute("""
            CREATE TABLE IF NOT EXISTS cassandra.articles ( 
                id_articles UUID PRIMARY KEY,
                url TEXT,
                title TEXT,
                content TEXT
            )
            """)

            self.session.execute("""
            CREATE TABLE IF NOT EXISTS cassandra.ai_answers (
                id_answers UUID PRIMARY KEY,
                content_answers TEXT
            )
            """)

            self.session.execute("""
            CREATE TABLE IF NOT EXISTS cassandra.user_questions (
                id_question UUID PRIMARY KEY,
                content_question TEXT
            )
            """)

            self.session.execute("""
            CREATE TABLE IF NOT EXISTS cassandra.users (
                id_user UUID PRIMARY KEY,
                name TEXT,
                email TEXT,
                password TEXT
            )
            """)

            self.session.execute("""
            CREATE TABLE IF NOT EXISTS cassandra.conversations (
                id_conversation UUID,
                id_user UUID,
                id_question UUID,
                id_answer UUID,
                date TIMESTAMP,
                PRIMARY KEY ((id_user), id_conversation, date)
            ) WITH CLUSTERING ORDER BY (id_conversation ASC, date DESC);
""")

        except Exception as e:
            logging.error(f"Error creating keyspaces and tables: {e}")
    
    def save_data(self, data):
        """Save articles to the database."""
        try:
            for item in data:
                self.session.execute("""
                INSERT INTO cassandra.articles (id_articles, url, title, content)
                VALUES (uuid(), %s, %s, %s)
                """, (item['url'], item['title'], item['content']))
        except Exception as e:
            logging.error(f"Error saving data to cassandra: {e}")


    def clear_table(self):
        """Clear the data from the given table."""
        try:
            self.session.execute(f"TRUNCATE cassandra.articles")
        
        except Exception as e:
            logging.error(f"Error clearing data from cassandra: {e}")


    def list_keyspaces(self):
        """List all the keyspaces in the database."""
        try:
            keyspaces = self.session.execute("SELECT keyspace_name FROM system_schema.keyspaces;")
            for keyspace in keyspaces:
                logging.info(keyspace.keyspace_name)

        except Exception as e:
            logging.error(f"Error listing keyspaces: {e}")


    def list_tables(self):
        """List all tables in the given keyspace."""
        try:
            tables = self.session.execute(f"SELECT table_name FROM system_schema.tables WHERE keyspace_name = 'cassandra'")
            for table in tables:
                logging.info({table.table_name})
        
        except Exception as e:
            logging.error(f"Error listing tables: {e}")


    def view_table_data(self, table, limit=10):
        """View the data in the given table."""
        try:
            data = self.session.execute(f"SELECT * FROM cassandra.{table} LIMIT {limit};")
            for row in data:
                logging.info(row)

        except Exception as e:
            logging.error(f"Error viewing table data: {e}")


    def load_data_chat_format(self, articles):
        """Format article data for chat display"""
        data = ""

        for article in articles:
            data += str(f"ID: {article['id_articles']}\nURL: {article['url']}\nTitle: {article['title']}\nContent: {article['content']}\n\n")

        return data


    def drop_table(self, table_name):
        """Remove a specific Cassandra Table."""
        if self.session is None:
            logging.error("No active session. Please check the connection.")
            return
        
        query = f"DROP TABLE cassandra.{table_name}"

        self.session.execute(query)


    def truncate_table(self, table_name):
        """Clear the information of a specific Cassandra table."""
        if self.session is None:
            logging.error("No active session. Please check the connection.")
            return
        
        self.session.execute(f"TRUNCATE cassandra.{table_name}")


    def execute(self, query):
        return self.session.execute(query)


    def keyspace_remove(self):
        """Removes a keyspace."""
        if self.session is None:
            logging.error("No active session. Please check the connection.")
            return

        try:
            self.session.execute(f"DROP KEYSPACE cassandra")
        except Exception as e:
            logging.error(f"Error removing keyspace: {e}")


    def check_table(self, table):
        """Show the columns for the corresponding keyspace table."""
        if self.session is None:
            logging.error("No active session. Please check the connection.")
            return

        try:
            self.session.execute(f"DESCRIBE TABLE cassandra.{table}")

        except Exception as e:
            logging.error(f"Error describing table: {e}")


    def check_vector_store_data(self):
        """Check the data in the vector store."""
        try:
            query = "SELECT * FROM cassandra.vector_store;"
            rows = self.session.execute(query)

            for row in rows:
                logging.info(row)

        except Exception as e:
            logging.error(f"Error checking vector store data: {e}")


    def close(self):
        """Close the connection to Cassandra."""
        self.cluster.shutdown()
        logging.info("Connection to Cassandra closed.")
