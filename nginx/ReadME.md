# Nginx

Following are the steps to any service

- Replace `example.svastikkk.com` with your domain in `docker-compose.yml`, `nginx.conf.http`, `nginx.conf.template`.
- Replace `manshu@svastikkk.com` with your email in `docker-compose.yml`, `nginx.conf.http`, `nginx.conf.template`
- Run command `chmod -R 777 certbot`
- Run command `chmod -R 777 webroot`
- Run command `chmod -R 777 certbot.sh`
- Run command `chmod -R 777 entrypoint.sh`
- Now comment following line `- ./nginx.conf.template:/etc/nginx/nginx.conf` and uncomment `- ./nginx.conf.http:/etc/nginx/nginx.conf`. We are doing this so certbot can download certificate at first time.
- Run command `docker compose up -d --build`