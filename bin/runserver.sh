#!/bin/bash

APP_PATH=/opt/pr
ENV_PATH=$APP_PATH/prenv
APP_ROOT=$APP_PATH/power_recruiter

cd $ENV_PATH
. ./bin/activate

cd $APP_ROOT
PYTHONPATH="/usr/lib/python2.7/dist-packages:$PYTHONPATH" ./manage.py runserver 0.0.0.0:80
