import logging
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import DCAwareRoundRobinPolicy

class CassandraSession():
    """Class to get the access to the service where our Database is stored."""

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def __init__(self, username, password, local_dc):
        """Initialize the connection to Cassandra."""
        self.auth_provider = PlainTextAuthProvider(username=username, password=password)

        self.cluster = Cluster(['172.18.0.2'], auth_provider=self.auth_provider,
                               load_balancing_policy=DCAwareRoundRobinPolicy(local_dc=local_dc),
                               protocol_version=5)
        self.session = self.cluster.connect()

        self._create_keyspaces_and_tables()
    

    def _create_keyspaces_and_tables(self):
        """Create the keyspaces and tables if they don't exist."""
        try:
            self.session.execute("""
            CREATE KEYSPACE IF NOT EXISTS cassandra
            WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 }
            """)

            self.session.set_keyspace('cassandra')

            self.session.execute("""
            CREATE TABLE IF NOT EXISTS cassandra.articles (
                id_articles UUID PRIMARY KEY,
                url TEXT,
                title TEXT,
                content TEXT
            )
            """)

            self.session.execute("""
            CREATE TABLE IF NOT EXISTS cassandra.user_feedback (
                id_feedback UUID PRIMARY KEY,
                content_question TEXT,
                content_feedback TEXT
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
        
        except Exception as e:
            logging.error(f"Error creating keyspaces and tables: {e}")
    
    def save_data(self, data):
        """Save articles to the database."""
        try:
            for item in data:
                self.session.execute("""
                INSERT INTO cassandra.articles (id_articles, url, title, content)
                VALUES (uuid(), %s, %s, %s)
                """, (item['url'], item['ttitle'], item['content']))
        
        except Exception as e:
            logging.error(f"Error saving data to cassandra: {e}")
    

    def clear_data(self, table):
        """Clear the data from the given table."""
        try:
            self.session.execute(f"TRUNCATE cassandra.{table}")
        
        except Exception as e:
            logging.error(f"Error clearing data from cassandra: {e}")
    

    def list_keyspaces(self):
        """List all the keyspaces in the database."""
        try:
            keyspaces = self.session.execute("SELECT keyspace_name FROM system_schema.keyspaces;")
            return [keyspace.keyspace_name for keyspace in keyspaces]

        except Exception as e:
            logging.error(f"Error listing keyspaces: {e}")
            return []
    

    def list_tables(self, keyspace):
        """List all tables in the given keyspace."""
        try:
            tables = self.session.execute(f"SELECT table_name FROM system_schema.tables WHERE keyspace_name = '{keyspace}'")
            return [table.table_name for table in tables]
        
        except Exception as e:
            logging.error(f"Error listing tables: {e}")
            return []
    
    def view_table_data(self, table, keyspace, limit=10):
        """View the data in the given table."""
        try:
            data = self.session.execute(f"SELECT * FROM {keyspace}.{table} LIMIT {limit};")
            return [row for row in data]
        
        except Exception as e:
            logging.error(f"Error viewing table data: {e}")
            return []
    
    def close(self):
        """Close the connection to Cassandra."""
        self.cluster.shutdown()
        logging.info("Connection to Cassandra closed.")
