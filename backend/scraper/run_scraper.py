from session import CreateCassandraSession 
from scraper import crawl_site
import logging
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
USERNAME = os.getenv('CASSANDRA_USERNAME')
PASSWORD = os.getenv('CASSANDRA_PASSWORD')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    """Main function to execute the crawling and data saving"""
    try:
        session = CreateCassandraSession(username=USERNAME, password=PASSWORD)

        session.clear_table()

        start_url = 'https://diariodarepublica.pt/dr/detalhe/diario-republica/142-2024-873180956'
        base_url = "https://diariodarepublica.pt"

        if session:
            await crawl_site(start_url, base_url, session)

        logging.info("--- KEYSPACES ---")
        session.list_keyspaces()

        logging.info("--- TABLES ---")
        session.list_tables()

        session.view_table_data('articles')

    except Exception as e:
        logging.error(f"Error executing the principal function (main): {e}")


if __name__ == '__main__':
    asyncio.run(main()) 
