from flask import Flask, g, request, jsonify, render_template
import os.path

import db

# Set to True to auto reload on change, otherwise False
DEBUG = True

app = Flask(__name__)

# Error trapping on database connections
@app.teardown_appcontext
def close_connection(exception):
    if getattr(g, "_database", None):
        g._database.close()

# Serve static files
@app.route('/static/<path:path>')
def static_proxy(path):
  return app.send_static_file("static/%s" % path)

# Frontend routes
@app.route("/demo/<string:page_name>")
def index(page_name):
    return render_template("%s.html" % (page_name))

# API routes
@app.route("/login", methods=["POST", "GET"])
def login():
    '''
    Returns either
    {outcome: "failure"}
    ...or...
    {outcome: "successful", token:"token-string"}
    based on if the email/password were correct
    '''
    data_dict = request.get_json()
    email = data_dict.get("email", "")
    password = data_dict.get("password", "")
    response = {"outcome": "failure"}
    if email and password:
        user = db.get_user(email)
        if user and db.verify_password(user, password):
            response["token"] = db.get_token(user, dual=False)
            response["outcome"] = "successful"
    return jsonify(response)

@app.route("/signup", methods=["POST", "GET"])
def signup():
    '''
    Creates a user with an email, hashed password, push_token,
    and randomized salt.
    '''
    data_dict = request.get_json()
    email = data_dict.get("email", "")
    password = data_dict.get("password", "")
    push_token = data_dict.get("push_token", "")
    response = {"outcome": "failure"}
    if email and password and push_token:
        user = db.signup(email, password, push_token)
        response["token"] = db.get_token(user)
        response["outcome"] = "successful"
    return jsonify(response)

@app.route("/dual-factor-token")
def dual_token():
    '''
    Returns an updated session token. If the dual factor was successful
    on the app side, the token will be updated accordingly, and the outcome
    will be marked as successful as opposed to failure
    '''
    data_dict = request.get_json()
    token = data_dict.get("token", "")
    success, updated_token = db.check_dual_factor(token)
    response = {
        "token": updated_token,
        "outcome": "successful" if success else "failure"
    }
    return jsonify(response)

@app.route("/phrase", methods=["POST", "GET"])
def get_phrase():
    '''
    Returns the phrase for the current session as indicated in
    the token. This token has to be authentic (signed correctly)
    to return any phrase.
    If there is already a phrase, it is simply fetched. If not, one
    is created for the current session and returned in fomrat...
    {phrase: "this will be a phrase"}.
    In addition, a push notifiation is sent to the user's phone with
    the specific key needed to verify the authentication request. This
    is the only time the push_key is visible, and thus, only the phone
    recieving the push notificartion can verify the auth request.
    '''
    data_dict = request.get_json()
    token = data_dict.get("token", "")
    phrase = db.get_session_passphrase(token)
    return jsonify({"phrase": phrase})

@app.route("/dual-requests")
def get_phrases():
    '''
    Returns all the dual-auth phrases for the user requesting.
    Must have a valid single-auth token to do so.
    '''
    data_dict = request.get_json()
    token = data_dict.get("token", "")
    requests = db.get_dual_requests(token)
    response = {"requests": requests}
    return jsonify(response)

@app.route("/submit-phrase-audio", methods=["GET", "POST"])
def submit_phrase_audio():
    '''
    Attempts to verify the audio sent up with the session stored
    in the single-auth token. Updates the dual auth database
    entry if needed and returns an outcome of success or failure.
    '''
    token = request.form.get("token", "")
    audioFile = request.files.get("audio", None)
    success = db.submit_audio(token)
    response = {"outcome": "successful" if success else "failure"}
    return jsonify(response)


app.run(debug=DEBUG)
