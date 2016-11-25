GoChatCLI services
==================


----------

## Local development ##

Install all the dependencies :

 - `pip2 install -r requirements.txt`



Start the flask server :



 - `npm run dev`

Deploying to AWS
-------

- Install serverless :

    `npm install -g serverless`

- Install AWS CLI. Instructions can be found [here](http://docs.aws.amazon.com/cli/latest/userguide/installing.html).


- Configure AWS CLI. Instructions can be found [here](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).

- cd into the services directory and install all the required dependencies

  `cd services`

	`npm run installDep`


- Deploy using serverless :

    `serverless deploy`
