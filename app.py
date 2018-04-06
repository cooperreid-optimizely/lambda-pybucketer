#!/usr/bin/env python

import json
import datetime
from datafile import datafile, datafile_url
from optimizely import optimizely

class BucketingInvalidExeperimentKeyException(BaseException): pass
class BucketingInvalidUserIdException(BaseException): pass

# Initialize an Optimizely client
optimizely_client = optimizely.Optimizely(datafile)
optimizely_client = optimizely.Optimizely(datafile,
                                          skip_json_validation=False)

def respond(err, res=None):
    return {
        'statusCode': '200',
        'body': json.dumps({'error': str(err), 'variation': None}) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def bucket(experiment_key='', user_id=None, attributes=None):
    if not experiment_key:
        raise BucketingInvalidExeperimentKeyException('Invalid experiment_key provided: {}'.format(experiment_key))

    if not user_id:
        raise BucketingInvalidUserIdException('Invalid User ID Provided: {}'.format(user_id))

    variation = optimizely_client.activate(experiment_key, user_id, attributes=attributes)

    log_message = """
    Bucketing decision
        User ID: {}
        Experiment Key: {}
        Variation: {}
    """.format(user_id, experiment_key, variation)
    print(log_message)

    return variation

def parseUserAttr(attrStr):
    attr = {}
    for keypair in attrStr.split(','):
        try:
            attr[keypair.split(':')[0]] = json.loads(keypair.split(':')[1])
        except:
            pass
    return attr

def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.
    '''    
    print('-------------------------')
        
    bucketing_decision = None    
    querystring_params = event["queryStringParameters"] or {}
    user_ip_address    = event['requestContext']['identity']['sourceIp']
    user_id            = querystring_params.get('u', user_ip_address) or user_ip_address
    experiment_key     = querystring_params.get('e', None)
    user_attributes    = parseUserAttr(querystring_params.get('a', "").strip() or "")

    try:
        bucketing_decision = bucket(experiment_key, user_id, user_attributes)
    except BucketingInvalidExeperimentKeyException: 
        pass
    except BucketingInvalidUserIdException: 
        pass        
    except BaseException as err:
        return respond(err)
    else:
        response_body = {
            'variation': bucketing_decision, 
            'user': user_id, 
            'experiment': experiment_key
        }
        debug = querystring_params.get('debug', False)
        if debug:
            datafile_contents = json.loads(datafile)
            response_body['debug'] = {
                'project_id': datafile_contents.get('projectId'),
                'account_id': datafile_contents.get('accountId'),
                'time': str(datetime.datetime.now()),
                'datafile': {
                    'url': datafile_url,
                    'revision': datafile_contents.get('revision'),
                },
                'user_attributes': user_attributes,
            }            
        return respond(None, response_body)

