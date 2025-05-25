#!/bin/sh

REGION="ap-northeast-1"

aws cloudformation create-stack --stack-name ${1} --template-body file://${1}.yml --parameters=file://./params/${1}.param.json --region $REGION
