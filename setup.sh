npm install
npm run build
flask db init
sudo pip3 install -r requirements.txt
sudo cp science_register.conf /etc/supervisor/conf.d/
sudo cp science_register_nginx.conf /etc/nginx/sites-enabled/
sudo supervisorctl update
sudo systemctl restart nginx
sudo certbot --nginx -d research.medsenger.ru
cp .env.example .env
