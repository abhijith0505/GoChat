import argparse, getpass, sys
import apiHelper


parser = argparse.ArgumentParser(description='This is terminal chat application')

parser.add_argument('-r', '--register', action='store_true', dest='register',
                    help='Register user')

parser.add_argument('-d', '--delete-user', action='store_true', dest='deleteUser',
                    help='Delete your account')

parser.add_argument('-lo', '--logout', action='store_true', dest='logout',
                    help='Log out')

parser.add_argument('--version', '-v', action='version', version='%(prog)s 1.0')

if len(sys.argv) < 2:
    parser.print_usage()
    sys.exit(1)

args = parser.parse_args()

register = args.register
deleteUser = args.deleteUser


if register:
     username = raw_input("Username:")
     password = getpass.getpass("Password:")
     while not username:
     	print "Please choose a username"
     	username = raw_input("Username:")

     while not password:
     	print "Please choose a password"
     	password = getpass.getpass("Password:")

     response = apiHelper.registerUser(username,password)
     if response == "exists":
          print "User exists! Try again"
          sys.exit(1)
     else:
          print "User created!"
          print "Please login"
          parser.print_usage()

if deleteUser:
	username = raw_input("Username:")
	password = getpass.getpass("Password:")
	
	if apiHelper.deleteUser(username,password):
		print "Your account has been deleted"
	else:
		print "Incorrect credentials!"
		print "You shall have power to delete only your accout"
