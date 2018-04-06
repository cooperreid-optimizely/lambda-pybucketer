## Updating your Lambda function code

#### Build the project, flatten everything into a lambda-friendly zip
`./build.sh`

##### Push the code to your lambda function
`aws lambda update-function-code --function-name BUCKETERFNC --zip-file fileb://package.zip --profile AWSPROFILENAME`
