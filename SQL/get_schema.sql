-- Lists all tables available in the SalesLT schema.
-- Used to verify the AdventureWorksLT database before ingestion.

SELECT
    s.name AS SchemaName,
    t.name AS TableName
FROM sys.tables t
INNER JOIN sys.schemas s
    ON t.schema_id = s.schema_id
WHERE s.name = 'SalesLT';