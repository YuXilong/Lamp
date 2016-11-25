
# created by yuxilong on 2016.11.25
# coding:utf8

import os 
import sys
import time

# PHP7 下载地址
php_url = 'http://cn2.php.net/distributions/php-7.0.13.tar.bz2'

# 开启https配置文件
ssl_content = '''
<VirtualHost *:443>
	#ServerName www.example.com

	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html
	SSLEngine On
	SSLOptions +StrictRequire
	SSLCertificateFile /etc/ssl/certs/server.crt
	SSLCertificateKeyFile /etc/ssl/private/server.key

	#LogLevel info ssl:warn

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	#Include conf-available/serve-cgi-bin.conf
</VirtualHost>
'''
# 重定向http配置文件
rewrite_content = '''
	RewriteEngine on
	RewriteBase /
	RewriteCond %{SERVER_PORT} !^443$
	RewriteRule ^.*$ https://%{SERVER_NAME}%{REQUEST_URI} [L,R]
'''

# 更新添加apt-get源地址
def update_apt():
    print '*********更新源地址*********'
    os.system('apt-get update')
    os.system('apt-get upgrade')
    os.system('apt-get install software-properties-common')

def get_apache2():
    print '*********安装Apache2*********'
    os.system('apt-get install apache2')
    os.system('a2dismod mpm_event')
    os.system('a2enmod mpm_prefork')
    os.system('service apache2 restart')

def get_mysql():
    print '*********安装MySQL*********'
    os.system('wget http://dev.mysql.com/get/mysql-apt-config_0.6.0-1_all.deb')
    os.system('dpkg -i mysql-apt-config_0.6.0-1_all.deb')
    os.system('apt-get install mysql-server')

# 安装PHP7.0
def get_php():
    print '*********安装PHP*********'
    os.system('add-apt-repository ppa:ondrej/php')
    os.system('apt-get install software-propert')
    os.system('sudo apt-get update')
    os.system('apt-get install php7.0')
    os.system('apt-get install libapache')
    print '*********正在重启Apache2*********'
    os.system('/etc/init.d/apache2 restart')
    print '*********重启完成*********'

# 开启https
def open_ssl():
    print '*********正在安装https依赖*********'
    os.system('a2enmod ssl')
    os.system('apt-get install openssl')
    os.system('openssl genrsa -des3 -out server.key 1024')
    os.system('openssl req -new -key server.key -out server.csr')
    os.system('openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt')
    os.system('cp server.crt /etc/ssl/certs')
    os.system('cp server.key /etc/ssl/private')
    os.system('cp /etc/apache2/sites-enabled/000-default /etc/apache2/sites-enabled/001-ssl')
    print '*********正在配置https*********'
    fp = open('/etc/apache2/sites-enabled/001-ssl.conf','wr')
    fp.write(ssl_content)
    fp.close()
    
    config_https()

# 重定向http请求
def  config_https():
    print '*********正在配置http重定向https*********'
    file_path = '/etc/apache2/apache2.conf'
    fp = open(file_path,'r')
    content = fp.readlines()
    fp.close()

    fp = open(file_path,'w')

    content.insert(167,rewrite_content)

    fp.writelines(content)
    fp.close()
    os.system('a2enmod rewrite')
    print '*********正在重启Apache2*********'
    os.system('/etc/init.d/apache2 force-reload')
    os.system('/etc/init.d/apache2 restart')
    print '*********重启完成*********'

def claen_file():
    print '*********正在清除临时文件*********'
    os.system('rm -r *')
    print '*********清除临时文件成功*********'

def creat_test():

    php_info = '''
    <?php
        echo phpinfo();
    ?>
    '''

    fp = open('/var/www/html/test.php','wr')
    fp.write(php_info)
    fp.close()

if __name__ == '__main__':

    start_time = time.time()

    update_apt()

    get_apache2()

    get_mysql()

    get_php()

    # 是否需要开启https 如不需要开启则注释下面两行
    open_ssl()

    creat_test()

    claen_file()

    end_time = time.time()

    use_time = end_time - start_time

    print '安装共用时：%d分%d秒,你可以访问网站根目录的test.php来确认安装是否成功' % (use_time / 60, use_time % 60)






