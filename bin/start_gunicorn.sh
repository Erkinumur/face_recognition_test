#!/bin/bash
source /root/project/venv/bin/activate
exec gunicorn -c "/var/www/project/face_recognition_test/gunicornconfig.py" src.wsgi
