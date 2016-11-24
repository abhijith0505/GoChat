GoChatCLI services
==================


----------

## Local development ##

Install all the dependencies :

 - `pip2 install -r requirements.txt`



Start the flask server :



 - `export FLASK_APP=app.py`
 - `flask run`

Deploying to AWS
-------

- Install serverless :


    `npm install -g serverless`




- Install AWS CLI. Instructions can be found [here](http://docs.aws.amazon.com/cli/latest/userguide/installing.html).


- Configure AWS CLI. Instructions can be found [here](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).

- cd into the services directory and install all the required dependencies
	`cd services`
	`npm install`
	`pip2 install -t python_modules/ -r requirements.txt`

- Deploy using serverless :
	`serverless deploy`
