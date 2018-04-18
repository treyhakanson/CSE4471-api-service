from exponent_server_sdk import PushClient, PushMessage

def send_push(push_token, data, message="You have a requested login verification"):
    push = PushMessage(to=push_token, body=message, data=data)
    response = PushClient().publish(push)
    print response
