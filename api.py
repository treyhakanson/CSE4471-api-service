from flask import Flask, g
app = Flask(__name__)

# App constants
DB_PATH = "db.sqlite"

# Database connection
def get_db():
    if not getattr(g, "_database", None):
        setattr(g, "_database", sqlite3.connect(DB_PATH))
    return g._database

@app.teardown_appcontext
def close_connection(exception):
    if getattr(g, "_database", None):
        g._database.close()

@app.route("/")
def index():
    return "index"

app.run()
