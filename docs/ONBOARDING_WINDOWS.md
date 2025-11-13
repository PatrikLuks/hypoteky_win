# 🪟 Jak spustit hypoteční aplikaci ve VS Code na Windows

Tento návod ti krok za krokem ukáže, jak rozběhnout Django aplikaci v prostředí Windows (včetně VS Code, PowerShell, CMD i WSL).

---

## 1. Klonování repozitáře

Otevři PowerShell nebo CMD a spusť:
```powershell
git clone https://github.com/PatrikLuks/hypoteky_django.git
cd hypoteky
```

---

## 2. Vytvoření a aktivace virtuálního prostředí

### a) PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### b) CMD
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### c) WSL (Windows Subsystem for Linux)
Doporučeno pro plnou kompatibilitu shell skriptů!
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Instalace závislostí

```powershell
pip install -r requirements.txt
pip install playwright
python -m playwright install --with-deps
```

---

## 4. Nastavení databáze (MySQL)

- Postupuj podle `DB_SETUP_MYSQL.md` (návod je univerzální pro všechny OS).
- Pro Windows doporučuji MySQL Workbench nebo XAMPP.

---

## 5. Migrace databáze

```powershell
python manage.py migrate
```

---

## 6. Spuštění serveru

```powershell
python manage.py runserver
```

Aplikace poběží na http://localhost:8000

---

## 7. Spuštění testů a údržby

```powershell
python -m pytest
```

---

## 8. Poznámky k shell skriptům

- Většina údržbových skriptů (`*.sh`) je určena pro Linux/macOS/WSL. Ve Windows CMD/PowerShell je nespouštěj přímo.
- Pro plnou kompatibilitu doporučuji používat WSL (Windows Subsystem for Linux) – umožní spouštět všechny shell skripty stejně jako na Linuxu/Macu.
- Alternativně můžeš údržbu provádět ručně nebo si vytvořit `.bat` skripty pro základní úlohy (aktivace prostředí, testy, server).

---

## 9. Doporučení

- Pokud narazíš na problém s cestami, používej vždy `\` ve Windows a `/` v Linux/WSL.
- Pro pokročilé workflow (údržba, snapshoty, CI/CD) používej WSL nebo Linux/macOS.
- Pravidelně zálohuj a pushuj změny na GitHub.

---

## 🆕 Novinky a tipy (červen 2025)
- **Kalkulačka hypotéky**: Nový UX, validace, grafy, export, přístupnost, sjednocený vzhled, tooltipy, animace, edukativní chybové hlášky.
- **Font Awesome**: Ikony jsou načítány lokálně ze složky `static/fontawesome`. Pokud se objeví čtverečky, spusť `./download_fontawesome.sh` (přes WSL nebo v Linux/macOS).
- **Optimalizace pro slabší HW**: Pravidelně spouštěj úklidové skripty (`cleanup_*`, `run_all_maintenance.sh`), archivuj snapshoty mimo hlavní workspace, omez rozšíření ve VS Code.
- **Údržba workspace**: Používej skripty pro úklid záloh, snapshotů, duplicit a prázdných souborů. Vše najdeš v rootu projektu a v `ONBOARDING.md`.

---

## 🖼️ Font Awesome – lokální načítání ikon
- Ikony Font Awesome jsou načítány lokálně ze složky `static/fontawesome`.
- Pro update spusť `./download_fontawesome.sh` (přes WSL nebo v Linux/macOS).
- V šablonách používej třídy `fa-solid`, `fa-regular` dle Font Awesome 6.
- Ověř, že máš v šabloně `{% load static %}`.

---

## 🧹 Údržba workspace a snapshotů
- Pravidelně spouštěj skripty `cleanup_*`, `run_all_maintenance.sh` a archivuj snapshoty/reporty mimo hlavní workspace.
- Pro úklid záloh, snapshotů a duplicit používej připravené skripty (viz `ONBOARDING.md`).
- Pro slabší HW doporučujeme minimalizovat počet otevřených souborů a rozšíření ve VS Code.

---

## 10. Odkazy
- [README.md](README.md)
- [ONBOARDING.md](ONBOARDING.md)
- [DB_SETUP_MYSQL.md](DB_SETUP_MYSQL.md)

---

Pokud narazíš na problém, začni od checklistu a logů, nebo se ptej v týmu. Hodně štěstí!
