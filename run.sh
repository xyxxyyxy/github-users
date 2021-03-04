#!/bin/bash

python3 -m pip install -r requirements.txt
python3 seed.py
export FLASK_APP=server.py
flask run