#!/usr/bin/python3

import shlex
import time
from smtplib import SMTP, SMTP_SSL
import pymysql


def bash(cmd):
    return shlex.os.system(cmd)

def color_print(msg, color='red'):
    color_msg = {'blue': '\033[1;36m%s\033[0m',
                 'green': '\033[1;32m%s\033[0m',
                 'yellow': '\033[1;33m%s\033[0m',
                 'red': '\033[1;31m%s\033[0m',
                 'title': '\033[30;42m%s\033[0m',
                 'info': '\033[32m%s\033[0m'}
    msg = color_msg.get(color, 'red') % msg
    print (msg)

class Setup(object):
    def __init__(self):
        self.db_host = '127.0.0.1'
        self.db_user = 'root'
        self.db_passwd = 'root'
        self.db = 'django'
        self.mail_host = ''
        self.mail_host_user = ''
        self.mail_port = 465
        self.mail_passwd = ''
        self.mail_SSL = True

    @staticmethod
    def check_bash(ret_code, error_msg):
        if ret_code != 0:
            color_print(error_msg)
            exit()

    def _setup_mysql(self):
        color_print('开始安装设置mysql (请手动设置mysql安全)', 'green')
        color_print('默认用户名: %s 默认密码: %s' % (self.db_user, self.db_passwd), 'green')
        ret_code = bash('yum install -y mysql-server')
        self.check_bash(ret_code, "安装mysql失败, 请检查安装源是否更新或手动安装！")
        bash('service mysqld start')
        bash('chkconfig mysqld on')
        bash('mysql -e "create database %s default charset=utf8"' % self.db)
        bash('mysql -e "grant all on %s.* to \'%s\'@\'%s\' identified by \'%s\'"' % (self.db, self.db_user, self.db_host, self.db_passwd))
        bash('mysqladmin -u %s password %s' % (self.db_user, self.db_passwd))

    def _set_env(self):
        color_print('开始关闭防火墙和selinux', 'green')
        bash('service iptables stop && chkconfig iptables off && setenforce 0')

    def _input_mysql(self):
        while True:
            mysql = input('是否安装新的MySQL服务器? [y/n]:')
            if mysql != 'n':
                self._setup_mysql()
            else:
                color_print('要是不知道如何设置，就按Enter使用默认值!', 'yellow')
                db_host = input('请输入数据库服务器IP [127.0.0.1]: ').strip()
                db_user = input('请输入数据库服务器用户 [root]: ').strip()
                db_passwd = input('请输入数据库服务器密码 [root]: ').strip()
                db = input('请输入使用的数据库 [django]: ').strip()

                if db_host:
                    self.db_host = db_host
                if db_user:
                    self.db_user = db_user
                if db_passwd:
                    self.db_passwd = db_passwd
                if db:
                    self.db = db
                color_print('安装程序将在5秒后自动创建%s数据库', 'green')
                time.sleep(5)
                bash('mysql -u %s -p%s -e "create database %s default charset=utf8"' % (self.db_user, self.db_passwd, self.db))
                bash('mysql -u %s -p%s -e "grant all on %s.* to \'%s\'@\'%s\' identified by \'%s\'"' % (self.db_user, self.db_passwd,
                self.db, self.db_user, self.db_host, self.db_passwd))
                color_print('开始写入django配置文件', 'green')
                bash('sh set_mysql.sh %s %s %s %s' % (self.db_host, self.db_user, self.db_passwd, self.db))

            if self._test_mysql():
               break

    def _alter_django(self):
        color_print('更改pymysql为django默认mysql连接模块', 'green')
        bash('python3 alter_django.py')

    def _test_mysql(self):
        try:
            pymysql.connect(host=self.db_host, user=self.db_user, passwd=self.db_passwd, db=self.db)
            color_print('连接数据库成功', 'green')
            return True
        except pymysql.OperationalError as e:
            color_print('数据库连接失败 %s' %e, 'red')
            return False

    def _test_mail(self):
        try:
            if self.mail_port == 465:
                smtp = SMTP_SSL(self.mail_host, port=self.mail_port, timeout=2)
            else:
                smtp = SMTP(self.mail_host, port=self.mail_port, timeout=2)
            smtp.login(self.mail_host_user, self.mail_passwd)
            smtp.sendmail(self.mail_host_user, (self.mail_host_user,),
                          '''From:%s\r\nTo:%s\r\nSubject:Piaoke Mail Test!\r\n\r\n  Mail test passed!\r\n''' %
                          (self.mail_host_user, self.mail_host_user))
            smtp.quit()
            return True

        except Exception as e:
            color_print(e, 'red')
            skip = input('是否跳过 [y/n]? : ')
            if skip == 'y':
                return True
            return False

    def _input_smtp(self):
        while True:
            color_print('除了端口号，其它必填!否则后台无法发送验证邮件导致注册失败!!', 'yellow')
            self.mail_host = input('请输入SMTP地址(例如smtp.qq.com): ').strip()
            mail_port = input('请输入SMTP端口(邮箱默认使用SSL加密，更改前自行确认，使用163邮箱可直接Enter跳过) [465]: ').strip()
            self.mail_host_user = input('请输入账户: ').strip()
            self.mail_passwd = input ('请输入授权码，注意不是邮箱密码，是授权码!!!: ').strip()
            if mail_port:
                self.mail_port = int(mail_port)
            if self._test_mail():
                color_print('\n\t请登陆邮箱查收邮件, 然后确认是否继续安装\n', 'green')
                smtp = input('是否保存设置继续安装? [y/n]: ')
                if smtp == 'n':
                    continue
                else:
                    bash('sh set_email.sh %s %s %s %s' % (
                    self.mail_host, self.mail_host_user, self.mail_passwd, self.mail_port))
                    break

    def start(self):
        color_print('安装过程如有疑问，请查看https://github.com/bianQ/django', 'yellow')
        time.sleep(3)
        self._set_env()
        self._input_mysql()
        self._input_smtp()
        self._alter_django()

if __name__ == '__main__':
    setup = Setup()
    setup.start()

