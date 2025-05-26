#!/bin/bash
exec > /var/log/user-data.log 2>&1
set -x

sudo apt update -y

# AWS INSTALL

sudo apt install unzip -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# PYENV INSTALL

# curl -fsSL https://pyenv.run | bash

# echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
# echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
# echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc

# echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
# echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
# echo 'eval "$(pyenv init - bash)"' >> ~/.profile

# NGINX INSTALL

sudo apt install nginx -y

# after setup and configuration

sudo service nginx restart

# GITHUB REPO CLONING

sudo apt install jq -y

cd /home/ubuntu

# export GITHUB_TOKEN=$(aws secretsmanager get-secret-value --secret-id github_token_new --query SecretString --output text | jq -r ".github_token_new")
# export DB_USERNAME=$(aws secretsmanager get-secret-value --secret-id merch_api_db_credentials --query SecretString --output text | jq -r ".db_username")
# export DB_PASSWORD=$(aws secretsmanager get-secret-value --secret-id merch_api_db_credentials --query SecretString --output text | jq -r ".db_password")

sudo -u ubuntu git clone https://${GITHUB_TOKEN}@github.com/AbbyAdj/cloud-picture-album-api.git

# EXPORT .ENV VARIABLES

# TO BE IMPLEMENTED

cd cloud-picture-album-api

touch .env

echo DB_PORT=${DB_PORT} >> .env
echo DB_USER=${DB_USERNAME} >> .env
echo DB_HOST=${DB_ENDPOINT} >> .env
echo DB_DATABASE=${DB_DATABASE} >> .env
echo DB_PASSWORD=${DB_PASSWORD} >> .env
    

# DATABASE SETUP

sudo apt install postgresql -y

psql "host=${DB_ENDPOINT} port=${DB_PORT} dbname=${DB_DATABASE} user=${DB_USERNAME} password=${DB_PASSWORD} sslmode=require" -f /home/ubuntu/cloud-picture-album-api/src/data/setup-database.sql


# GET SERVER UP AND RUNNING

# sudo apt install make

sudo apt install python3-venv -y

cd cloud-picture-album-api

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


# SETUP SYSTEM SERVICE

cat <<EOF > /etc/systemd/system/fastapi.service
[Unit]
Description=FastAPI app
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/cloud-picture-album-api
ExecStart=/home/ubuntu/cloud-picture-album-api/venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF


systemctl daemon-reload
systemctl enable fastapi
systemctl start fastapi

# nginx setup
cat <<EOF > /etc/nginx/sites-available/fastapi
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF


ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

