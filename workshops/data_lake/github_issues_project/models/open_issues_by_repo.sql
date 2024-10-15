WITH parquet_data AS (
    SELECT *
    FROM read_parquet('/Users/alena/dlthub/dlthub-education/workshops/data_lake/data_lake/github_raw/issues/1728478654.322983.c4d10ce543.parquet')
    WHERE state = 'open'
)
SELECT
    user__login,
    COUNT(*) AS issue_count
FROM parquet_data
GROUP BY user__login;