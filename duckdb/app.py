import duckdb

# Initialize DuckDB connection
con = duckdb.connect()

# Install the httpfs extension if not already installed
con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")

# Set the S3 region to ap-southeast-2
con.execute("SET s3_region='ap-southeast-2';")

# Read the data, specifying that it is Hive partitioned on date
query = f"""
    SELECT * FROM read_json('s3://garmin-connection-aws-cron-s3bucket-ucg6p4b0lajd/stress/*/*/*/*.json', hive_partitioning = true)
    WHERE year = 2024 AND month = 09 AND day = 30;
"""

# Execute the query and fetch the result into a DataFrame
df = con.execute(query).fetchdf()

# Display the DataFrame (optional)
print(df)
