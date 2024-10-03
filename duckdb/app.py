import duckdb
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

bucket_name = os.environ.get(
    "BUCKET_NAME", "garmin-connection-aws-cron-s3bucket-ucg6p4b0lajd"
)


def table_exists(con, table_name):
    result = con.sql("SELECT * FROM duckdb_tables;").df()
    return result["table_name"].str.contains(table_name).any()


def get_most_recent_date(con, table_name):
    if table_exists(con, table_name):
        logging.info(f"Fetching the most recent date from the '{table_name}' table...")
        query = f"""
            SELECT MAX(make_date(CAST(year AS BIGINT), CAST(month AS BIGINT), CAST(day AS BIGINT))) AS most_recent_date 
            FROM {table_name};
        """
        most_recent_date = con.execute(query).fetchone()[0]
        if most_recent_date is None:
            logging.info(
                f"No previous {table_name} data found. Setting date to '2023-01-01'."
            )
            return "2023-01-01"
        else:
            logging.info(f"Most recent {table_name} date: {most_recent_date}")
            return str(most_recent_date)
    else:
        logging.info(f"'{table_name}' table does not exist. Setting default date.")
        return "2023-01-01"


def load_new_data(con, table_name, recent_date, options):
    logging.info(f"Fetching new {table_name} data after {recent_date}...")
    options_list = [
        "hive_partitioning = true",
        "filename = true",
    ]
    if options.get("ignore_errors", False):
        options_list.append("ignore_errors = true")
    options_str = ",\n            ".join(options_list)
    query = f"""
        SELECT *
        FROM read_json_auto(
            's3://{bucket_name}/{table_name}/*/*/*/*.json', 
            {options_str}
        )
        WHERE make_date(CAST(year AS BIGINT), CAST(month AS BIGINT), CAST(day AS BIGINT)) > '{recent_date}';
    """
    logging.info(
        f"Inserting new {table_name} data into the DuckDB '{table_name}' table..."
    )
    if table_exists(con, table_name):
        con.execute(f"INSERT INTO {table_name} {query};")
    else:
        con.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS {query};")


con = duckdb.connect("garmin.duckdb")  # Saves to 'garmin.duckdb' file

con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")

con.execute("SET s3_region='ap-southeast-2';")


tables = {"stress": {"ignore_errors": False}, "sleep": {"ignore_errors": True}}


for table_name, options in tables.items():
    recent_date = get_most_recent_date(con, table_name)
    load_new_data(con, table_name, recent_date, options)


con.close()
