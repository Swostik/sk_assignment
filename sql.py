import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(
        database="codingpub",
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host="127.0.0.1",
        port="5432",
    )
except Exception as e:
    print("error occured while connecting to database ", e)
else:
    try:
        cursor = conn.cursor()
        query = """SELECT query_2.post_code, query_2.income_difference FROM 
        (SELECT MAX((t21.average_income - t17.average_income)*100.0/ t17.average_income) income_difference
                FROM table_2021 t21
                INNER JOIN 
            table_2017 t17 ON t17.post_code = t21.post_code) query_1
        join (SELECT t21.post_code post_code, (t21.average_income - t17.average_income)*100.0/ t17.average_income income_difference
            FROM table_2021 t21
            INNER JOIN 
            table_2017 t17 ON t17.post_code = t21.post_code) query_2
            ON query_1.income_difference = query_2.income_difference"""
        cursor.execute(query)
        row = cursor.fetchall()

    except Exception as err:
        print("error occured during query ", err)
    else:
        for i, r in row:
            print(
                f"Biggest income difference is found in post code {i} with percentage difference of {r} "
            )
    finally:
        cursor.close()
finally:
    conn.close()
