# Troubleshooting checklist

Tento checklist ti pomůže rychle vyřešit běžné i méně časté problémy při vývoji, testování, nasazení nebo práci s workspace. Všechny příkazy jsou optimalizované pro macOS a shell zsh.

---

## 1. Problémy s virtuálním prostředím a závislostmi
- [ ] Virtuální prostředí nejde aktivovat:
  ```zsh
  source venv/bin/activate
  # Pokud venv neexistuje, vytvoř ho:
  python3 -m venv venv
  source venv/bin/activate
  ```
- [ ] Chybí závislosti nebo selže instalace:
  ```zsh
  pip install -r requirements.txt
  # Pokud selže, zkontroluj verzi pip:
  pip --version
  python --version
  ```

## 2. Problémy s databází
- [ ] Nelze se připojit k MySQL:
  - Ověř, že DB běží (`brew services list` nebo `mysql.server status`)
  - Zkontroluj přihlašovací údaje v `settings.py` a `DB_SETUP_MYSQL.md`
  - Proveď migrace:
    ```zsh
    python manage.py migrate
    ```

## 3. Selhání testů nebo CI/CD
- [ ] Testy padají na chybějící závislosti:
  - Ověř, že je aktivní venv a vše nainstalováno
- [ ] Testy padají na DB:
  - Ověř, že DB běží a je správně nastavená
- [ ] CI/CD pipeline selže:
  - Zkontroluj logy v GitHub Actions (sekce Actions)
  - Ověř, že všechny skripty mají práva pro spuštění (`chmod +x ...`)

## 4. Problémy s a11y reporty, snapshoty, exporty/importy
- [ ] Chybí nebo jsou poškozené reporty/snapshoty:
  - Spusť znovu generování:
    ```zsh
    ./pa11y_batch.sh
    ./cleanup_workspace.sh
    ```
  - Ověř, že složky a soubory existují a nejsou prázdné
- [ ] Nelze otevřít .gz snapshot/report:
  ```zsh
  gunzip nazev_souboru.html.gz
  open nazev_souboru.html
  ```

## 5. Úklid workspace a řešení konfliktů
- [ ] Workspace je zahlcený dočasnými soubory:
  ```zsh
  ./cleanup_workspace.sh
  ```
- [ ] Konflikty v Gitu:
  - Ověř, že máš commitnuté změny
  - Použij `git status`, `git diff`, `git mergetool`

## 6. Další tipy
- [ ] Pokud si nevíš rady, podívej se do README (sekce troubleshooting, onboarding, best practices)
- [ ] Využij checklisty v adresáři `tests/` pro konkrétní scénáře

---

Checklist pravidelně aktualizuj podle nových zkušeností a typických chyb v projektu.
