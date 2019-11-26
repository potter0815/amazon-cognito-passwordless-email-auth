import json

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    event['response']['autoConfirmUser'] = True
    event['response']['autoVerifyEmail'] = True
    return event
    
