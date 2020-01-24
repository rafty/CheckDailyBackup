# CheckDailyBackup
Check if SSM Backup is working properly
## Instructions

These are the deployment steps until the full implementation is complete.


### Parameter description

PROJECTNAME: The name of the system.  
ROLENAME: Classification of instances.  
ENVIRONMENT: The name of the environment.  
YOURNAME: The Bucket name prefix.  


### Set variables

Locally(terminal), run following commands.

```bash
$ PROJECTNAME=ac
$ ENVIRONMENT=dev
$ YOURNAME=hoge
```


### Create Lambda Functions & CloudWatch Events

__Install python package.__
```bash
$ cd lambda/layer/python
$ pip install -r requirements.txt -t .
$ cd ../../..
```

__Create a bucket to upload lambda functions.__
```bash
$ aws s3 mb s3://$YOURNAME-$PROJECTNAME
```

```bash
$ aws cloudformation package \
    --template-file template.yml \
    --s3-bucket $YOURNAME-$PROJECTNAME \
    --output-template-file packaged.yml

$ aws cloudformation deploy \
    --stack-name $PROJECTNAME-$ENVIRONMENT-Lambda-check-SSMBackup \
    --region ap-northeast-1 \
    --template-file packaged.yml \
    --capabilities CAPABILITY_NAMED_IAM \
    --output text
```
