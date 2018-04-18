import requests
import string
import random

HOST = "http://localhost:5000"
auth = {
    "email": "danarters@gmail.com",
    "password": "password"
}

def get_random_string():
    return "".join([random.choice(string.letters) for _ in range(10)])

def test_signup():
    signup_data = {
        "email": get_random_string()+"@gmail.com",
        "password": "password",
        "push_token": get_random_string()
    }
    print requests.post(HOST+"/signup", json=signup_data).json()

def test_login():
    print requests.post(HOST+"/login", json=auth).json()

def test_dual_token_retrieval():
    token = requests.get(HOST+"/login", json=auth).json()["token"]
    print requests.get(HOST+"/dual-factor-token", json={"token": token}).json()

def test_get_phrase():
    token = requests.get(HOST+"/login", json=auth).json()["token"]
    print requests.get(HOST+"/phrase", json={"token": token}).json()

def test_get_phrases():
    token = requests.get(HOST+"/login", json=auth).json()["token"]
    print requests.get(HOST+"/dual-requests", json={"token": token}).json()


test_signup()
# test_login()
# test_dual_token_retrieval()
# test_get_phrase()
# test_get_phrases()
