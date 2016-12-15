import argparse, getpass, sys
import apiHelper


parser = argparse.ArgumentParser(description='This is terminal chat application')

parser.add_argument('-r', '--register', action='store_true', dest='register',
                    help='Register user')

parser.add_argument('--version', '-v', action='version', version='%(prog)s 1.0')

if len(sys.argv) < 2:
    parser.print_usage()
    sys.exit(1)

args = parser.parse_args()

register = args.register

if args.register:
     username = raw_input("Username:")
     password = getpass.getpass("Password:")
     response = apiHelper.registerUser(username,password)
     if response == "exists":
          print "User exists! Try again"
          sys.exit(1)
     else:
          print "User created!"
