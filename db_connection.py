# File: db_connection.py
import psycopg2
import pandas as pd

def connect_to_database():
    host = "10.0.1.235"
    port = 5432
    database = "argri_dw"
    user = "postgres"
    password = "postgres"

    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

    return conn

def query_data(conn, query):
    df = pd.read_sql(query, conn)
    return df

def close_connection(conn):
    conn.close()
