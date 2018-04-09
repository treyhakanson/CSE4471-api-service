import hashlib
import json

# Unique private key on the server, used to verify that tokens are not modified 
server_key = "47731a07-7d1f-4186-86af-1203e721ef7c"

def hash(val, salt):
	return hashlib.sha512(salt+val).hexdigest()

def verify_token(token):
	pattern = "\/\/(?P<data>{[^;]*});sign=(?P<sign>[^\/]+)\/\/"
	match = re.match(pattern, token)
	try:
		signature = hash(match.group('data'), server_key)
		data = json.loads(match.group('data'))
		return (signature == match.group('sign'), data)
	except ValueError, AttributeError:
		return (False, None)

def sign(data):
	json_data = json.dumps(data, sort_keys=True)
	signature = hash(json_data, server_key)
	return "//%s;sign=%s//" % (json_data, signature)
