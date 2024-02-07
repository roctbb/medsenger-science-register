npm install
npm run build
flask db init
sudo pip3 install -r requirements.txt
sudo cp telegynecology_register.ini /etc/uwsgi/apps/
sudo cp telegynecology_register.conf /etc/supervisor/conf.d/
sudo cp telegynecology_register_nginx.conf /etc/nginx/sites-enabled/
sudo supervisorctl update
sudo systemctl restart nginx
sudo certbot --nginx -d register.telegynecology.ru
if [ ! -f ./.env ]; then
  cp .env.example .env
fi
