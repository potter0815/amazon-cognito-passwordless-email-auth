
import boto3
import secrets
import os
import json
import string

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
        alphabet = string.digits
        secretLoginCode = ''.join(secrets.choice(alphabet) for i in range(6))  
        sendEmail(event['request']['userAttributes']['email'], secretLoginCode)
    else:
        # There's an existing session. Don't generate new digits but
        # re-use the code from the current session. This allows the user to
        # make a mistake when keying in the code and to then retry, rather
        # the needing to e-mail the user an all new code again.    
        previousChallenge = event['request']['session'][0]  
        secretLoginCode = previousChallenge['challengeMetadata'][5:11]       

    # This is sent back to the client app
    event['response']['publicChallengeParameters'] = { 'email': event['request']['userAttributes']['email'] }

    # Add the secret login code to the private challenge parameters
    # so it can be verified by the "Verify Auth Challenge Response" trigger
    event['response']['privateChallengeParameters'] = secretLoginCode 
    
    # Add the secret login code to the session so it is available
    # in a next invocation of the "Create Auth Challenge" trigger
    event['response']['challengeMetadata'] = f"CODE-{secretLoginCode}"
    
    print(f'event_out: {json.dumps(event)}')
    return event


def sendEmail(emailAddress, secretLoginCode):

    boto3.client('ses').send_email(
        Source=SES_FROM_ADDRESS,
        Destination={
            'ToAddresses': [ emailAddress,]
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': f"<html><body><p>This is your secret login code:</p><h3>{secretLoginCode}</h3></body></html>"
                },
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': f"Your secret login code: {secretLoginCode}"
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

