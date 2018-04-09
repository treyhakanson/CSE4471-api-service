import hashlib
import json
import re

try:
    with open('settings.py', 'rb') as settings: exec(settings.read())
except:
    print "You must have a settings files to designate server key and db path"

def hash(val, salt):
	return hashlib.sha512(salt+val).hexdigest()

def verify_token(token):
	pattern = "\/\/(?P<data>{[^;]*});sign=(?P<sign>[^\/]+)\/\/"
	match = re.match(pattern, token)
	try:
		signature = hash(match.group('data'), SERVER_KEY)
		data = json.loads(match.group('data'))
		return (signature == match.group('sign'), data)
	except ValueError, AttributeError:
		return (False, None)

def sign(data):
	json_data = json.dumps(data, sort_keys=True)
	signature = hash(json_data, SERVER_KEY)
	return "//%s;sign=%s//" % (json_data, signature)
