# 📋 DEPLOYMENT_CHECKLIST – Produkční Nasazení

**Cíl:** Zajistit, že aplikace je bezpečná, testovaná a připravená na produkci

---

## ✅ PRE-DEPLOYMENT (3 dny před nasazením)

### 1. Bezpečnost
- [ ] Všechna citlivá data jsou v `.env` (nie v kódu)
- [ ] DEBUG=False v `.env.production`
- [ ] SECRET_KEY je nový a silný (50+ znaků)
- [ ] ALLOWED_HOSTS je nastaven na produkční domény
- [ ] CSRF_TRUSTED_ORIGINS je nastaven
- [ ] SECURE_SSL_REDIRECT=True
- [ ] SESSION_COOKIE_SECURE=True
- [ ] CSRF_COOKIE_SECURE=True
- [ ] SECURE_HSTS_SECONDS=31536000

### 2. Databáze
- [ ] MySQL server běží a je přístupný
- [ ] Databáze je vytvořena s UTF-8
- [ ] Uživatel DB má správná oprávnění
- [ ] Backup databáze je vytvořen
- [ ] Migrace jsou testovány: `python manage.py migrate --plan`

### 3. Static Files
- [ ] `python manage.py collectstatic --noinput` prošel bez chyb
- [ ] Static files jsou na disku nebo CDN
- [ ] STATIC_URL je správně nastavena

### 4. Testy
- [ ] Všechny unit testy procházejí: `pytest klienti/ tests/`
- [ ] Coverage > 70%: `pytest --cov=klienti`
- [ ] E2E testy procházejí: `pytest -m e2e`
- [ ] Bezpečnostní testy prošly: `pytest klienti/tests_bezpecnost.py`

### 5. Security Audit
- [ ] Bezpečnostní kontrola: `safety scan`
- [ ] Bandit audit: `bandit -r klienti/ hypoteky/`
- [ ] OWASP Top 10 audit (SQL injection, XSS, CSRF, atd.)
- [ ] Penetrační test (dobrovolně)

### 6. Performance
- [ ] Database queries jsou optimalizovány
- [ ] Caching je nakonfigurován (Redis/Memcached)
- [ ] Frontend assets jsou minifikované
- [ ] GZIP compression je povolena
- [ ] Load test prošel: `apache2 -n 1000 https://app.com/`

### 7. Monitoring & Logging
- [ ] Sentry je nakonfigurován pro error tracking
- [ ] Logging je nastaveno (rotace logů)
- [ ] Email notifikace na kritické chyby
- [ ] Monitoring dashboard (Grafana) je připraven
- [ ] Health check endpoint (`/health/`) je funkční

### 8. Dokumentace
- [ ] README je aktuální
- [ ] API dokumentace je přesná
- [ ] Runbook pro incident response
- [ ] Rollback plán je dokumentován

---

## 🚀 DEPLOYMENT (Den nasazení)

### 1. Příprava Serveru
```bash
# Loguď se na produkční server
ssh user@production-server.com

# Aktualizuj systém
sudo apt update && sudo apt upgrade -y

# Instaluj dependencies
sudo apt install -y python3 python3-venv python3-dev mysql-server redis-server nginx

# Vytvoř aplikační uživatele
sudo useradd -m -s /bin/bash hypoteky
sudo su - hypoteky
```

### 2. Deploy Aplikace
```bash
# Clone repozitáře
git clone https://github.com/PatrikLuks/hypoteky_django.git /home/hypoteky/app
cd /home/hypoteky/app

# Vytvoř virtuální prostředí
python3 -m venv venv
source venv/bin/activate

# Instaluj závislosti
pip install -r requirements.txt
pip install gunicorn

# Vytvoř .env z .env.example
cp .env.example .env
# Vyplň produkční hodnoty
nano .env

# Proveď migrace
python manage.py migrate

# Sbírni static files
python manage.py collectstatic --noinput

# Vytvoř superuživatele
python manage.py createsuperuser
```

### 3. Gunicorn Setup
```bash
# Vytvoř Gunicorn config
sudo nano /home/hypoteky/app/gunicorn_config.py
```

```python
# gunicorn_config.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
timeout = 120
access_log = "/home/hypoteky/logs/access.log"
error_log = "/home/hypoteky/logs/error.log"
loglevel = "info"
```

```bash
# Spusť Gunicorn
gunicorn \
  --config /home/hypoteky/app/gunicorn_config.py \
  hypoteky.wsgi:application
```

