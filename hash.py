import hashlib
import json
import re
import base64

try:
    with open('settings.py', 'rb') as settings: exec(settings.read())
except:
    print "You must have a settings files to designate server key and db path"

def hash(val, salt):
	return hashlib.sha512(salt+val).hexdigest()

def urlencode(token):
	return base64.b64encode(token).strip("=")

def urldecode(token):
	padding = (4 - len(token)) % 4
	return base64.b64decode(token + (padding*"="))

def verify_token(token):
	token = urldecode(token)
	pattern = "\/\/(?P<data>{[^;]*});sign=(?P<sign>[^\/]+)\/\/"
	match = re.match(pattern, token)
	try:
		signature = hash(match.group('data'), SERVER_KEY)
		data = json.loads(match.group('data'))
		return (signature == match.group('sign'), data)
	except:
		return (False, None)

def sign(data):
	json_data = json.dumps(data, sort_keys=True)
	signature = hash(json_data, SERVER_KEY)
	token = "//%s;sign=%s//" % (json_data, signature)
	return urlencode(token)
