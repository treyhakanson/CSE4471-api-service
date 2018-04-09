import requests

HOST = "http://localhost:5000"

def test_login():
    data = {
        "email": "danarters@gmail.com",
        "password": "password"
    }
    print requests.post(HOST+"/login", json=data).json()


def test_dual_token_retrieval():
    token = requests.get(HOST+"/login", json={
        "email": "danarters@gmail.com",
        "password": "password"
    }).json()["token"]
    print requests.get(HOST+"/dual-factor-token", json={"token": token}).json()

test_login()
test_dual_token_retrieval()
