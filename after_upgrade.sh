#!/bin/bash

APP_PATH=/opt/pr
APP_ROOT=$APP_PATH/power_recruiter
ENV_PATH=$APP_PATH/prenv
REQ_PATH=$APP_PATH/requirements.txt
BIN_PATH=$APP_PATH/bin

mv $APP_PATH/power-recruiter.conf /etc/init

cd $ENV_PATH
. ./bin/activate

pip install -r $REQ_PATH

cd $APP_ROOT
$APP_ROOT/manage.py makemigrations
$APP_ROOT/manage.py migrate

service power-recruiter restart
