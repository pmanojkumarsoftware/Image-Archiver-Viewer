from flask import Flask, g, request, render_template, send_from_directory
import sqlite3
import os
from settings import DATABASE, CAT2, CATEGORIES, PH_FOLDER

app = Flask(__name__, static_url_path='')

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

@app.route('/photos/<path:path>')
def send_js(path):
    return send_from_directory('photos', path)


@app.route("/")
def hello_world():
    category = request.args.get("category", CAT2)
    rows = []
    if category in CATEGORIES:
        print ("CAT:", category)
        cur = get_db().cursor()
        for category, filename in cur.execute("SELECT * FROM photos where category=?", (category,)):
            full_path = os.path.join(PH_FOLDER, category, filename)
            rows.append(full_path)

    print (rows)
    return render_template("home.html", rows=rows, category=category, categories=CATEGORIES)
