#!/bin/bash

# Install the database
apt -y install mariadb-server

# Enable and start MariaDB service
systemctl enable mariadb
systemctl start mariadb

# Set MySQL root password
mysqladmin -u root password "P@ssw0rd"

# Create database and user
mysql -u root -p"P@ssw0rd" -e "CREATE DATABASE demodb;"
mysql -u root -p"P@ssw0rd" -e "CREATE USER 'demouser'@'localhost' IDENTIFIED BY 'Passw0rd';"
mysql -u root -p"P@ssw0rd" -e "GRANT ALL PRIVILEGES ON demodb.* TO 'demouser'@'%' IDENTIFIED BY 'Passw0rd';"
mysql -u root -p"P@ssw0rd" -e "FLUSH PRIVILEGES;"

# Allow remote connections by binding to all addresses
echo "bind-address = 0.0.0.0" >> /etc/mysql/mariadb.conf.d/50-server.cnf

# Restart MariaDB service to apply changes
systemctl restart mariadb

# Stop the firewall (assuming you're using ufw)
systemctl stop ufw