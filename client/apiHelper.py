import requests, json
import variables, pymongo
from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient()
db = client['gochat']
user = db['user']
user.ensure_index('username',unique=True)

def checkUser(username):
    url = variables.AWSEndPoint + "/checkUser"
    data = {"username": username}
    json_data = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    return response.text

def registerUser(username, password):
    url = variables.AWSEndPoint + "/registerUser"
    data = {"username": username, "password": password}
    json_data = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    try:
        db.user.insert_one({'username':username, 'password': hash_pass(password)})
    except:
        print "nononono"

    return response.text

def hash_pass(password):
    # used to hash the password similar to how MySQL hashes passwords with the password() function.
    import hashlib
    hash_password = hashlib.sha1(password.encode('utf-8')).digest()
    hash_password = hashlib.sha1(hash_password).hexdigest()
    hash_password = '*' + hash_password.upper()
    return hash_password