#!/bin/bash
IMAGE_NAME=gitlab-auto-approve
IMAGE_RELEASE_TAG=latest
IMAGE_RELEASE_NAME=$IMAGE_NAME:$IMAGE_RELEASE_TAG

read -p 'Docker hub username: ' username
stty -echo
read -p 'Docker hub password: ' password; echo
stty echo

REGISTRY_IMAGE_NAME=$username/$IMAGE_RELEASE_NAME

echo $password | docker login -u $username --password-stdin
docker tag $IMAGE_NAME $REGISTRY_IMAGE_NAME
docker push $REGISTRY_IMAGE_NAME
docker logout