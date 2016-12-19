#django
网站内容待更新。。。

##开始部署
**默认你的系统为CentOS 7(不包括)以下版本**

####下载到本地
    su - root
      
    yum install -y git  
      
    git clone https://github.com/bianQ/django.git  
    
####安装python及依赖库
>部署脚本统一放在DjangoSetup目录下  

    sh setup_python.sh
    
####运行安装脚本
>根据提示安装

    python3 install.py
    
>测试django

    切换到django_project目录  
      
    cd ../django_project/  
      
    rm -f blog/migrations/0001_initial.py  
      
    python3 manage.py makemigrations  
      
    python3 manage.py migrate  
      
    python3 manage.py runserver $ip:$port  #写本机IP及自定义端口号
    
打开浏览器访问，例如: http://127.0.0.1:8000

####uWSGI

>安装uwsgi

    pip3 install uwsgi  
    
>配置uwsgi

在项目根目录下创建blog.ini    

chdir后面是django_project的路径，与manage.py同一目录  

socket用来跟本地nginx通信

    [uwsgi]  
    socket = 127.0.0.1:8006  
    chdir = /$PATH/to/django_project/
    wsgi-file = django_project/wsgi.py
    processes = 4
    threads = 2

>测试

    uwsgi blog.ini
    
打开浏览器访问http://127.0.0.1:8006  

现在还不能读取到django的static文件，所以会看到没有CSS的原始网页
####Nginx

>安装nginx

安装 pcre

    wget https://sourceforge.net/projects/pcre/files/pcre/8.39/pcre-8.39.tar.gz 
      
    tar -zxvf pcre-8.39.tar.gz  
      
    cd pcre-8.39  
      
    ./configure  
      
    make  
      
    make install
      
安装nginx
      
    wget http://nginx.org/download/nginx-1.10.2.tar.gz  
      
    tar -zxvf nginx-1.10.2.tar.gz  
      
    cd nginx-1.10.2  
      
    ./configure --prefix=/usr/local/nginx  
      
    make  
      
    make install
      
运行测试nginx，记得关闭防火墙，然后访问本机ip，会出现nginx的欢迎页

    /usr/local/nginx/sbin/nginx
    
如有报错

    /usr/local/nginx/sbin/nginx: error while loading shared libraries: libpcre.so.1: cannot open shared object file: No such file or directory

解决方法
    
    64位系统：
      
    ln -s /usr/local/lib/libpcre.so.1 /lib64
      
    32位系统：
      
    ln -s /usr/local/lib/libpcre.so.1 /lib
    
>配置nginx

    vim /usr/local/nginx/conf/nginx.conf
      
    server {
        listen       80;                          #开放端口号
        server_name  $ip;                         #被访问的ip或域名
   
        
        location / {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:8006;            #对应uwsgi的socket
        }

        location ^~/static/ {
            alias $path/django_project/static/;  #path改为项目的存放目录，例如：/home/test/
        }
    }
    
检查语法，没有错误就返回ok

    /usr/local/nginx/sbin/nginx -t
    

####启动django

***切换路径，path改为项目的存放目录，例如：/home/test/***

    cd $path/django_project/
>生成static文件到项目根路径

    python3 manage.py collectstatic

>修改django配置文件

    vim django_project/settings
      
    找到 DOMAIN = 'http://127.0.0.1:8000'
      
    修改成对应ip/域名及端口号
    
>后台运行uwsgi

    nohup uwsgi blog.ini &

>重启nginx

    /usr/local/nginx/sbin/nginx -s reload
    
####部署完成

打开浏览器，输入对应的ip/域名及端口号即可访问网站