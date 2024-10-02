import duckdb

# Initialize DuckDB connection and create or open a DuckDB file
con = duckdb.connect('garmin.duckdb')  # Saves to 'garmin.duckdb' file

# Install the httpfs extension if not already installed
con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")

# Set the S3 region to ap-southeast-2
con.execute("SET s3_region='ap-southeast-2';")

# Read the data, specifying that it is Hive partitioned on date
stress_query = f"""
    SELECT * FROM read_json('s3://garmin-connection-aws-cron-s3bucket-ucg6p4b0lajd/stress/*/*/*/*.json', hive_partitioning = true);
"""
sleep_query = f"""
    SELECT * FROM read_json('s3://garmin-connection-aws-cron-s3bucket-ucg6p4b0lajd/sleep/*/*/*/*.json', hive_partitioning = true, union_by_name = true);
"""

# Execute the query and save the result directly into a DuckDB table
con.execute(f"CREATE TABLE IF NOT EXISTS stress AS {stress_query};")
con.execute(f"CREATE TABLE IF NOT EXISTS sleep AS {sleep_query};")

# Close the connection
con.close()
