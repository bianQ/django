#!/usr/bin/python3

import os
import django
from install import color_print

django_path = django.__path__[0]
alter1 = os.path.join(django_path, 'db/backends/mysql/introspection.py')
alter2 = os.path.join(django_path, 'db/backends/mysql/base.py')

def alter(filename):
    print(filename)
    with open(filename, 'r') as file:
        data = file.read()
        new = data.replace('MySQLdb', 'pymysql')

    with open(filename, 'w') as file:
        file.write(new)

    color_print('修改成功', 'green')

alter(alter1)
alter(alter2)