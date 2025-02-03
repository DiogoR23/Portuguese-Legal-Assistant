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