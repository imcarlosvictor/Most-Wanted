#!/bin/bash

# Build the project
echo "Building the project..."
python3.9 -m pip install -r requirements.txt

echo "Make Migration..."
python3.9 mysite/manage.py makemigrations --noinput
python3.9 mysite/manage.py migrate --noinput

echo "Collect Static..."
python3.9 mysite/manage.py collectstatic --noinput --clear
