#!/bin/bash
# Install php and integrate with MariaDB
dbip="192.168.9.21"
/usr/bin/apt -y install mysql-server apache2 php php7.4-mysql php-common php-gd php-xml php-mbstring  php-xmlrpc unzip wget

# Download PHP files
wget -O /var/www/html/config.php  https://raw.githubusercontent.com/ibrahimmumgit/3Tier/master/app/config.php
wget -O /var/www/html/create.php  https://raw.githubusercontent.com/ibrahimmumgit/3Tier/master/app/create.php
wget -O /var/www/html/delete.php  https://raw.githubusercontent.com/ibrahimmumgit/3Tier/master/app/delete.php
wget -O /var/www/html/error.php  https://raw.githubusercontent.com/ibrahimmumgit/3Tier/master/app/error.php
wget -O /var/www/html/index.php https://raw.githubusercontent.com/ibrahimmumgit/3Tier/master/app/index.php
wget -O /var/www/html/read.php  https://raw.githubusercontent.com/ibrahimmumgit/3Tier/master/app/read.php
wget -O /var/www/html/update.php  https://raw.githubusercontent.com/ibrahimmumgit/3Tier/master/app/update.php

# Modify configuration files
sed -i "s@DBName@demodb@" /var/www/html/config.php
sed -i "s@DBUser@demouser@" /var/www/html/config.php
sed -i "s@DBPassword@Passw0rd@" /var/www/html/config.php
# Note: Variable substitution (like $dbip) won't work in single quotes ('') in Bash, 
# so I'm assuming you've set $dbip elsewhere in your script or environment
sed -i "s@DBServer@$dbip@" /var/www/html/config.php
sed -i "s@HOSTNAME@demo-app@" /var/www/html/index.php

# Download and import MySQL database
wget -O /tmp/employees.sql https://raw.githubusercontent.com/sammcgeown/vRA-3-Tier-Application/master/app/employees.sql
chmod 755 /tmp/employees.sql
mysql -u "demouser" -p"Passw0rd" demodb -h "$dbip" < /tmp/employees.sql

# Configure Apache
sed -i "/^<Directory \"\/var\/www\/html\">/,/^<\/Directory>/{s/AllowOverride None/AllowOverride All/g}" /etc/apache2/apache2.conf

# Enable and start Apache service
systemctl enable apache2
systemctl start apache2

# Stop the firewall (assuming you're managing it with ufw)
systemctl stop ufw