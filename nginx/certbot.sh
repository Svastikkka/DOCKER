#!/bin/bash

# First-time certificate generation
certbot certonly \
  --webroot -w /var/www/certbot \
  -d "$DOMAIN" \
  --email "$EMAIL" \
  --agree-tos \
  --non-interactive

# Loop forever and renew twice a day
while true; do
  certbot renew --webroot -w /var/www/certbot
  sleep 12h
done
