# 📦 Kroky k Produkčnímu Nasazení - Přehled

**Status**: ✅ Připraveno k nasazení  
**Čas**: ~5-6 hodin + 1-2 týdny pilotáže  
**Riziko**: Nízké (máš backup, rollback plán, testy)  
**Aktualizace**: 5. ledna 2026

---

## 🎯 10-Bodový Nasazovací Plán

| # | Fáze | Čas | Kroky | Status | Soubor |
|---|------|-----|-------|--------|--------|
| 1️⃣ | **Build & Config** | 60 min | Git commit → pip install → .env check → static files | ⏳ Not Started | [RUNBOOK](PRODUCTION_DEPLOYMENT_RUNBOOK.md#fáze-1-příprava--build-60-minut) |
| 2️⃣ | **Migrace & DB** | 30 min | DB Backup → migrate --plan → python migrate → data validate | ⏳ Not Started | [RUNBOOK](PRODUCTION_DEPLOYMENT_RUNBOOK.md#fáze-2-databáze--migrace-30-minut) |
| 3️⃣ | **Testování** | 45 min | Unit testy → Integration → E2E → Coverage 85%+ | ⏳ Not Started | [RUNBOOK](PRODUCTION_DEPLOYMENT_RUNBOOK.md#fáze-3-testování-45-minut) |
| 4️⃣ | **Security Audit** | 60 min | check --deploy → requirements → encrypted → audit logs → GDPR | ⏳ Not Started | [RUNBOOK](PRODUCTION_DEPLOYMENT_RUNBOOK.md#fáze-4-bezpečnostní-audit-60-minut) |
| 5️⃣ | **Notifikace & Cron** | 30 min | Email test → management commands → cron/systemd setup | ⏳ Not Started | [RUNBOOK](PRODUCTION_DEPLOYMENT_RUNBOOK.md#fáze-5-notifikace--cron-30-minut) |
| 6️⃣ | **Web Server Setup** | 45 min | Gunicorn install → systemd service → Nginx config → SSL cert | ⏳ Not Started | [RUNBOOK](PRODUCTION_DEPLOYMENT_RUNBOOK.md#fáze-6-web-server-setup-45-minut) |
| 7️⃣ | **Monitoring & Logging** | 30 min | Log files check → Health checks → Sentry (optional) | ⏳ Not Started | [RUNBOOK](PRODUCTION_DEPLOYMENT_RUNBOOK.md#fáze-7-monitoring--logging-30-minut) |
| 8️⃣ | **Final Verification** | 30 min | Checklist → User testing → Sign-off | ⏳ Not Started | [RUNBOOK](PRODUCTION_DEPLOYMENT_RUNBOOK.md#fáze-8-final-verification-30-minut) |
| 9️⃣ | **Pilotní Provoz** | 1-2 týdny | Daily monitoring → User feedback → Performance test → Approval | ⏳ Not Started | [RUNBOOK](PRODUCTION_DEPLOYMENT_RUNBOOK.md#fáze-9-pilotní-provoz-1-2-týdny) |
| 🔟 | **Post-Production** | Ongoing | Maintenance schedule → Updates → Security patching | ⏳ Not Started | [RUNBOOK](PRODUCTION_DEPLOYMENT_RUNBOOK.md#fáze-10-post-production-ongoing) |

**Celkový čas**: ~5-6 hodin aktivního práce (bez čekání na pilotáž)

---

## 📋 Souhrn Kontrolních Bodů

### Fáze 1: Build & Config (60 min)
```
✅ Git commit & push na main
✅ pip install -r requirements.txt
✅ .env obsahuje: SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, DB_*, EMAIL_*, ENCRYPTED_MODEL_FIELDS_KEY
✅ python manage.py collectstatic --noinput
✅ npm run build (pokud máš frontend)
```

### Fáze 2: Migrace & DB (30 min)
```
✅ mysqldump backup PŘED migrací
✅ python manage.py migrate --plan (ověřit že je 0020_update_workflow_choices)
✅ python manage.py migrate (aplikovat)
✅ Ověřit max workflow step ≤ 15
```

### Fáze 3: Testování (45 min)
```
✅ pytest klienti/tests_views.py -q → 30+ passed
✅ pytest klienti/tests_api.py -q → 12+ passed
✅ pytest --cov=klienti → 85%+ coverage
✅ pytest dev/tests_e2e_playwright.py (s live serverem)
```

### Fáze 4: Security (60 min)
```
✅ python manage.py check --deploy → "no issues"
✅ bash dev/check_requirements_security.sh → 0 CVE
✅ 14 šifrovaných polí v Klient modelu
✅ NotifikaceLog zaznamenává notifikace
✅ GDPR: export & delete endpoints fungují
```

### Fáze 5: Notifikace & Cron (30 min)
```
✅ python manage.py send_deadline_notifications
✅ python manage.py send_reporting_email
✅ sudo bash dev/setup_cron_notifications.sh --cron
✅ sudo crontab -l | grep hypoteky (ověřit instalaci)
```

### Fáze 6: Web Server (45 min)
```
✅ pip install gunicorn
✅ /etc/systemd/system/hypoteky.service
✅ sudo systemctl enable hypoteky && start hypoteky
✅ /etc/nginx/sites-available/hypoteky.conf
✅ sudo certbot certonly -d example.com
✅ curl https://example.com/ → HTTP 200
```

### Fáze 7: Monitoring (30 min)
```
✅ tail -50 /var/log/hypoteky/django.log (žádné ERROR)
✅ tail -50 /var/log/hypoteky_notifications.log
✅ curl https://example.com/ (zdravotní test)
✅ systemctl status hypoteky → active
✅ systemctl status nginx → active
```

### Fáze 8: Finál (30 min)
```
✅ git status → "nothing to commit"
✅ python manage.py showmigrations klienti | grep "\[X\]" (všechny migrace)
✅ curl https://example.com/admin/ → login form
✅ curl https://example.com/api/klienti/ → JSON
✅ Finální sign-off od DevOps, Developer, QA
```

### Fáze 9: Pilotáž (1-2 týdny)
```
✅ Daily: tail -50 /var/log/hypoteky/django.log (monitoring)
✅ User testing: 5-10 lidí zkouší workflow
✅ Performance test: ab -n 1000 -c 10
✅ Sentry/monitoring: sleduj error rate
✅ Finální approval pro go/no-go
```

### Fáze 10: Post-Production (Ongoing)
```
✅ Weekly: DB backup, performance review
✅ Monthly: Security updates, dependency updates
✅ Quarterly: Full penetration test
✅ Maintenance schedule nastavena
```

---

## 📚 Dostupné Dokumenty

| Soubor | Účel | Čitatelnost |
|--------|------|------------|
| [PRODUCTION_DEPLOYMENT_RUNBOOK.md](PRODUCTION_DEPLOYMENT_RUNBOOK.md) | **Detailný krok-za-krokem** | ⭐⭐⭐⭐⭐ (Velmi detailní) |
| [QUICK_DEPLOYMENT.md](QUICK_DEPLOYMENT.md) | **TL;DR - 10 minut** | ⭐⭐ (Super krátké) |
| [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) | **Formální checklist** | ⭐⭐⭐ (Strukturované) |
| README.md | **Úvodní guide** | ⭐⭐⭐⭐ (Dobré) |
| docs/ONBOARDING.md | **Onboarding pro nováčky** | ⭐⭐⭐⭐ (Přátelské) |

---

## 🚀 Jak Začít?

### Pokud máš 5 minut:
→ Čti [QUICK_DEPLOYMENT.md](QUICK_DEPLOYMENT.md)

### Pokud máš 1-2 hodiny:
→ Čti [PRODUCTION_DEPLOYMENT_RUNBOOK.md](PRODUCTION_DEPLOYMENT_RUNBOOK.md) Fáze 1-3

### Pokud máš 5-6 hodin:
→ Projdi všechny Fáze v [PRODUCTION_DEPLOYMENT_RUNBOOK.md](PRODUCTION_DEPLOYMENT_RUNBOOK.md)

### Pokud jsi DevOps:
→ Soustředí se na Fáze 1, 2, 5, 6, 7, 10

### Pokud jsi Developer:
→ Soustředí se na Fáze 1, 3, 4, 8

### Pokud jsi QA/Tester:
→ Soustředí se na Fáze 3, 4, 8, 9

---

## 🔄 Typický Nasazovací Den

```
09:00 - Kick-off meeting (5 min)
09:05 - Fáze 1: Build & Config (DevOps/Dev) ← Paralelně
09:05 - Fáze 2: DB Backup & Migrace (DBA) ← Čeká na Fáze 1
09:45 - Fáze 3: Testy (QA) ← Čeká na Fáze 1
10:15 - Fáze 4: Security Audit (Security/Dev) ← Čeká na Fáze 1
11:15 - Fáze 5: Cron Setup (DevOps) ← Paralelně
11:45 - Fáze 6: Web Server (DevOps) ← Čeká na Fáze 2
12:30 - Lunch break ☕
13:30 - Fáze 7: Monitoring Setup (DevOps)
14:00 - Fáze 8: Final Verification (Team) ← Všichni
14:30 - GO/NO-GO Decision (Management)
```

---

## ⚠️ Klíčová Rizika & Mitigation

| Riziko | Impact | Mitigation |
|--------|--------|-----------|
| DB migrace selže | 🔴 Critical | ✅ Backup PŘED migrací, test --plan |
| Tests padnou | 🟠 Major | ✅ Všechny testy lokálně OK před deploy |
| Email nechodí | 🟡 Minor | ✅ Test SMTP v manage.py shell |
| Web server se nepustí | 🔴 Critical | ✅ Test Gunicorn lokálně |
| SSL certifikát selže | 🟠 Major | ✅ Certbot dry-run předem |
| Cron se nenahrazuje | 🟡 Minor | ✅ sudo crontab -l ověřit |
| Notifikace nejdou | 🟡 Minor | ✅ Management command test |
| Performance problém | 🟡 Minor | ✅ Load test během pilotáže |
| Security vulnerability | 🔴 Critical | ✅ Full audit v Fázi 4 |

---

## 📞 Komunikace & Escalation

### Během Nasazení
- **DevOps Lead**: ops@company.com (odpovídá za Fáze 1, 2, 5, 6, 7)
- **Developer**: dev@company.com (odpovídá za Fáze 3, 4, 8)
- **QA**: qa@company.com (odpovídá za testování)

### Escalation Path
```
Problem Discovered
    ↓
Zjisti Root Cause (logy, monitoring)
    ↓
Pokus fix (pokud jednoduchý)
    ↓
Pokud nelze fixnout → Escaluj na Lead
    ↓
Lead rozhoduje: Continue vs. Rollback
    ↓
Pokud Rollback → Obnovit z backupu
```

---

## ✅ Success Criteria

Nasazení je **úspěšné**, když:
- ✅ Všechny testy procházejí
- ✅ Security audit je čistý
- ✅ Website je dostupná (https://example.com/)
- ✅ Logy nejsou plné ERROR zpráv
- ✅ Email notifikace fungují
- ✅ Database je integrální (integrity check OK)
- ✅ Cron úlohy běží (logs viditelné)
- ✅ Performance je akceptabilní (response < 2s)
- ✅ Všichni stakeholders dali approval

---

## 🎓 Learning Resources

### Pro DevOps
- Django deployment guide: https://docs.djangoproject.com/en/4.2/howto/deployment/
- Gunicorn config: https://gunicorn.org/
- Nginx proxy: https://nginx.org/

### Pro Developers
- pytest guide: https://docs.pytest.org/
- Django testing: https://docs.djangoproject.com/en/4.2/topics/testing/
- Security checklist: https://owasp.org/www-project-web-security-testing-guide/

### Pro QA
- Playwright guide: https://playwright.dev/
- Load testing: https://httpd.apache.org/docs/2.4/programs/ab.html
- Penetration testing: https://owasp.org/www-project-top-ten/

---

## 📊 Metriky Úspěchu (Post-Deployment)

Monitoruj tyto metriky během prvních 2 týdnů:

| Metrika | Target | Check |
|---------|--------|-------|
| Error Rate | < 0.1% | Sentry dashboard |
| Response Time | < 2s | Nginx access logs |
| Uptime | > 99.9% | systemctl status + Monitoring |
| CPU Usage | < 70% | top command |
| Memory Usage | < 80% | free command |
| DB Size Growth | < 10MB/day | MySQL du -sh |
| Cron Execution | 100% | Cron logs |
| Email Delivery | > 99% | NotifikaceLog |

---

## 🎯 Next Steps

1. **TODAY**: Přečti [QUICK_DEPLOYMENT.md](QUICK_DEPLOYMENT.md)
2. **TOMORROW**: Začni s [PRODUCTION_DEPLOYMENT_RUNBOOK.md](PRODUCTION_DEPLOYMENT_RUNBOOK.md) Fáze 1
3. **NEXT 3 DAYS**: Projdi Fáze 1-8
4. **WEEK 2**: Pilotní provoz + monitoring
5. **WEEK 3**: Finální approval + Go Live

---

**Poslední aktualizace**: 5. ledna 2026  
**Připraveno**: ✅ Ano  
**Vytvořeno**: Copilot AI Assistant  
**Pro projekt**: hypoteky_win (Django CRM pro finanční poradce)
