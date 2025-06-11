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

## 10. Odkazy
- [README.md](README.md)
- [ONBOARDING.md](ONBOARDING.md)
- [DB_SETUP_MYSQL.md](DB_SETUP_MYSQL.md)

---

Pokud narazíš na problém, začni od checklistu a logů, nebo se ptej v týmu. Hodně štěstí!
