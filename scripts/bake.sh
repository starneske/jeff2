#!/bin/bash
set -o allexport

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

if [ -e .env ]; then
	source .env
fi
echo $JEFF2_DOCKER_IMAGE_LOCAL

docker build -t $JEFF2_DOCKER_IMAGE_LOCAL:$JEFF2_IMAGE_VERSION . 
