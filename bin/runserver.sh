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
ENV_PATH=$APP_PATH/prenv
APP_ROOT=$APP_PATH/power_recruiter

cd $ENV_PATH
. ./bin/activate

cd $APP_ROOT
./manage.py runserver 0.0.0.0:4080
