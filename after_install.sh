#!/bin/bash

#Power Recruiter - a browser-based FSM-centered database application profiled for IT recruiters
#Copyright (C) 2015 Krzysztof Fudali, Andrzej Jackowski, Cezary Kosko, Filip Ochnik
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
