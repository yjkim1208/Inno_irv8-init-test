
import os
from dotenv import load_dotenv
import oracledb

load_dotenv()  # .env 파일에서 DB 정보 불러오기

def get_connection():
    return oracledb.connect(
        host=os.getenv("DB_HOST"),
        service_name=os.getenv("DB_SERVICE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", 1521)
    )

# def fetch_one_dict(db_name, query, params=None):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(query, params)
#     desc = [col[0] for col in cur.description]
#     row = cur.fetchone()
#     cur.close()
#     conn.close()
#     return dict(zip(desc, row)) if row else None

def fetch_one_dict(db_name, query, params=None):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(query, params or {})

        row = cur.fetchone()

        if row is None:
            return None

        columns = [
            column[0].lower()
            for column in cur.description
        ]

        return dict(zip(columns, row))

    finally:
        cur.close()
        conn.close()