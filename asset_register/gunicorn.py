from os import getenv

bind = f":{getenv('GUNICORN_PORT', 9000)}"
workers = 1
threads = 2
accesslog = '-'
errorlog = '-'
