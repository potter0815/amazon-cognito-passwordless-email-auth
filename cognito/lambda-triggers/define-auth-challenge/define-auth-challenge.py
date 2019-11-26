import json


def handler(event, context):
    print('event_in: {}'.format(json.dumps(event)))

    if event['request']['session'] and len(event['request']['session']) >= 3 and event['request']['session'][0]['challengeResult'] == False:
        #event['request']['session'].slice(-1)[0].challengeResult == False:
        #// The user provided a wrong answer 3 times; fail auth
        event['response']['issueTokens'] = False
        event['response']['failAuthentication'] = True
    elif event['request']['session'] and len(event['request']['session']) and event['request']['session'][0]['challengeResult'] == True:
        #// The user provided the right answer; succeed auth
        event['response']['issueTokens'] = True
        event['response']['failAuthentication'] = False
    else: 
        #// The user did not provide a correct answer yet; present challenge
        event['response']['issueTokens'] = False
        event['response']['failAuthentication'] = False
        event['response']['challengeName'] = 'CUSTOM_CHALLENGE'

    print('event_out: {}'.format(json.dumps(event)))

    return event


