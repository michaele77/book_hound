#!/usr/bin/env python3

from aws_cdk import core

from aws_lambda_scraper.aws_lambda_scraper_stack import AwsLambdaScraperStack


app = core.App()
AwsLambdaScraperStack(app, "aws-lambda-scraper")

app.synth()
