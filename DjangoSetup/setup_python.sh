#!/bin/bash

yum install -y gcc python-devel zlib-devel openssl-devel
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
wget https://pypi.python.org/packages/dc/37/f01d823fd312ba8ea6c3aea906d2d6ac9e9e8bf9e7853e34f296e94b0d0d/setuptools-32.0.0.tar.gz#md5=e5f513a5b53e843b361d663feec4f5fa --no-check-certificate
wget https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-9.0.1.tar.gz#md5=35f01da33009719497f01a4ba69d63c9 --no-check-certificate
tar -zxvf Python-3.5.2.tgz
tar -zxvf setuptools-32.0.0.tar.gz
tar -zxvf pip-9.0.1.tar.gz
cd Python-3.5.2
./configure --prefix=/usr/local/python3.5
make
make install
ln -s /usr/local/python3.5/bin/python3 /usr/bin/python3
cd ../setuptools-32.0.0
python3 setup.py install
cd ../pip-9.0.1
python3 setup.py install
ln -s /usr/local/python3.5/bin/pip3 /usr/bin/pip3
cd ..
rm -rf Python-3.5.2*
rm -rf setuptools-32.0.0*
rm -rf pip-9.0.1*
echo 开始安装python依赖库
pip3 install -r requirements.txt