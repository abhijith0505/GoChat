import requests, json, random, sys, os, rabinMiller, cryptomath, variables, pymongo
from pymongo import MongoClient
from bson.json_util import dumps
from requests.auth import HTTPBasicAuth

client = MongoClient("mongodb://localhost:26969/")
db = client['gochat']
user = db['user']
messages = db['messages']
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
    publicKey, privateKey = generateKey(1024)
    data = {"username": username, "password": hash_pass(password), "publicKey": publicKey}
    json_data = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    if response.text != "exists":
	    try:
	        db.user.insert_one({'username':username, 'password': hash_pass(password), 'privateKey': privateKey})
	    except e:
	    	print e

    return response.text

def deleteUser():
	try:
		selfUser = db.user.find_one()
		selfUserName = selfUser['username']
		selfPassword = selfUser['password']
		requests.get(variables.AWSEndPoint + '/removeUser', auth=(selfUserName, selfPassword))
		db.user.drop()
		return True
	except:
		return False


def sendMessage(recipient, message):
	selfUser = db.user.find_one()
	selfUserName = selfUser['username']
	selfPassword = selfUser['password']
	if "true" in checkUser(recipient):
		url = variables.AWSEndPoint + "/newMessage"
		data = {"to": recipient, "message": message}
		json_data = json.dumps(data)
		headers = {'Content-type': 'application/json'}
		response = requests.post(url, auth=(selfUserName, selfPassword), data=json_data, headers=headers)
		return response.text
	else:
		return "No such user exists!"


def unreadMessages():
	selfUser = db.user.find_one()
	selfUserName = selfUser['username']
	selfPassword = selfUser['password']

	url = variables.AWSEndPoint + "/getNewMessages"
	response = requests.get(url, auth=(selfUserName, selfPassword))

	data = json.loads(response.text)
	#db.messages.insert(data)

	return response.text



def hash_pass(password):
    # used to hash the password similar to how MySQL hashes passwords with the password() function.
    import hashlib
    hash_password = hashlib.sha1(password.encode('utf-8')).digest()
    hash_password = hashlib.sha1(hash_password).hexdigest()
    hash_password = '*' + hash_password.upper()
    return hash_password

def generateKey(keySize):
     # Creates a public/private key pair with keys that are keySize bits in
     # size. This function may take a while to run.

     # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
     p = rabinMiller.generateLargePrime(keySize)
     q = rabinMiller.generateLargePrime(keySize)
     n = p * q

     # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
     while True:
         # Keep trying random numbers for e until one is valid.
         e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
         if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
             break

     # Step 3: Calculate d, the mod inverse of e.
     d = cryptomath.findModInverse(e, (p - 1) * (q - 1))

     publicKey = (n, e)
     privateKey = (n, d)

     return (publicKey, privateKey)

def test():
	response = [{"timestamp": 1481886764, "message": "hihhi", "from": "sha"}]
	print json.dumps(response)
