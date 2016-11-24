from flask import Flask, request, jsonify, abort
import  time, boto3, sys, os
from threading import Timer
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
app = Flask(__name__)
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
goChatUsersTable = dynamodb.Table('goChatUsers')




# Enter the following command in CLI to test this API
# curl -i -H "Content-type: application/json" -X POST -d '{"username":"usrnm","password":"pwd"}'  http://localhost:5000/registerUser
@app.route("/registerUser", methods=['POST'])
def registerUser():
    if not request.json or not 'username' in request.json or 'password' not in request.json:
        abort(400)
    user = {
        'username': request.json['username'],
        'password': request.json['password']
    }
    goChatUsersTable.put_item(
        Item=user
    )
    response = goChatUsersTable.get_item(
        Key = {
            'username': request.json['username']
        }
    )
    return jsonify(response), 201



#following code is for Sharath's system as ctrl+C does not seem to kill flask server
#Enter the following in CLI to kill the server :
# curl -i -H "Content-Type: application/json" -X POST  http://localhost:5000/kill
LAST_REQUEST_MS = 0
@app.before_request
def update_last_request_ms():
    global LAST_REQUEST_MS
    LAST_REQUEST_MS = time.time() * 1000


@app.route('/seriouslykill', methods=['POST'])
def seriouslykill():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "Shutting down..."


@app.route('/kill', methods=['POST'])
def kill():
    last_ms = LAST_REQUEST_MS
    def shutdown():
        if LAST_REQUEST_MS <= last_ms:  # subsequent requests abort shutdown
            requests.post('http://localhost:5000/seriouslykill')
        else:
            pass

    Timer(1.0, shutdown).start()  # wait 1 second
    return "Shutting down..."
