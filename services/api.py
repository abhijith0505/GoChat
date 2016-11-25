from flask import Flask, request, jsonify, abort, make_response
import time, boto3, sys, os, requests, json, decimal
from threading import Timer
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./python_modules"))

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
goChatUsersTable = dynamodb.Table('goChatUsers')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


# Enter the following command in CLI to test this API
# curl -i -H "Content-type: application/json" -X POST -d '{"username":"usrnm","password":"pwd"}'  http://localhost:5000/registerUser
@app.route("/registerUser", methods=['POST'])
def registerUser():
    if not request.json or not 'username' in request.json or 'password' not in request.json:
        abort(400)
    user = {
        'username': request.json['username'],
        'password': request.json['password'],
        'newMessages': []
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



#curl -i -H "Content-Type: application/json" -u usrnm:pwd -X POST -d '{"to":"nd","message":"sup"}' http://localhost:5000/newMessage

@app.route('/newMessage', methods=['POST'])
@auth.login_required
def newMessage():
    if not request.json or not 'to' in request.json or not 'message' in request.json:
        abort(400)
    response = goChatUsersTable.get_item(
        Key = {
            'username': request.json['to']
        }
    )

    if not 'Item' in response:
        abort(400)
    newMessage = {
        'from': auth.username(),
        'message': request.json['message'],
        'timestamp': int(time.time())
    }
    response = goChatUsersTable.update_item(
        Key={
            'username': request.json['to']
        },
        UpdateExpression="SET newMessages = list_append(newMessages, :i)",
        ExpressionAttributeValues={
            ':i': [newMessage]
        },
        ReturnValues="UPDATED_NEW"
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200 and 'Attributes' in response:
        return "Message sent succesfully"


# curl -i -H "Content-Type: application/json" -X POST -d '{"username":"usrnm"}' http://localhost:5000/checkUser

@app.route('/checkUser', methods=['POST'])
def checkUser():
    response = goChatUsersTable.get_item(
        Key={
            'username': request.json['username']
        }
    )
    try:
        response['Item']['username']
        return "Username already exists"
    except :
        return "Username does not exist"

# curl -u usrnm:pwd -i http://localhost:5000/getUsers

@app.route('/getUsers', methods=['GET'])
@auth.login_required
def getUsers():
    response = goChatUsersTable.scan(
        Select = 'SPECIFIC_ATTRIBUTES',
        AttributesToGet = [
            'username'
        ]
    )
    return jsonify(response['Items'])

# curl -u usrnm:pwd http://localhost:5000/getNewMessages

@app.route('/getNewMessages', methods=['GET'])
@auth.login_required
def getNewMessages():
    response= goChatUsersTable.get_item(
        Key = {
            'username': auth.username()
        }
    )
    newMessages = response['Item']['newMessages']
    if newMessages:
        response = goChatUsersTable.update_item(
            Key={
                'username': auth.username()
            },
            UpdateExpression="SET newMessages = :i",
            ExpressionAttributeValues={
                ':i': []
            },
            ReturnValues="UPDATED_NEW"
        )
        if not response['Attributes']['newMessages']:
            return json.dumps(newMessages, cls=DecimalEncoder)
        else:
            return "Sync failed"
    else:
        return "No new messages"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@auth.get_password
def get_password(username):
    try:
        response = goChatUsersTable.get_item(
            Key = {
                'username': username
            }
        )
        return response['Item']['password']
    except Exception as e:
        raise
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
