ENVIRONMENT ?= dev
STACK_NAME ?= sample-xray-no-lambda-$(ENVIRONMENT)

all: build package deploy

# Build
build: ;

# Package
package:
	sam package --s3-bucket $(S3_BUCKET) --template-file template.yml --output-template-file template-output.yml

# Deploy
deploy:
	sam deploy --template-file template-output.yml --stack-name $(STACK_NAME) --capabilities CAPABILITY_IAM

# Calls
calls:
	go run ../helpers/put.go $(shell aws cloudformation describe-stacks --stack-name $(STACK_NAME) --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' --output text)
	go run ../helpers/get.go $(shell aws cloudformation describe-stacks --stack-name $(STACK_NAME) --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' --output text)

# Local
# Not supported by AWS SAM as there is no AWS Lambda function defined in this stack
local: ;

# Delete
delete:
	aws cloudformation delete-stack --stack-name $(STACK_NAME)
	aws cloudformation wait stack-delete-complete --stack-name $(STACK_NAME)
