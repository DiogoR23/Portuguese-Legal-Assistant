from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os

def connect_to_cassandra():
    """Establishes a connection to Cassandra and returns the session."""
    try:
        auth_provider = PlainTextAuthProvider(username=os.getenv("CASSANDRA_USERNAME"), password=os.getenv("CASSANDRA_PASSWORD"))
        cluster = Cluster([os.getenv("CASSANDRA_HOST", '127.0.0.1')], auth_provider=auth_provider)
        session = cluster.connect()
        print("Successfully connected to Cassandra.")
        return cluster, session
    except Exception as e:
        print(f"Error connecting to Cassandra: {e}")
        return None, None

def view_data(session, table):
    """Views data from a specific table and keyspace."""
    if session is None:
        print("No active session. Please check the connection.")
        return

    try:
        query = "SELECT * FROM cassandra.%s LIMIT 10;" % table
        rows = session.execute(query)
        print(f"Data from table '{table}':")
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Error viewing data: {e}")

def drop_table(session, table_name):
    """Drops a table if it exists."""
    if session is None:
        print("No active session. Please check the connection.")
        return

    try:
        session.execute("DROP TABLE IF EXISTS cassandra.%s" % table_name)
    except Exception as e:
        print(f"Error dropping table: {e}")

def clear_table(session, table_name):
    """Clear the information of a specific Cassandra table."""
    if session is None:
        print("No active session. Please check the connection.")
        return

    try:
        session.execute("TRUNCATE cassandra.%s" % table_name)
    except Exception as e:
        print(f"Error cleaning table: {e}")

def keyspace_remove(session, keyspace):
    """Removes a keyspace."""
    if session is None:
        print("No active session. Please check the connection.")
        return

    try:
        session.execute("DROP KEYSPACE %s" % keyspace)
    except Exception as e:
        print(f"Error removing keyspace: {e}")

def check_table(session, keyspace, table):
    """Show the columns for the corresponding keyspace table."""
    if session is None:
        print("No active session. Please check the connection.")
        return

    try:
        session.execute("DESCRIBE TABLE %s.%s" % (keyspace, table))
    except Exception as e:
        print(f"Error describing table: {e}")
