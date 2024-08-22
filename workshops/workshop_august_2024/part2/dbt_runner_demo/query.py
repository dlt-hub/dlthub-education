import sys
import duckdb

conn = duckdb.connect("github_issues_merge.duckdb")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing query")
    else:
        response = conn.sql(" ".join(sys.argv[1:]))
        print(response)
        print(response.columns)

    conn.close()
