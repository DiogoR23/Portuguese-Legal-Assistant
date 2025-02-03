from scraper.storage import create_cassandra_session, clear_table, list_keyspaces, list_tables, view_table_data
from scraper.scraper import crawl_site
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Main function to execute the crawling and data saving"""
    try:
        session = create_cassandra_session()
        clear_table(session)

        start_url = 'https://diariodarepublica.pt/dr/detalhe/diario-republica/142-2024-873180956'
        base_url = "https://diariodarepublica.pt"

        if session:
            crawl_site(start_url, base_url, session)

            list_keyspaces(session)

            keyspace = 'cassandra'
            list_tables(session, keyspace)

            view_table_data(session, keyspace, 'articles')

    except Exception as e:
        logging.error(f"Error executing the principal function (main): {e}")


if __name__ == '__main__':
    main()