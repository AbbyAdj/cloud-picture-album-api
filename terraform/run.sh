# !/bin/bash

sudo apt update -y

# AWS INSTALL

sudo apt install unzip
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# PYENV INSTALL

curl -fsSL https://pyenv.run | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
echo 'eval "$(pyenv init - bash)"' >> ~/.profile

# NGINX INSTALL

sudo apt install nginx -y

# after setup and configuration

sudo service nginx restart

# GITHUB REPO CLONING

cd /home/ubuntu

export GITHUB_TOKEN=$(aws secretsmanager get-secret-value --secret-id github_token_new --query SecretString --output text | jq -r ".github_token_new")
export DB_USERNAME=$(aws secretsmanager get-secret-value --secret-id merch_api_db_credentials --query SecretString --output text | jq -r ".db_username")
export DB_PASSWORD=$(aws secretsmanager get-secret-value --secret-id merch_api_db_credentials --query SecretString --output text | jq -r ".db_password")

sudo -u ubuntu git clone https://${GITHUB_TOKEN}github.com/AbbyAdj/cloud-picture-album-api.git

# EXPORT .ENV VARIABLES

# TO BE IMPLEMENTED

cd cloud-picture-album-api

touch .env


# DATABASE SETUP

sudo apt install postgresql -y


# GET SERVER UP AND RUNNING

# sudo apt install make

sudo apt install python3.12-venv -y

cd ~/cloud-picture-album-api

