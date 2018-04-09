import sqlite3
import uuid
from flask import g
from datetime import datetime

from hash import hash

# DB utility functions
def get_db():
    if not getattr(g, "_database", None):
        setattr(g, "_database", sqlite3.connect(DB_PATH))
    return g._database

def query_db(sql, args=[], one=False):
    cursor = get_db().execute(query, args)
    result = cursor.fetchall()
    cursor.close()
    if one:
        result = result[0] if result else None
    return result

# Functionality
def get_user(email):
    sql = "SELECT * FROM User WHERE email=? LIMIT 1;"
    return query_db(sql, [email], one=True)

def verify_password(user, password):
    pass_hash = hash(password, user["salt"])
    success = pass_hash == user["password"]
    if not success:
        pass # Check for too many login attempts?
    return success

def get_token(user, dual=False):
    data = {
        "user_id": user["user_id"],
        "session": str(uuid.uuid4()),
        "authtype": "dual" if dual else "standard",
        "created_at": datetime.now()
    }
    return hash.sign(data)

def get_session_passphrase(token):
    success, data = hash.verify_token(token)
    if success:
        sql = """
            SELECT * FROM Phrases
            WHERE user_id=? AND session=?
            LIMIT 1;
        """
        row = query_db(sql, [data["user_id"], data["session"]], one=True)
        phrase = row["phrase"] if row else create_passphrase(user, session)
        return phrase
    return None

def create_passphrase(user_id, session):
    sql = "INSERT INTO Phrases (user_id, phrase, session) VALUES(?, ?, ?);"
    phrase = "Test phrase authentication" # TODO change this
    query_db(sql, [user_id, phrase, session])
    return phrase

def check_dual_factor(token):
    success, data = hash.verify_token(token)
    if success:
        sql = """
            SELECT * FROM get_phrases
            WHERE user_id=? AND session=?
            LIMIT 1;
        """
        row = query_db(sql, [data["user_id"], data["session"]], one=True)
        if row and row["verified"]:
            success = True
            data["authtype"] = "dual"
            return True, hash.sign(data)
        else:
            return False, hash.sign(data)
    else:
        return False, None
