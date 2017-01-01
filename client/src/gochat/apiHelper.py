import requests
import json
import random
import sys
import os
import rabinMiller
import cryptomath
import variables
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
from requests.auth import HTTPBasicAuth
DEFAULT_BLOCK_SIZE = 128
BYTE_SIZE = 256

client = MongoClient("mongodb://localhost:26969/")
db = client['gochat']
user = db['user']
messages = db['messages']
user.ensure_index('username', unique=True)


def checkUser(username):
    url = variables.AWSEndPoint + "/checkUser"
    data = {"username": username}
    json_data = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    return response.text


def registerUser(username, password):
    url = variables.AWSEndPoint + "/registerUser"
    publicKey, privateKey = generateKey(128)
    data = {"username": username, "password": hash_pass(
        password), "publicKey": json.dumps(publicKey)}
    json_data = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    if response.text != "exists":
	    try:
	        db.user.insert_one({'username': username, 'password': hash_pass(
	            password), 'privateKey': json.dumps(privateKey)})
	    except Exception:
	    	Exception

    return response.text


def deleteUser():
	try:
		selfUser = db.user.find_one()
		selfUserName = selfUser['username']
		selfPassword = selfUser['password']
		requests.get(variables.AWSEndPoint + '/removeUser',
		             auth=(selfUserName, selfPassword))
		db.user.drop()
		return True
	except:
		return False


def getPublicKey(recipient):
    url = variables.AWSEndPoint + "/getPublicKey"
    selfUser = db.user.find_one()
    selfUserName = selfUser['username']
    selfPassword = selfUser['password']
    url = variables.AWSEndPoint + "/getPublicKey"
    data = {"username": recipient}
    json_data = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, auth=(
        selfUserName, selfPassword), data=json_data, headers=headers)
    return [float(i) for i in response.text.strip('[]').split(',')]
    # return response.text



def sendMessage(recipient, message):
    selfUser = db.user.find_one()
    selfUserName = selfUser['username']
    selfPassword = selfUser['password']
    if "true" in checkUser(recipient):
        url = variables.AWSEndPoint + "/newMessage"
        publicKey = (getPublicKey(recipient))
        encryptedBlocks = encryptMessage(
            message, publicKey, DEFAULT_BLOCK_SIZE)
        for i in range(len(encryptedBlocks)):
            encryptedBlocks[i] = str(encryptedBlocks[i])
        encryptedContent = ','.join(encryptedBlocks)
        encryptedContent = '%s_%s_%s' % (
            len(message), DEFAULT_BLOCK_SIZE, encryptedContent)
        data = {"to": recipient, "message": encryptedContent}
        json_data = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, auth=(
            selfUserName, selfPassword), data=json_data, headers=headers)
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
	# db.messages.insert(data)

	return response.text


def hash_pass(password):
    # used to hash the password similar to how MySQL hashes passwords with the
    # password() function.
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


def getBlocksFromText(message, blockSize=DEFAULT_BLOCK_SIZE):
     # Converts a string message to a list of block integers. Each integer
     # represents 128 (or whatever blockSize is set to) string characters.

     messageBytes = message.encode('ascii')  # convert the string to bytes
     print (message)
     print (messageBytes)

     blockInts = []
     for blockStart in range(0, len(messageBytes), blockSize):
         # Calculate the block integer for this block of text
         blockInt = 0
         for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
             print (type(messageBytes[i]))
             blockInt += (messageBytes[i]) * (BYTE_SIZE ** (i % blockSize))
         blockInts.append(blockInt)
     return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE):
    # Converts a list of block integers to the original message string.
    # The original message length is needed to properly convert the last
    # block integer.
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                 # Decode the message string for the 128 (or whatever
                 # blockSize is set to) characters from this block integer.
                asciiNumber = blockInt // (BYTE_SIZE ** i)
                blockInt = blockInt % (BYTE_SIZE ** i)
                blockMessage.insert(0, chr(asciiNumber))
        message.extend(blockMessage)
    return ''.join(message)


def encryptMessage(message, key, blockSize=DEFAULT_BLOCK_SIZE):
    # Converts the message string into a list of block integers, and then
    # encrypts each block integer. Pass the PUBLIC key to encrypt.
    encryptedBlocks = []
    n, e = key

    for block in getBlocksFromText(message, blockSize):
         # ciphertext = plaintext ^ e mod n
        encryptedBlocks.append(pow(block, int(e), int(n)))
    return encryptedBlocks


def decryptMessage(encryptedBlocks, messageLength, key, blockSize=DEFAULT_BLOCK_SIZE):
     # Decrypts a list of encrypted block ints into the original message
     # string. The original message length is required to properly decrypt
     # the last block. Be sure to pass the PRIVATE key to decrypt.
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
         # plaintext = ciphertext ^ d mod n
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)

def test():
	response = [{"timestamp": 1481886764, "message": "hihhi", "from": "sha"}]
	print (json.dumps(response))
