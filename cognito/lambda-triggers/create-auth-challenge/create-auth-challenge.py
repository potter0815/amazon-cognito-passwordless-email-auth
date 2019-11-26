
import boto3
# generate random integer values
from random import seed
from random import randint
import os
import json

localtest = False

try:
    SES_FROM_ADDRESS = os.environ['SES_FROM_ADDRESS']
except Exception: 
    localtest = True
    filename = os.getcwd() + "/event.json"
    f = open(filename)
    event = json.loads(f.read())   
    context = ""
    SES_FROM_ADDRESS = "csc+cognito_e-mail_auth_backend@amazon.de"
    


ses = boto3.client('ses')
#import { CognitoUserPoolTriggerHandler } from 'aws-lambda';
#export const handler: CognitoUserPoolTriggerHandler = async event => {

def handler(event, context):

    secretLoginCode = ""
    if not event['request']['session'] or  not event['request']['session']['length']:

        # This is a new auth session
        # Generate a new secret login code and mail it to the user
        # seed random number generator
        seed(763437)        
        secretLoginCode = randint(6, 6)

        sendEmail(event['request']['userAttributes']['email'], secretLoginCode)
        print('if:.....')
    else:
        # There's an existing session. Don't generate new digits but
        # re-use the code from the current session. This allows the user to
        # make a mistake when keying in the code and to then retry, rather
        # the needing to e-mail the user an all new code again.    
        #const previousChallenge = event['request']['session'].slice(-1)[0];
        # JS: secretLoginCode = previousChallenge.challengeMetadata!.match(/CODE-(\d*)/)![1];
        previousChallenge = event['request']['session'][0]  
        secretLoginCode = previousChallenge['challengeMetadata'][5:11]    
        print('secretLoginCode {}'.format(secretLoginCode))
        print('else:.....')
    

    # This is sent back to the client app
    event['response']['publicChallengeParameters'] = { 'email': event['request']['userAttributes']['email'] }

    # Add the secret login code to the private challenge parameters
    # so it can be verified by the "Verify Auth Challenge Response" trigger
    event['response']['privateChallengeParameters'] = secretLoginCode 
    
    # Add the secret login code to the session so it is available
    # in a next invocation of the "Create Auth Challenge" trigger
    event['response']['challengeMetadata'] = "CODE-{}",format(secretLoginCode)
    
    print('event_out: {}'.format(json.dumps(event)))
    return event


def sendEmail(emailAddress, secretLoginCode):

    dataTxt = "Your secret login code: {}".format(secretLoginCode)
    dataHtml = "<html><body><p>This is your secret login code:</p><h3>{}</h3></body></html>".format(secretLoginCode)


    boto3.client('ses').send_email(
        Source=SES_FROM_ADDRESS,
        Destination={
            'ToAddresses': [ emailAddress,]
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': dataHtml
                },
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': dataTxt
                }
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Your secret login code'
            }
        }
    )

if localtest:
    handler(event, context)

