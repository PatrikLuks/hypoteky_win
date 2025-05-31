# TROUBLESHOOTING_GUIDE.md

> Praktický průvodce řešením nejčastějších problémů v projektu (Django, shell skripty, snapshoty, CI/CD)
> Pomáhá rychle najít příčinu a navrhnout řešení – ideální pro onboarding i ostrý provoz.

---

## 1. Problémy s prostředím a závislostmi
- [ ] **Virtuální prostředí nejde aktivovat**
    - Ověř, že existuje složka `.venv` a obsahuje `bin/activate`.
    - Pokud chybí, spusť: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- [ ] **Chybí nebo selhává některý balíček**
    - Spusť: `pip install -r requirements.txt`
    - Ověř, že používáš správnou verzi Pythonu (viz README).

## 2. Problémy s databází
- [ ] **Nelze se připojit k DB / selhávají migrace**
    - Ověř přihlašovací údaje v `settings.py`.
    - Spusť: `python manage.py showmigrations` a `python manage.py migrate`
    - Ověř, že běží MySQL server a máš správná práva.
- [ ] **Chyby integrity dat**
    - Spusť: `python check_db_integrity.py`
    - Oprav nalezené chyby podle výpisu.

## 3. Problémy s testy a snapshoty
- [ ] **Selhávají snapshot testy**
    - Spusť: `run_and_update_snapshots.sh` pro aktualizaci snapshotů.
    - Smaž poškozené snapshoty a spusť testy znovu.
- [ ] **Chyby v a11y testech (pa11y)**
    - Spusť: `pa11y_batch_snapshots.sh` a oprav kontrast, labely, role.
    - Ověř, že badge a tlačítka mají správné aria-label.

## 4. Problémy s CI/CD a skripty
- [ ] **Chyby v CI (GitHub Actions)**
    - Projdi logy v sekci Actions na GitHubu.
    - Ověř, že všechny skripty mají správný shebang (`#!/bin/zsh`) a jsou spustitelné (`chmod +x skript.sh`).
- [ ] **Skript selhává na Macu**
    - Ověř, že používáš zsh a máš nainstalované potřebné nástroje (`brew install fdupes` apod.).

## 5. Ostatní časté problémy
- [ ] **Duplicitní nebo prázdné soubory**
    - Spusť: `cleanup_duplicates_and_empty.sh` a `cleanup_bak_files.sh`
- [ ] **Zálohy zahlcují workspace**
    - Spusť: `cleanup_backups.sh` a archivuj zálohy mimo hlavní složku.

---

> **Tip:** Pokud problém přetrvává, hledej v README, ONBOARDING nebo se ptej v chatu. Každý problém a jeho řešení dokumentuj pro ostatní!

---

*Průvodce připravil Copilot pro rychlé řešení problémů a efektivní onboarding.*
