#!/bin/bash
domain="mb30host.online"
email="megamail49421331@gmail.com"
script_location="/root/tm_offersAdmin"

# Check if --restart is passed as an argument
restart=false
for arg in "$@"; do
  if [ "$arg" == "--restart" ]; then
    restart=true
    break
  fi
done

# Obtain the certificate
if certbot certificates | grep -q "Certificate Name: ${domain}"; then
    echo "Renewing existing certificate..."
    certbot renew --webroot --webroot-path=./nginx/ssl/ --non-interactive --cert-name $domain
else
    echo "Requesting new certificate..."
    certbot certonly --webroot --webroot-path=./nginx/ssl/ -d $domain --email $email --agree-tos --non-interactive --cert-name $domain
fi


fullchain_path="/etc/letsencrypt/live/${domain}/fullchain.pem"
privkey_path="/etc/letsencrypt/live/${domain}/privkey.pem"
nginx_certs_path="${script_location}/nginx/ssl/default"

# Copy certificates
cp $fullchain_path "${nginx_certs_path}/fullchain.pem"
cp $privkey_path "${nginx_certs_path}/privkey.pem"

echo "FULLCHAIN: " $fullchain_path "${nginx_certs_path}/fullchain.pem"
echo "PRIVKEY: " $privkey_path "${nginx_certs_path}/privkey.pem"

# Set permissions
chmod 644 "${nginx_certs_path}/fullchain.pem"
chmod 644 "${nginx_certs_path}/privkey.pem"

echo "Certificates updated"

# Log the time the script ran
echo "Script ran at $(date)" >> ${script_location}/cron_test.log

# Restart nginx if --restart is passed
if [ "$restart" == true ]; then
  echo "Reloading nginx inside the container..." >> ${script_location}/cron_test.log
  # Use docker exec to reload nginx
  docker compose -f ${script_location}/docker-compose.yaml exec nginx nginx -s reload || { echo "Failed to reload nginx" >> ${script_location}/cron_test.log; exit 1; }
  echo "Reloaded nginx at $(date)" >> ${script_location}/cron_test.log
fi