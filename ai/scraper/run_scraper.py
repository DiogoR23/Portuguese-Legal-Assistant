from .session import CreateCassandraSession 
from scraper.scraper import crawl_site
import logging
import os
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv('CASSANDRA_USERNAME')
PASSWORD = os.getenv('CASSANDRA_PASSWORD')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Main function to execute the crawling and data saving"""
    try:
        session = CreateCassandraSession(username=USERNAME, password=PASSWORD)

        session.clear_table()

        start_url = 'https://diariodarepublica.pt/dr/detalhe/diario-republica/142-2024-873180956'
        base_url = "https://diariodarepublica.pt"

        if session:
            crawl_site(start_url, base_url, session)

            session.list_keyspaces()

            session.list_tables(KEYSPACE)

            session.view_table_data('articles', KEYSPACE)

    except Exception as e:
        logging.error(f"Error executing the principal function (main): {e}")


if __name__ == '__main__':
    main()