
import boto3
import os
import json

# import secrets
# import string

localtest = False

try:
    LAMBDA_LOCAL_TEST = os.environ['LAMBDA_LOCAL_TEST']
except Exception: 
    localtest = True
    filename = os.getcwd() + "/event.json"
    f = open(filename)
    event = json.loads(f.read())   
    context = ""
    LAMBDA_LOCAL_TEST = True
    

def handler(event, context):

    expectedAnswer = event['request']['privateChallengeParameters']['secretLoginCode']
    if event['request']['challengeAnswer'] == expectedAnswer:
        event['response']['answerCorrect'] = True
    else: 
        event['response']['answerCorrect'] = False
    print(event)
    return event

if LAMBDA_LOCAL_TEST == True:
    handler(event, context)