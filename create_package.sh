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


fpm -s dir -t deb -n power-recruiter -v 1.0.0 \
    -C . \
    -d "python (>=2.7)" \
    -d "python-pip" \
    -d "python-opencv" \
    -d "libjpeg-dev" \
    -d "python-dev" \
    -d "build-essential" \
    -d "python-virtualenv" \
    -d "gfortran" \
    -d "libopenblas-dev" \
    -d "liblapack-dev" \
    --prefix /opt/pr \
    --after-install after_install.sh \
    --after-upgrade after_upgrade.sh \
    --before-remove before_remove.sh \
    -m "Filip Ochnik <filip.ochnik@gmail.com>" \
    power_recruiter/power_recruiter/candidate \
    power_recruiter/power_recruiter/basic_site \
    power_recruiter/power_recruiter/tests \
    power_recruiter/power_recruiter/image_comparator/*.py \
    power_recruiter/power_recruiter/image_comparator/network.bin \
    power_recruiter/power_recruiter/*.py \
    power_recruiter/*.sh \
    power_recruiter/*.py \
    requirements.txt bin power-recruiter.conf
