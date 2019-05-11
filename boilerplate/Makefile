ENVIRONMENT ?= dev
STACK_NAME ?= <PUT A DEFAULT STACK NAME HERE>-$(ENVIRONMENT)

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
calls: ;

# Local
local:
	sam local start-api --template template.yml

# Delete
delete:
	aws cloudformation delete-stack --stack-name $(STACK_NAME)
	aws cloudformation wait stack-delete-complete --stack-name $(STACK_NAME)
