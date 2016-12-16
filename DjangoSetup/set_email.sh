#!/bin/bash

host=$1
host_user=$2
password=$3
port=$4

cd ../django_project/django_project/
sed -i -e "/^EMAIL_HOST/,/^EMAIL_USE_SSL/s/EMAIL_HOST = 'smtp.163.com'/EMAIL_HOST: '${host}'/g" settings.py
sed -i -e "/^EMAIL_HOST/,/^EMAIL_USE_SSL/s/EMAIL_HOST_USER = '15989490620@163.com'/EMAIL_HOST_USER: '${host_user}'/g" settings.py
sed -i -e "/^EMAIL_HOST/,/^EMAIL_USE_SSL/s/EMAIL_HOST_PASSWORD = os.environ.get('PASSWORD')/EMAIL_HOST_PASSWORD: '${password}'/g" settings.py
sed -i -e "/^EMAIL_HOST/,/^EMAIL_USE_SSL/s/EMAIL_PORT = 465/EMAIL_PORT: '${port}'/g" settings.py