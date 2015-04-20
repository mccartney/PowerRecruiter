#!/bin/bash


fpm -s dir -t deb -n power-recruiter -v 0.9.0 \
    -C . \
    -d "python (>=2.7)" \
    -d "python-pip" \
    -d "python-dev" \
    -d "build-essential" \
    -d "python-virtualenv" \
    --prefix /opt/pr \
    --after-install after_install.sh \
    --after-upgrade after_upgrade.sh \
    -m "Filip Ochnik <filip.ochnik@gmail.com>" \
    power_recruiter requirements.txt bin power-recruiter.conf
