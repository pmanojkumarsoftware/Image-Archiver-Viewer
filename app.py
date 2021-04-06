from flask import Flask
import sqlite3
from flask import g
from settings import DATABASE

app = Flask(__name__)

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def hello_world():
    cur = get_db().cursor()
    rows = list(cur.execute("SELECT * FROM photos ORDER BY category"))
    print(rows)
    return "Hello, World!"
