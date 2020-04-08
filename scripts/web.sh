#!/bin/bash

. ./deploy.ini

cd $BASE_DIR;

docker cp containers/nlp-web/templates/index.html containers_nlp-web_1:/app/templates/index.html;
