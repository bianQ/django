#!/bin/bash

host=$1
user=$2
password=$3
name=$4

cd ../django_project/django_project/
sed -i -e "/^DATABASES/,/^\}/s/'HOST': '127.0.0.1'/'HOST': '${host}'/g" settings.py
sed -i -e "/^DATABASES/,/^\}/s/'USER': 'root'/'USER': '${user}'/g" settings.py
sed -i -e "/^DATABASES/,/^\}/s/'PASSWORD': 'root'/'PASSWORD': '${password}'/g" settings.py
sed -i -e "/^DATABASES/,/^\}/s/'NAME': 'django'/'NAME': '${name}'/g" settings.py