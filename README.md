## AWS X-Ray Serverless Samples

The samples in this repository demonstrate different ways to integrate AWS X-Ray within a serverless application.

* **xray**: Simple tracing without code instrumentation.
* **xray-instrumented**: AWS X-Ray tracing with code instrumentation.
* **xray-instrumented-layers**: AWS X-Ray tracing with code instrumentation where the X-Ray Python SDK is provided by a Lambda Layer.
* **xray-no-lambda**: AWS X-Ray tracing for an API Gateway without a Lambda function.
* **boilerplate**: Contains a template for a SAM project with X-Ray tracing enabled.

The **pipeline** folder contains an AWS CloudFormation template for a pipeline using AWS CodeCommit, AWS CodePipeline and AWS CodeBuild.

The **helpers** folder contains script to help deploy Serverless applications locally and run calls against API Gateway.

## Usage

### 1. Deploy

To deploy any sample, go to the sample folder and run the following commands:

```
export S3_BUCKET="<your artifact bucket>"
make
```

### 2. Send test traffic

To send test traffic for a particular sample, run this command in the sample folder:

```
make calls
```

By default, this will send 10 PUT requests and 500 GET requests.

### 3. Check traces

After sending test traffic, you can check traces and the service map in the [AWS Console](https://console.aws.amazon.com/xray/home).

### 4. Cleanup

To tear down resources, run this command in the sample folder:

```
make delete
```

### Deploy all samples

You can deploy and make calls to all samples at once using the following commands from the root of this repository:

```
export S3_BUCKET="<your artifact bucket>"
# Deploy all samples
./helpers/deploy_all.sh
# Send requests to all samples
./helpers/calls_all.sh
```

Once you are done experimenting, you can delete all resources with the following command:

```
./helpers/delete_all.sh
```

### Deploy all samples with CI/CD pipelines

To deploy all samples in CI/CD pipelines, run the following commands from the root of this repository:

```
export S3_BUCKET="<your artifact bucket>"
# Deploy all samples
./helpers/deploy_all_pipeline.sh
# Send requests to all samples
./helpers/calls_all_pipeline.sh
```

Once you are done experimenting, you can delete all resources with the following command:

```
./helpers/delete_all_pipeline.sh
```

## Requirements

The samples require these programs to be installed on your computer:

* [AWS Command Line Interface](https://aws.amazon.com/cli/)
* [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Docker](https://docs.docker.com/install/)
* [Go](https://golang.org/dl/)
* [Python 3](https://www.python.org/downloads/)

You would also need to install the [cfn_flip](https://github.com/awslabs/aws-cfn-template-flip) package for Python3. You can install it with Pip by running `python3 -m pip install cfn_flip`.

## Troubleshooting

### I keep getting "socket: too many open files" errors when running "make calls"

The **get** program triggers 500 HTTP calls by default, which can exceed the default limit of open file descriptors. You can increase this limit by running `ulimit -n 4096`, which should be enough for the default case.

To learn more about this, check the ulimit help by typing `help ulimit` or the man page for `limits.conf`.

## License Summary

This sample code is made available under the MIT-0 license. See the LICENSE file.
