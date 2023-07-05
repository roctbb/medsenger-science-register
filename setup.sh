npm install
flask db init
sudo pip3 install -r requirements.txt
sudo cp agents_forms.conf /etc/supervisor/conf.d/
sudo cp agents_forms_nginx.conf /etc/nginx/sites-enabled/
sudo supervisorctl update
sudo systemctl restart nginx
sudo certbot --nginx -d research.medsenger.ru
cp .env.example .env
