Deployment Pipeline
===================

This folder contains a CloudFormation template to deploy an AWS CodePipeline pipeline for the various examples contained in this repository.

To deploy a pipeline, you need to first create a repository in AWS CodeCommit and push one of the `xray-*` folders to this repository.

After that, run the following command to deploy the pipeline:

```
export S3_BUCKET="(name of an S3 bucket for code artifacts)"
export REPOSITORY_NAME="(name of your repository in AWS CodeCommit)"
make
```
