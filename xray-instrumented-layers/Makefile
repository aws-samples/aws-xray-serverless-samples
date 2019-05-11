ENVIRONMENT ?= dev
STACK_NAME ?= sample-xray-instrumented-layers-$(ENVIRONMENT)

all: build package deploy

# Build
CODEBUILD_START_TIME ?= "FALSE"
ifeq ($(CODEBUILD_START_TIME),"FALSE")
	BUILD_MODE=build-local
else
	BUILD_MODE=build-codebuild
endif

build: $(BUILD_MODE)

build-codebuild:
	mkdir -p ./layers/build/xray/python/
	$(MAKE) -C layers

build-local:
	mkdir -p ./layers/build/xray/python/
	docker run -v $(PWD)/layers:/var/task lambci/lambda:build-python3.7 make

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
local: build
	$(eval TABLE_NAME=$(shell aws cloudformation describe-stacks --stack-name $(STACK_NAME) --query 'Stacks[0].Outputs[?OutputKey==`TableName`].OutputValue' --output text))
	python3 ../helpers/gen_env.py TABLE_NAME=$(TABLE_NAME) > env.json
	@echo "Environment variables:"
	@cat env.json
	sam local start-api --template template.yml -n env.json

# Delete
delete:
	aws cloudformation delete-stack --stack-name $(STACK_NAME)
	aws cloudformation wait stack-delete-complete --stack-name $(STACK_NAME)
