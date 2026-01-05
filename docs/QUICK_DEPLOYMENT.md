# ⚡ Quick Deployment Start (10 minut)

## TL;DR - Pro ty co spěchají

```bash
# 1. Příprava (2 min)
cd /home/lenkaluksova/hypoteky_win && git add . && git commit -m "Deploy" && git push

# 2. Migrace (2 min)
source .venv/bin/activate
python manage.py migrate

# 3. Testy (3 min)
pytest klienti/tests_views.py -q

# 4. Build (2 min)
python manage.py collectstatic --noinput

# 5. Start (1 min)
sudo systemctl restart hypoteky
curl https://example.com/

# ✅ DONE!
```

---

## Detaily (Pro bezpečné nasazení)

### Krok 1: Ověř Konfiguraci
```bash
# Mělo by mít všechna tato pole:
grep "^DEBUG=False\|^ALLOWED_HOSTS=\|^DB_\|^EMAIL_\|^ENCRYPTED_MODEL_FIELDS_KEY=" .env | wc -l
# Mělo by být: 9+ řádků
```

### Krok 2: Backup (DŮLEŽITÉ!)
```bash
mysqldump -u hypoteky_user -p hypoteky_prod > /backups/pre_deploy_$(date +%s).sql
```

### Krok 3: Migrace s Plánem
```bash
python manage.py migrate --plan  # Zkontroluj co se změnit
python manage.py migrate         # Spusť
```

### Krok 4: Testy (Jen Core)
```bash
pytest klienti/tests_views.py klienti/tests_api.py -q
# Mělo by: 30+ passed
```

### Krok 5: Security Check
```bash
python manage.py check --deploy
# Mělo by: "no issues"
```

### Krok 6: Cron Setup
```bash
sudo bash dev/setup_cron_notifications.sh --cron
sudo crontab -l | grep hypoteky  # Ověř
```

### Krok 7: Web Server
```bash
# Pokud Gunicorn + Nginx:
sudo systemctl restart hypoteky
sudo systemctl restart nginx

# Ověř
curl https://example.com/
```

### Krok 8: Health Check
```bash
# ✅ Website lives
curl -I https://example.com/

# ✅ Admin panel
curl https://example.com/admin/

# ✅ API
curl https://example.com/api/klienti/

# ✅ Logs
tail -10 /var/log/hypoteky/django.log | grep -i error  # Mělo by být prázdné
```

---

## Problémy & Řešení

| Problém | Řešení |
|---------|--------|
| `ERROR: ENCRYPTED_MODEL_FIELDS_KEY not found` | `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" >> .env` |
| `no such table: klienti_klient` | `python manage.py migrate` |
| `Connection refused to MySQL` | `grep ^DB_ .env` a zkontroluj data |
| `Email not sending` | `python manage.py shell` → `send_mail(...)` → test |
| `Gunicorn socket not found` | `sudo systemctl restart hypoteky && ls -la /run/gunicorn.sock` |
| `Cron not running` | `sudo crontab -l` a zkontroluj, že je tam |

---

## Monitoring (Daily Checks)
```bash
# Zkontroluj každý den:
sudo systemctl status hypoteky hypoteky hypoteky
tail -20 /var/log/hypoteky/django.log | grep -i error
tail -20 /var/log/hypoteky_notifications.log
curl -s https://example.com/ | wc -c  # Mělo by být > 1000 (ne error)

# Pokud 404 nebo chyba -> zjisti v logs -> fix -> restart
```

---

## Rollback (Emergency Only)
```bash
# Zastavit
sudo systemctl stop hypoteky

# Vrátit kód
git revert HEAD

# Vrátit DB z backupu
mysql -u hypoteky_user -p hypoteky_prod < /backups/pre_deploy_*.sql

# Restartovat
sudo systemctl start hypoteky
curl https://example.com/
```

---

**Čas**: ~10-15 minut  
**Riziko**: Nízké (máš backup)  
**Pokud se něco pokazí**: Kontaktuj ops@company.com
