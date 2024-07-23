# Installation

Create prodigy user and group if not done yet:

```sh
groupadd prodigy
useradd -s /bin/bash -g prodigy -d /usr/local/prodigy/ prodigy
```

clone this repository in the prodigy home directory:

```sh
git clone https://github.com/OpenPecha/prodigy-tools.git
```

copy the `prodigy.service` script in `/etc/systemd/system/` and then

```sh
systemctl daemon-reload
systemctl enable prodigy
systemctl start prodigy
```

## nginx

copy `prodigy_images.conf` into `/etc/nginx/sites-enabled/` and restart nginx.

## SSL certificate

#### setup

The first time, create `/var/www/letsencrypt`, copy the following in `/etc/nginx/acmechallenge.conf`:

```
location ^~ /.well-known/acme-challenge/ {
    default_type "text/plain";
    root         /var/www/letsencrypt;
}

location = /.well-known/acme-challenge/ {
    return 404;
}

```

and the following in `/etc/nginx/ssl_params`:

```
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;
ssl_dhparam /etc/nginx/dhparam.pem;
ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
ssl_ciphers 'ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:ECDHE-ECDSA-DES-CBC3-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA:!DSS';
ssl_prefer_server_ciphers on;
ssl_stapling on;
ssl_stapling_verify on;
```

and run

```
openssl dhparam -out /etc/nginx/dhparam.pem 2048 2> /dev/null
```

and add automatic certificate renewal to the crontab:

```
crontab -l | { cat; echo "0 12 * * * /usr/bin/certbot renew --quiet && service nginx restart";  } | crontab -
```

#### Creating a certificate

Run the following the create a new certificate:

```
certbot certonly -d prodigy.bdrc.io --webroot --agree-tos -m github@tbrc.org -w /var/www/letsencrypt
```

