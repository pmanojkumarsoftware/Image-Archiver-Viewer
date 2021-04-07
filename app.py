import sqlite3
import os
from flask import Flask, g, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
from settings import DATABASE, CAT2, CATEGORIES, PH_FOLDER

app = Flask(__name__, static_url_path="")


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


@app.route("/photos/<path:path>")
def send_js(path):
    return send_from_directory("photos", path)


@app.route("/", methods=["POST", "GET"])
def hello_world():
    if request.method == "POST":
        c = request.form["category"].lower()
        f = request.files["file"]
        if not c in CATEGORIES:
            return "category not recognised"
        file_path = os.path.join(PH_FOLDER, c, secure_filename(f.filename))
        f.save(file_path)
        conn = get_db()
        cur = conn.cursor()
        cur.execute("insert into photos values (?,?)", (c, file_path))
        conn.commit()
        return "file uploaded successfully"
    else:
        category = request.args.get("category", CAT2)
        rows = []
        if category in CATEGORIES:
            print("CAT:", category)
            cur = get_db().cursor()
            for category, filename in cur.execute(
                "SELECT * FROM photos where category=?", (category,)
            ):
                rows.append(filename)

        print(rows)
        return render_template(
            "home.html", rows=rows, category=category, categories=CATEGORIES
        )
