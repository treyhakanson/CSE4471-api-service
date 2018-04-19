import sqlite3
import uuid
import time
from flask import g
import cStringIO

import hash
import push
import passphrase_generator

try:
    with open('settings.py', 'rb') as settings: exec(settings.read())
except:
    print "You must have a settings files to designate server key and db path"

# DB utility functions
def get_db():
    if not getattr(g, "_database", None):
        setattr(g, "_database", sqlite3.connect(DB_PATH))
        g._database.row_factory = sqlite3.Row
    return g._database

def query_db(sql, args=[], one=False):
    cursor = get_db().execute(sql, args)
    result = cursor.fetchall()
    cursor.close()
    if one:
        result = result[0] if result else None
    return result

# Functionality
def get_user(email):
    sql = "SELECT * FROM User WHERE email=? LIMIT 1;"
    return query_db(sql, [email], one=True)

def get_user_by_id(user_id):
    sql = "SELECT * FROM User WHERE user_id=? LIMIT 1;"
    return query_db(sql, [email], one=True)

def verify_password(user, password):
    pass_hash = hash.hash(password, user["salt"])
    success = pass_hash == user["password"]
    if not success:
        pass # Check for too many login attempts?
    return success

def signup(email, password, push_token):
    salt = str(uuid.uuid4())
    password = hash.hash(password, salt)
    sql = """
        INSERT INTO User (email, salt, password, push_token)
            VALUES(?, ?, ?, ?);
    """
    query_db(sql, [email, salt, password, push_token])
    return query_db("SELECT * FROM User WHERE email=?;", [email], one=True)

def get_token(user, dual=False):
    data = {
        "user_id": user["user_id"],
        "session": str(uuid.uuid4()),
        "authtype": "dual" if dual else "standard",
        "created_at": int(time.time())
    }
    return hash.sign(data)

def get_session_passphrase(token):
    success, data = hash.verify_token(token)
    if success:
        row = get_passphrase(data["user_id"], data["session"])
        if row:
            phrase = row["phrase"]
            push_key = row["push_key"]
        else:
            phrase, push_key = create_passphrase(data["user_id"], data["session"])
            user = get_user_by_id(data["user_id"])
        push.send_push(user["push_token"], {"key": push_key})
        return phrase
    return None

def submit_audio(token, push_key=None, audio=None):
    success, data = hash.verify_token(token)
    if success:
        audiofile = cStringIO.StringIO()
        audiofile.write(audio)
        audio_phrase = speech_recog.read_audio(audiofile)
        phrase = get_passphrase(data["user_id"], data["session"])
        verified_phrases = phrase["phrase"] == audio_phrase
        verified_push_keys = phrase["push_key"] == push_key
        if verified_phrases and verified_push_keys:
            updated_verified_passphrase(user_id, session)

def get_passphrase(user_id, session):
    sql = """
        SELECT * FROM Phrases
        WHERE user_id=? AND session=?
        LIMIT 1;
    """
    return query_db(sql, [user_id, session], one=True)

def create_passphrase(user_id, session):
    sql = """
        INSERT INTO Phrases (user_id, phrase, session, push_key)
        VALUES(?, ?, ?, ?);
    """
    phrase = passphrase_generator.get_passphrase(5)
    push_key = str(uuid.uuid4())
    query_db(sql, [user_id, phrase, session, push_key])
    return phrase, push_key

def updated_verified_passphrase(user_id, session):
    sql = """
        UPDATE FROM Phrases
        WHERE user_id=? AND session=?
        SET verified=TRUE;
    """
    query_db(sql, [user_id, session])

def check_dual_factor(token):
    success, data = hash.verify_token(token)
    if success:
        sql = """
            SELECT * FROM Phrases
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
