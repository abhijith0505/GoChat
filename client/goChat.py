import argparse, getpass, sys, json, time, pymongo
from pymongo import MongoClient
import apiHelper

client = MongoClient()
db = client['gochat']
user = db['user']
messages = db['messages']
user.ensure_index('username',unique=True)

parser = argparse.ArgumentParser(description='This is terminal chat application')

parser.add_argument('-r', '--register', action='store_true', dest='register',
					help='Register user')

parser.add_argument('-d', '--delete-user', action='store_true', dest='deleteUser',
					help='Delete your account. Deletes complete user credentials and messages. You\'ll have to start fresh')

parser.add_argument('-s', '--send', action='store_true', dest='send',
					help='To send message')

parser.add_argument('-u', '--unread', action='store_true', dest='unread',
					help='Read your unread messages')

parser.add_argument('--version', '-v', action='version', version='%(prog)s 1.0')

if len(sys.argv) < 2:
	parser.print_usage()
	sys.exit(1)

args = parser.parse_args()

register = args.register
deleteUser = args.deleteUser
send = args.send
unread = args.unread

if register:
	selfUser = db.user.find_one()
	if not selfUser:
		username = raw_input("Username:")
		while not username:
			print "Please choose a username"
			username = raw_input("Username:")

		password = getpass.getpass("Password:")
		while not password:
			print "Please choose a password"
			password = getpass.getpass("Password:")

		response = apiHelper.registerUser(username,password)

		if response == "exists":
			print "User exists! Try again"
			sys.exit(1)
		else:
			print "User created!"
	else:
		print "User already exists in this computer"
		print "Current version supports only one user per computer"
		print "Please, use existing user or delete user from your system"
		parser.print_help()
		print ""

if deleteUser:
	if apiHelper.deleteUser():
		print "Your computer is free from GOChatCLI accounts now"
	else:
		print "There is nothing to delete, please register an account, so that you can delete it later."

if send:
	selfUser = db.user.find_one()
	selfUserName = selfUser['username']
	toUsername = raw_input("Username of recipient: ")
	while not toUsername:
		print "Specify recipient username"
		toUsername = raw_input("Username of recipient: ")

	while toUsername == selfUserName:
		print "Why would you want to send yourself a message? :/"
		toUsername = raw_input("Username of recipient: ")
	
	toMessage = raw_input("Message: ")
	while not toMessage:
		print "Specify message to be sent"
		toMessage = raw_input("Message: ")

	print apiHelper.sendMessage(toUsername, toMessage)

if unread:
	try:
		unreadMessages = apiHelper.unreadMessages()
		unreadMessages = json.loads(unreadMessages)
		messagesToBeStored = []
		for msg in unreadMessages:
			print ('{}: {}'.format(msg['timestamp'], msg['message']))
			messageToBeStored = {}
			messageToBeStored['timestamp'] = msg['timestamp']
			messageToBeStored['message'] = msg['message']
			messagesToBeStored.append(messageToBeStored)
	except:
		print "No New Messages"
	
