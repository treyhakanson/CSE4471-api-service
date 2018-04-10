import requests

HOST = "http://localhost:5000"
auth = {
    "email": "danarters@gmail.com",
    "password": "password"
}

def test_login():
    print requests.post(HOST+"/login", json=auth).json()


def test_dual_token_retrieval():
    token = requests.get(HOST+"/login", json=auth).json()["token"]
    print requests.get(HOST+"/dual-factor-token", json={"token": token}).json()

def test_get_phrase():
    token = requests.get(HOST+"/login", json=auth).json()["token"]
    print requests.get(HOST+"/phrase", json={"token": token}).json()

# test_login()
# test_dual_token_retrieval()
test_get_phrase()
