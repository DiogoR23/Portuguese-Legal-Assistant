class CassandraSession():
    """Class to get the access to the service where our Database is stored."""
    from cassandra.cluster import Cluster
    from cassandra.auth import PlainTextAuthProvider
    from cassandra.policies import DCAwareRoundRobinPolicy
    import logging

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


    def __init__(self, cluster, auth_provider):
        self.cluster = cluster
        self.auth_provider = auth_provider
        # Try to complete the code, so that those functions enter in this class
        # Use ChatGPT or DeepSeek or Copilot to complete this class


def create_cassandra_session():
    """Connect to Cassandra and create the keyspace and table if they don't exist."""
    try:
        auth_provider = PlainTextAuthProvider(username='cassandra_user', password='cassandra_password')
        cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider,
                          load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='datacenter1'),
                          protocol_version=5)
        session = cluster.connect()

        # Create keyspaces
        session.execute("""
        CREATE KEYSPACE IF NOT EXISTS cassandra
        WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
        """)

        # Create tables
        session.execute("""
        CREATE TABLE IF NOT EXISTS cassandra.articles (
            id_articles UUID PRIMARY KEY,
            url TEXT,
            title TEXT,
            content TEXT
        )
        """)

        session.execute("""
        CREATE TABLE IF NOT EXISTS cassandra.user_feedback (
            id_feedback UUID PRIMARY KEY,
            content_question TEXT,
            content_feedback TEXT
        )
        """)

        session.execute("""
        CREATE TABLE IF NOT EXISTS cassandra.ai_answers (
            id_answers UUID PRIMARY KEY,
            content_answers TEXT
        )
        """)

        session.execute("""
        CREATE TABLE IF NOT EXISTS cassandra.user_questions (
            id_question UUID PRIMARY KEY,
            content_question TEXT
        )
        """)

        return session
    
    except Exception as e:
        logging.error(f"Error connecting to cassandra: {e}")
        return None


def save_data_to_cassandra(session, data):
    """Save the extracted data to Cassandra."""
    try:
        for item in data:
            if item:
                session.execute("""
                INSERT INTO cassandra.articles (id_articles, url, title, content)
                VALUES (uuid(), %s, %s, %s)
                """, (item['url'], item['title'], item['content']))
    
    except Exception as e:
        logging.error(f"Error saving data in Cassandra: {e}")


def clear_table(session):
    """Clear the articles table in Cassandra."""
    try:
        session.execute("TRUNCATE cassandra.articles")

    except Exception as e:
        logging.error(f"Error cleaning table: {e}")


def list_keyspaces(session):
    """List all keyspaces in Cassandra."""
    try:
        keyspaces = session.execute("SELECT keyspace_name FROM system_schema.keyspaces;")
        logging.info("Keyspaces:")
        for keyspace in keyspaces:
            logging.info(keyspace.keyspace_name)

    except Exception as e:
        logging.error(f"Error listing keyspaces: {e}")


def list_tables(session, keyspace):
    """List all tables in specific keyspace."""
    try:
        tables = session.execute(f"SELECT table_name FROM system_schema.tables WHERE keyspace_name = '{keyspace}';")
        logging.info(f"Keyspace tables '{keyspace}':")
        for table in tables:
            logging.info(table.table_name)

    except Exception as e:
        logging.error(f"Error listing tables: {e}")


def view_table_data(session, keyspace, table):
    """View data from a specific table."""
    try:
        query = f"SELECT * FROM {keyspace}.{table} LIMIT 10;"
        rows = session.execute(query)
        logging.info(f"Table Data '{table}':")
        for row in rows:
            logging.info(row)

    except Exception as e:
        logging.error(f"Error visualizing data from table {table}: {e}")
