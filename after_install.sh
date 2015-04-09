#!/bin/bash

ENV_PATH=/opt/pr/prenv
REQ_PATH=/opt/pr/requirements.txt

virtualenv $ENV_PATH
/bin/bash -c "source "$ENV_PATH"/bin/activate; pip install -r "$REQ_PATH
