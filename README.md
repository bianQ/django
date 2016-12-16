#django



##开始部署




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
    
####配置uWSGI

####待更新...