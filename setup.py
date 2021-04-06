import sqlite3
import os
from sqlite3 import Error
from settings import PH_FOLDER, CAT1, CAT2, CAT3, CAT4, DATABASE


def execute_query(conn, query, many=False):
    try:
        cur = conn.cursor()
        cur.execute(query)
    except Error as e:
        print(e)
    else:
        conn.commit()


def execute_many_query(conn, query, values):
    try:
        cur = conn.cursor()
        cur.executemany(query, values)
    except Error as e:
        print(e)
    else:
        conn.commit()


def get_category_and_filename_from_folders():
    if os.path.exists(PH_FOLDER):
        for _, dirname, filenames in os.walk(PH_FOLDER):
            if _.startswith(f"{PH_FOLDER}/"):
                category = _.lstrip(f"{PH_FOLDER}/")
                for filename in filenames:
                    print(category, filename)
                    yield category, filename


def setup_database(conn):
    print("DROP TABLE")
    execute_query(conn, """drop table photos""")
    print("CREATE TABLE")
    execute_query(conn, """create table photos(filename text, category text)""")

    print("LOAD PICTURES")
    values = get_category_and_filename_from_folders()
    execute_many_query(conn, "INSERT INTO photos VALUES (?,?)", values)


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    else:
        setup_database(conn)
    finally:
        if conn:
            conn.close()


def setup_folders():
    if not os.path.exists(PH_FOLDER):
        os.mkdir(PH_FOLDER)
    if not os.path.exists(os.path.join(PH_FOLDER, CAT1)):
        os.mkdir(f"{PH_FOLDER}/{CAT1}")
    if not os.path.exists(os.path.join(PH_FOLDER, CAT2)):
        os.mkdir(f"{PH_FOLDER}/{CAT2}")
    if not os.path.exists(os.path.join(PH_FOLDER, CAT3)):
        os.mkdir(f"{PH_FOLDER}/{CAT3}")
    if not os.path.exists(os.path.join(PH_FOLDER, CAT4)):
        os.mkdir(f"{PH_FOLDER}/{CAT4}")


if __name__ == "__main__":
    setup_folders()
    create_connection(DATABASE)
