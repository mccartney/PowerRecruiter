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

echo "activating virtualenv"
. ./bin/activate

pip install -r $REQ_PATH

echo "current directory $(APP_ROOT)"
cd $APP_ROOT
echo "moving old database to pr.db.backup.$(date +%s) if exists"
mv -f $APP_ROOT/pr.db $APP_ROOT/pr.db.backup.$(date +%s)
echo "running migrations"
$APP_ROOT/manage.py makemigrations
echo "synchronizing database"
echo 'no' | $APP_ROOT/manage.py syncdb
echo "loading fixtures"
$APP_ROOT/manage.py loaddata graph
$APP_ROOT/manage.py loaddata admin

echo "starting service"
service power-recruiter start
