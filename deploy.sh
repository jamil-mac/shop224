#!/bin/bash

PROJECT_NAME=shop_224
PROJECT_ROOT=/var/www/$PROJECT_NAME
VENV_PATH=$PROJECT_ROOT/venv
NGINX_CONF=/etc/nginx/sites-available/$PROJECT_NAME.conf

sudo apt-get update
sudo apt-get install -y python3-dev python3-venv nginx

# Detect Python 3 automatically
PYTHON_BIN=$(command -v python3)

# Create virtual environment
$PYTHON_BIN -m venv $VENV_PATH

# Install deps
source $VENV_PATH/bin/activate
pip install --upgrade pip
pip install -r $PROJECT_ROOT/requirements.txt
pip install psycopg2-binary gunicorn

cd $PROJECT_ROOT

# Gunicorn service
sudo tee /etc/systemd/system/$PROJECT_NAME.service > /dev/null <<EOF
[Unit]
Description=Gunicorn Service
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$PROJECT_ROOT
ExecStart=$VENV_PATH/bin/gunicorn --access-logfile - --workers 3 --bind unix:$PROJECT_ROOT/$PROJECT_NAME.sock $PROJECT_NAME.wsgi:application

[Install]
WantedBy=multi-user.target
EOF


# Enable services
sudo systemctl daemon-reload
sudo systemctl enable $PROJECT_NAME

sudo systemctl start $PROJECT_NAME

# Apply migrations and collect static
$VENV_PATH/bin/python manage.py makemigrations
$VENV_PATH/bin/python manage.py migrate
$VENV_PATH/bin/python manage.py collectstatic --noinput

# Nginx config
sudo tee $NGINX_CONF > /dev/null <<EOF
server {
    listen 80;
    server_name churvaqalar.uz ;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root $PROJECT_ROOT;
    }
    location /media/ {
        root $PROJECT_ROOT;
    }
    location / {
        include proxy_params;
        proxy_pass http://unix:$PROJECT_ROOT/$PROJECT_NAME.sock;
    }
}
EOF

sudo ln -s $NGINX_CONF /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
