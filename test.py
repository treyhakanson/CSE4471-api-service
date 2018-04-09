import requests

HOST = "http://localhost:5000"

def test_login():
    data = {
        "email": "danarters@gmail.com",
        "password": "password"
    }
    print requests.get(HOST+"/login", json=data).json()

test_login()
