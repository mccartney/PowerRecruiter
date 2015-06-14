#!/bin/bash


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
