all: build package deploy

build: ;

package: ;

deploy:
	aws cloudformation deploy --template-file template.yml --stack-name $(REPOSITORY_NAME)-pipeline --parameter-overrides RepositoryName=$(REPOSITORY_NAME) ArtifactStore=$(S3_BUCKET) --capabilities CAPABILITY_IAM

delete:
	aws cloudformation delete-stack --stack-name $(REPOSITORY_NAME)-pipeline
	aws cloudformation wait stack-delete-complete --stack-name $(REPOSITORY_NAME)-pipeline
