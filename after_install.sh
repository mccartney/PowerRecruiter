#!/bin/bash

APP_PATH=/opt/pr
APP_ROOT=$APP_PATH/power_recruiter
ENV_PATH=$APP_PATH/prenv
REQ_PATH=$APP_PATH/requirements.txt
BIN_PATH=$APP_PATH/bin

cp $APP_PATH/power-recruiter.conf /etc/init

virtualenv $ENV_PATH

cd $ENV_PATH
cp /usr/lib/python2.7/dist-packages/cv* ./lib/python2.7/site-packages/

. ./bin/activate

pip install -r $REQ_PATH

cd $APP_ROOT
rm $APP_ROOT/pr.db
$APP_ROOT/manage.py makemigrations
echo 'no' | sudo $APP_ROOT/manage.py syncdb
sudo $APP_ROOT/manage.py loaddata graph
sudo $APP_ROOT/manage.py loaddata admin

service power-recruiter start
