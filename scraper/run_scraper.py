from scraper.cassandra_session import CassandraSession 
from scraper.scraper import crawl_site
import logging
import os
from dotenv import load_dotenv

load_dotenv()
username = os.getenv('CASSANDRA_USERNAME')
password = os.getenv('CASSANDRA_PASSWORD')
keyspace = os.getenv('CASSANDRA_KEYSPACE')
local_dc = os.getenv('CASSANDRA_LOCAL_DC')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Main function to execute the crawling and data saving"""
    try:
        session = CassandraSession(username=username, password=password, local_dc=local_dc)
        session.clear_data()

        start_url = 'https://diariodarepublica.pt/dr/detalhe/diario-republica/142-2024-873180956'
        base_url = "https://diariodarepublica.pt"

        if session:
            crawl_site(start_url, base_url, session)

            session.list_keyspaces()

            session.list_tables(keyspace)

            session.view_table_data(session, keyspace, 'articles')

    except Exception as e:
        logging.error(f"Error executing the principal function (main): {e}")


if __name__ == '__main__':
    main()