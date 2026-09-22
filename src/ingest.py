import logging
from pathlib import Path

import duckdb


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
WAREHOUSE_DIR = BASE_DIR / "data" / "warehouse"

DATABASE_PATH = WAREHOUSE_DIR / "warehouse.duckdb"
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "ingestion.log"


def configure_logging():
    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(),
        ],
    )


logger = logging.getLogger(__name__)


def create_directories():
    WAREHOUSE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def ingest_customers(connection):
    logger.info("Ingesting customers.csv")

    connection.execute(
        f"""
        CREATE OR REPLACE TABLE raw_customers AS
        SELECT
            CAST(customer_id AS VARCHAR) AS customer_id,
            CAST(country AS VARCHAR) AS country,
            CAST(signup_date AS DATE) AS signup_date,
            CAST(device_type AS VARCHAR) AS device_type
        FROM read_csv_auto(
            '{RAW_DIR / "customers.csv"}'
        )
        """
    )


def ingest_products(connection):
    logger.info("Ingesting products.csv")

    connection.execute(
        f"""
        CREATE OR REPLACE TABLE raw_products AS
        SELECT
            CAST(product_id AS VARCHAR) AS product_id,
            CAST(product_name AS VARCHAR) AS product_name,
            CAST(category AS VARCHAR) AS category,
            CAST(list_price AS DECIMAL(10, 2)) AS list_price
        FROM read_csv_auto(
            '{RAW_DIR / "products.csv"}'
        )
        """
    )


def ingest_events(connection):
    logger.info("Ingesting events.json")

    connection.execute(
        f"""
        CREATE OR REPLACE TABLE raw_events AS
        SELECT
            CAST(event_id AS VARCHAR) AS event_id,
            CAST(customer_id AS VARCHAR) AS customer_id,
            CAST(event_type AS VARCHAR) AS event_type,
            CAST(event_timestamp AS TIMESTAMP) AS event_timestamp,
            CAST(platform AS VARCHAR) AS platform,
            CAST(session_id AS VARCHAR) AS session_id
        FROM read_json_auto(
            '{RAW_DIR / "events.json"}'
        )
        """
    )


def ingest_orders(connection):
    logger.info("Ingesting orders.csv")

    connection.execute(
        f"""
        CREATE OR REPLACE TABLE raw_orders AS
        SELECT
            CAST(order_id AS VARCHAR) AS order_id,
            CAST(customer_id AS VARCHAR) AS customer_id,
            CAST(order_timestamp AS TIMESTAMP) AS order_timestamp,
            CAST(product_id AS VARCHAR) AS product_id,
            CAST(quantity AS INTEGER) AS quantity,
            CAST(unit_price AS DECIMAL(10, 2)) AS unit_price,
            CAST(currency AS VARCHAR) AS currency
        FROM read_csv_auto(
            '{RAW_DIR / "orders.csv"}'
        )
        """
    )


def report_row_counts(connection):
    tables = [
        "raw_customers",
        "raw_products",
        "raw_events",
        "raw_orders",
    ]

    logger.info("Warehouse row counts:")

    for table in tables:
        count = connection.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        logger.info(
            "  %s: %s rows",
            table,
            count,
        )


def main():
    configure_logging()

    logger.info("Starting ingestion pipeline")

    create_directories()

    connection = duckdb.connect(
        str(DATABASE_PATH)
    )

    try:
        ingest_customers(connection)
        ingest_products(connection)
        ingest_events(connection)
        ingest_orders(connection)

        report_row_counts(connection)

        logger.info(
            "Ingestion completed successfully"
        )

    except Exception:
        logger.exception(
            "Ingestion pipeline failed"
        )
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
