import psycopg2
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# main function to get data


def getData(url, post_code, table_name, values="Hr_ktu"):
    query = {
        "query": [
            {
                "code": "Postinumeroalue",
                "selection": {"filter": "item", "values": post_code},
            },
            {"code": "Tiedot", "selection": {"filter": "item", "values": [values]}},
        ],
        "response": {"format": "json-stat2"},
    }
    try:
        response = requests.post(url, json=query)
        content = response.json()
    except json.decoder.JSONDecodeError:
        print("there is an error with url")
    except requests.exceptions.ConnectionError:
        print("url connection error...please check the url address")
    except Exception as e:
        print("something else wrong with the code", type(e))
    else:
        print(f"Data fetched successfully for {table_name}")
        # income are stored in the value as key and amount as values in key-value pair of json response
        data = content["value"]
        print("connecting database...")
        try:
            conn = psycopg2.connect(
                database="codingpub",
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                host="127.0.0.1",
                port="5432",
            )
            cursor = conn.cursor()
        except psycopg2.OperationalError:
            print("connection error")
        except Exception as e:
            print(type(e))
        else:
            print("Database connected")

        try:

            cursor.execute(("DROP TABLE IF EXISTS {}").format(table_name))
            query = "CREATE TABLE {} (ID SERIAL PRIMARY KEY,POST_CODE CHAR(5),AVERAGE_INCOME INT)".format(
                table_name
            )
            cursor.execute(query)

        except psycopg2.errors.SyntaxError:
            print(" sql syntax error")
        except Exception as e:
            print(type(e))
        else:
            print(f"Table {table_name} created")

            try:
                # creating table and inserting values respectively
                sql = "INSERT INTO {} (POST_CODE,AVERAGE_INCOME) VALUES(%s,%s)".format(
                    table_name
                )

            except psycopg2.errors.SyntaxError:
                print(" sql syntax error")
            except Exception as e:
                print("something else error", e)
            else:
                # executing the sql query to insert income values for each post code
                try:
                    for i in range(len(post_code)):
                        cursor.execute(sql, (post_code[i], data[i]))
                    print("Data entered to the table")
                except psycopg2.errors.SyntaxError:
                    print("error inserting values...please check the insert statement")
                except Exception as e:
                    print("error", type(e))
                else:
                    conn.commit()

        finally:

            conn.close()
            print("connection closed")


years = [2017, 2018, 2019, 2020, 2021]
post_codes = ["00130", "02380", "16710", "41930", "54800"]
for year in years:
    page = f"paavo_3_hr_{year}"
    values = "Hr_ktu"
    if year > 2019:
        page = f"paavo_pxt_12f1"
        values = "hr_ktu"
    getData(
        f"https://pxnet2.stat.fi:443/PXWeb/api/v1/en/Postinumeroalueittainen_avoin_tieto/{year}/{page}.px",
        post_codes,
        f"TABLE_{year}",
        values,
    )