### 4. Systemd Service (Pro automatický start)
```bash
sudo nano /etc/systemd/system/hypoteky.service
```

```ini
[Unit]
Description=Hypotéky Django Application
After=network.target mysql.service

[Service]
Type=notify
User=hypoteky
WorkingDirectory=/home/hypoteky/app
Environment="PATH=/home/hypoteky/app/venv/bin"
ExecStart=/home/hypoteky/app/venv/bin/gunicorn \
  --config /home/hypoteky/app/gunicorn_config.py \
  hypoteky.wsgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable a start service
sudo systemctl daemon-reload
sudo systemctl enable hypoteky
sudo systemctl start hypoteky
sudo systemctl status hypoteky
```

### 5. Nginx Setup
```bash
sudo nano /etc/nginx/sites-available/hypoteky.conf
```

```nginx
upstream hypoteky {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    client_max_body_size 10M;

    location /static/ {
        alias /home/hypoteky/app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/hypoteky/app/media/;
    }

    location / {
        proxy_pass http://hypoteky;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/hypoteky.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d example.com -d www.example.com
```

### 7. Database Backup
```bash
# Prvotní backup
mysqldump -u root -p hypoteky > /home/hypoteky/backups/hypoteky_$(date +%Y%m%d_%H%M%S).sql

# Automatizovaný denní backup (crontab)
0 2 * * * mysqldump -u root -p hypoteky | gzip > /home/hypoteky/backups/hypoteky_$(date +\%Y\%m\%d).sql.gz
```

---

## ✅ POST-DEPLOYMENT (Den po nasazení)

### 1. Zdravotnostní Kontrola
```bash
# Otestuj aplikaci
curl -I https://example.com/
curl -I https://example.com/api/docs/

# Ověř logs
tail -f /home/hypoteky/logs/access.log
tail -f /home/hypoteky/logs/error.log

# Zkontroluj Sentry
# Jdi na https://sentry.io/ a ověř, že nejsou chyby
```

### 2. Monitoring Setup
```bash
# Sentry integrační test
python -c "import sentry_sdk; sentry_sdk.init('YOUR_DSN'); sentry_sdk.capture_exception(Exception('Test'))"

# Health check
curl https://example.com/health/
```

### 3. Zálohy & Disaster Recovery
```bash
# Ověř backupy
ls -lh /home/hypoteky/backups/

# Test restore
mysql -u root -p hypoteky_test < /home/hypoteky/backups/hypoteky_latest.sql
```

### 4. User & Access Testing
- [ ] Přihlaš se jako admin
- [ ] Vytvoř testovacího klienta
- [ ] Otestuj workflow (všech 15 kroků)
- [ ] Otestuj reporting & export
- [ ] Otestuj API (GET, POST, PATCH, DELETE)
- [ ] Otestuj 2FA (TOTP)

### 5. Performance Verification
```bash
# Load test
apache2 -n 100 -c 10 https://example.com/

# Slow query log check
tail -f /var/log/mysql/slow.log
```

---

## 🆘 ROLLBACK (Pokud selhání)

```bash
# Vrátit na předchozí verzi
cd /home/hypoteky/app
git checkout previous-tag

# Obnovit databázi
mysql -u root -p hypoteky < /home/hypoteky/backups/hypoteky_previous.sql

# Restartuj aplikaci
sudo systemctl restart hypoteky

# Ověř funkčnost
curl https://example.com/
```

---

## 📊 Monitoring & Maintenance

### Daily Tasks
- [ ] Kontroluj logy (Sentry, nginx, MySQL)
- [ ] Ověř health check endpoint
- [ ] Kontroluj disk space (`df -h`)
- [ ] Kontroluj memory usage (`free -h`)

### Weekly Tasks
- [ ] Kontroluj databázi (integritu, velikost)
- [ ] Ověř backupy
- [ ] Aktualizuj dependencies (`pip list --outdated`)
- [ ] Kontroluj security updates

### Monthly Tasks
- [ ] Performance audit
- [ ] Security audit
- [ ] User feedback review
- [ ] Database optimization

---

## 📝 Contacts & Escalation

| Role | Kontakt | Čas |
|------|---------|------|
| Administrátor | admin@example.com | 24/7 |
| Developer | dev@example.com | Business hours |
| Manager | manager@example.com | Business hours |

---

**Autor:** GitHub Copilot  
**Datum:** 11. listopadu 2025  
**Status:** Produkční nasazení připraveno

