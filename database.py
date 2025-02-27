import sqlite3
import pandas as pd


def create_database_from_csv(csv_file, db_name="data.db", table_name="DATA"):
    """
    Reads an uploaded CSV file into a pandas DataFrame and writes it to a SQLite database.
    Returns the database name, table name, and the list of columns.
    """
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(db_name)
    # Replace any existing table with the new data
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
    return db_name, table_name, list(df.columns)


def create_database_from_url(url, db_name="data.db", table_name="DATA"):
    """
    Reads a CSV file from a URL into a pandas DataFrame and writes it to a SQLite database.
    Returns the database name, table name, and the list of columns.
    """
    df = pd.read_csv(url)
    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
    return db_name, table_name, list(df.columns)
