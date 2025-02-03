from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os

def connect_to_cassandra():
    """Establishes a connection to Cassandra and returns the session."""
    auth_provider = PlainTextAuthProvider(username=os.getenv("CASSANDRA_USERNAME"), password=os.getenv("CASSANDRA_PASSWORD"))
    cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)
    session = cluster.connect()

    print("Successfully connected to Cassandra.")

    return session


def view_data(session, table):
    """Views data from a specific table and keyspace."""
    if session is None:
        print("No active session. Please check the connection.")
        return

    query = f"SELECT * FROM cassandra.{table} LIMIT 10;"
    rows = session.execute(query)
    print(f"Data from table '{table}':")

    for row in rows:
        print(row)


def drop_table(session, table_name):
    session.execute(f"DROP TABLE IF EXISTS cassandra.{table_name}")


def clear_table(session, table_name):
    """Clear the information of a specific Cassandra table."""
    try:
        session.execute(f"TRUNCATE cassandra.{table_name}")

    except Exception as e:
        print(f"Error cleaning table: {e}")


def keyspace_remove(session, keyspace):
    session.execute(f"DROP KEYSPACE {keyspace}")


def check_table(session, keyspace, table):
    """Show the columns for the corresponding keyspace table."""
    
    session.execute(f"DESCRIBE TABLE {keyspace}.{table}")


