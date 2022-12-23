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

copy `prodigy_images.conf` into `/etc/nginx/sites-enabled/` and restart nginx.