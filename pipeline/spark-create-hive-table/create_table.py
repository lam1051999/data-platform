from pyspark.sql import SparkSession
import os

# Initialize Spark Session with Hive support
spark = SparkSession.builder \
    .appName("HiveCreateTableExample") \
    .config("hive.metastore.uris", "thrift://hive-metastore.data-platform.svc.cluster.local:9083") \
    .enableHiveSupport() \
    .getOrCreate()

# MinIO configuration
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID", "minio"))
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY", "minio123"))
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", os.getenv("ENDPOINT", "https://localhost:9000"))
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "true")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.attempts.maximum", "1")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.connection.establish.timeout", "5000")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.connection.timeout", "10000")

# Create a Hive table
table_name = "delta_table"  # Choose your table name
database_name = "default" # Choose your database name. Default is used if you don't specify one.

spark.sql("CREATE DATABASE IF NOT EXISTS default").show()

spark.sql(f"""
  CREATE TABLE IF NOT EXISTS {database_name}.{table_name} (country STRING, continent STRING) USING delta
""")

spark.sql(f"""
  INSERT INTO {database_name}.{table_name} VALUES
      ('china', 'asia'),
      ('argentina', 'south america')
""")

# Show all tables in the default database
spark.sql("SHOW TABLES").show()

# Show all tables in a specific database:
spark.sql(f"SHOW TABLES IN {database_name}").show()

# Show tables with a specific pattern (e.g., all tables starting with "my_"):
spark.sql("SHOW TABLES LIKE 'my_*'").show()

# Describe the table schema
spark.sql(f"DESCRIBE {database_name}.{table_name}").show()

# Query the data from the Hive table
spark.sql(f"SELECT * FROM {database_name}.{table_name}").show()

# Stop the Spark session
spark.stop()