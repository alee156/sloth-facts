# :paw_prints: Endangered Species Facts 
An Alexa skill that gives interesting facts about endangered species and attempts to bring more attention to them.

## :wave: [Contribute interesting facts here](https://airtable.com/shrWUQJ7pjSDDgip5)

# :smiley_cat: Getting Started 
In order to get started you will need to create an alexa developer account and an aws account.

* [Alexa Developer](https://developer.amazon.com/alexa)
* [Amazon Web Services (AWS)](https://aws.amazon.com/)

## Setting up Alexa Skill


## Setting up AWS
1. Install [Serverless](https://serverless.com/)
2. Install [serverless-python-requirements](https://www.npmjs.com/package/serverless-python-requirements)
3. `pip install -r requirements.txt`


## Deploy fulfillment handler
You can deploy with your default aws profile

`sls deploy`

Or deploy with a different profile:

`AWS_PROFILE=alexa-user sls deploy`