# Lambda Python Bucketer 
> Using Optimizely Python SDK v1.4

### Updating your Lambda function code

Flatten everything into a lambda-friendly zip

`./build.sh`

Push the code to your lambda function

`aws lambda update-function-code --function-name BUCKETERFNC --zip-file fileb://package.zip --profile AWSPROFILENAME`
