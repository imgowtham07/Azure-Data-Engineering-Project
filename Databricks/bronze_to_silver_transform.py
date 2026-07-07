from pyspark.sql.functions import from_utc_timestamp, date_format
from pyspark.sql.types import TimestampType

table_names = []

for i in dbutils.fs.ls("abfss://bronze@datalakegowtham01.dfs.core.windows.net/SalesLT/"):
    table_names.append(i.name.split('/')[0])

for i in table_names:

    path = "abfss://bronze@datalakegowtham01.dfs.core.windows.net/SalesLT/" + i + "/" + i + ".parquet"

    df = spark.read.format("parquet").load(path)

    for col in df.columns:
        if "Date" in col or "date" in col:
            df = df.withColumn(
                col,
                date_format(
                    from_utc_timestamp(df[col].cast(TimestampType()), "UTC"),
                    "yyyy-MM-dd"
                )
            )

    output_path = "abfss://silver@datalakegowtham01.dfs.core.windows.net/SalesLT/" + i + "/"

    df.write.format("delta").mode("overwrite").save(output_path)

print("All tables transformed successfully")