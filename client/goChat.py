import argparse, getpass, sys
import apiHelper


parser = argparse.ArgumentParser(description='This is terminal chat application')

parser.add_argument('-r', '--register', action='store_true', dest='register',
					help='Register user')

parser.add_argument('-d', '--delete-user', action='store_true', dest='deleteUser',
					help='Delete your account')

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

if deleteUser:
	username = raw_input("Username:")
	while not username:
		print "Please enter a username"
		username = raw_input("Username:")

	password = getpass.getpass("Password:")
	while not password:
		print "Please enter a password"
		password = getpass.getpass("Password:")

	if apiHelper.deleteUser(username,password):
		print "Your account has been deleted"
	else:
		print "Incorrect credentials!"
		print "Thou shall have power to delete only thy account"

if send:
	toUsername = raw_input("Username of recipient: ")
	while not toUsername:
		print "Specify recipient username"
		toUsername = raw_input("Username of recipient: ")
	
	toMessage = raw_input("Message: ")
	while not toMessage:
		print "Specify message to be sent"
		toMessage = raw_input("Message: ")

	print apiHelper.sendMessage(toUsername, toMessage)

if unread:
	unreadMessages = apiHelper.unreadMessages()
	print unreadMessages