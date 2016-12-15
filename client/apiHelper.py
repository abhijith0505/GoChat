import requests, json
import variables

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
    return response.text
