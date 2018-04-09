# Lambda Python Bucketer 
> Using Optimizely Python SDK v1.4

### What does it do?

The Python bucketer is a lambda function exposed via an https AWS API Gateway that takes an array of parameters and returns the variation_key that the visitor was bucketed into. 

```
https://aws-api-gateway-address.us-east-1.amazonaws.com/prod/bucketer?    
  e=checkout_flow_experiment
  &u=cooper34523569
  &a=tier:"platinum",zip:07020
  &debug=1
```

### Bucketing Parameters

| parameter | name   | details                                            | required | default |
|-----------|--------|----------------------------------------------------|----------|---------|
| e       | experiment_key | Pass the experiment_key in as a string | yes      |     null    |
| u      | user_id  | Pass the userId in as a string. If no userId is provided, the userId will default to the visitors IP address                      | no      |    IP address    |
| a      | attributes  | A list of user attributes used for `activate`. These will be passed into the activate call, and can be used to qualify users for Audience and for Results segmentation.                      | no      |    {}    |
| debug      | debug mode  | Enabled debug mode. The response will show additional data, including accountId, projectId, and verbose datafile characteristics                      | no      |    False    |

### Updating your Lambda function code

Flatten everything into a lambda-friendly zip

`./build.sh`

Push the code to your lambda function

`aws lambda update-function-code --function-name BUCKETERFNC --zip-file fileb://package.zip --profile AWSPROFILENAME`
