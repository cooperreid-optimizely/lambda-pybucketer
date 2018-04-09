# Lambda Python Bucketer 
> Using Optimizely Python SDK v1.4

The Python bucketer is a lambda function exposed via an https AWS API Gateway that takes an array of parameters and returns the variation_key that the visitor was bucketed into. 

_input_
```
https://aws-api-gateway-address.amazonaws.com/prod/bucketer?  
  e=checkout_flow_experiment
  &u=cooper34523569
  &a=tier:"platinum",member_since_days:56
  &debug=1
```

_response_
```
{
  "variation": "one_step_checkout",
  "user": "cooper34523569",
  "experiment": "checkout_flow_experiment",
  "debug": {
    "project_id": "10000000000",
    "account_id": "80000000000",
    "time": "2018-04-09 17:06:02.698754",
    "datafile": {
      "url": "https://cdn.optimizely.com/PATH/TO/DATAFILE.json",
      "revision": "22"
    },
    "user_attributes": {
      "tier": "platinum",
      "member_since_days": 56
    }
  }
}
```

### Bucketing Parameters

| parameter | name   | details                                            | required | default |
|-----------|--------|----------------------------------------------------|----------|---------|
| e       | experiment_key | Pass the experiment_key in as a string | yes      |     null    |
| u      | user_id  | Pass the userId in as a string. If no userId is provided, the userId will default to the visitors IP address                      | no      |    IP address    |
| a      | attributes  | A list of user attributes used for `activate`. These will be passed into the activate call, and can be used to qualify users for Audience and for Results segmentation.                      | no      |    {}    |
| debug      | debug mode  | Enabled debug mode. The response will show additional data, including accountId, projectId, and verbose datafile characteristics                      | no      |    False    |

### Datafile Management

The Optimizely Full SDKs require the consumption of the project's [JSON datafile](https://developers.optimizely.com/x/solutions/sdks/reference/index.html?language=python#datafile) in order to be informed of the experiment settings configured within Optimizely. 

**Current state**

Running the `webhook.py` script will fetch the datafile contents and store them within `datafile.py`. The core Lambda function file, `app.py` imports `datafile.py` and uses its contents to instantiate the `Optimizely Client`. After you've updated the datafile contents using the webhook, you'll need to manually push the code package up to Lambda. 

In order to inform `webhook.py` where the datafile lives, you must set your datafile url as an environment variable:
```
$ export DATAFILE_URL="https://cdn.optimizely.com/PATH/TO/FULLSTACK/DATAFILE.json"
```
**Future state**

Future versions of this tool will do one of the following
* Include an additional Lambda function that will serve as a webhook that will fetch a fresh copy of the datafile, and update the code package of the Bucketer lambda function.
* Include an additional Lambda function that will serve as a webhook that will fetch a fresh copy of the datafile and push it into an S3 bucket. The Bucketer lambda function would then have to access the datafile contents via a `Boto` S3 connection, which may not be performant.

### Updating your Lambda function code

Flatten everything into a lambda-friendly zip

`./build.sh`

Push the code to your lambda function

`aws lambda update-function-code --function-name BUCKETERFNC --zip-file fileb://package.zip --profile AWSPROFILENAME`
