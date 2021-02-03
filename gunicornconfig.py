command = '/var/www/project/face_recognition_test/venv/bin/gunicorn'
pythonpath = '/var/www/project/face_recognition_test'
bind = '0.0.0.0:8001'
workers = 5
user = 'www'
limit_request_fields = 32000
limit_request_field_size = 0
row_env = 'DJANGO_SETTINGS_MODULE=src.settings'

