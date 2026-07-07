# Get all tables from the Silver layer
table_names = []

for i in dbutils.fs.ls("abfss://silver@datalakegowtham01.dfs.core.windows.net/SalesLT/"):
    table_names.append(i.name.split('/')[0])

# Transform data from Silver to Gold layer
for name in table_names:

    # Read Delta table from Silver layer
    path = f"abfss://silver@datalakegowtham01.dfs.core.windows.net/SalesLT/{name}/"
    df = spark.read.format("delta").load(path)

    # Get all column names
    column_names = df.columns

    # Convert CamelCase column names to snake_case
    for old_col_name in column_names:
        new_col_name = "".join(
            [
                "_" + c if c.isupper() and not old_col_name[i - 1].isupper() else c
                for i, c in enumerate(old_col_name)
            ]
        ).lstrip("_")

        df = df.withColumnRenamed(old_col_name, new_col_name)

    # Write transformed data to Gold layer
    output_path = f"abfss://gold@datalakegowtham01.dfs.core.windows.net/SalesLT/{name}/"

    df.write.format("delta").mode("overwrite").save(output_path)

print("Silver to Gold transformation completed successfully.")