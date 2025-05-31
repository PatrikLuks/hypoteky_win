# 🧑‍💻 ONBOARDING – rychlý start pro nové vývojáře

Tento soubor slouží jako stručný rozcestník pro nové členy týmu i studenty. Najdeš zde nejdůležitější kroky, checklisty a odkazy pro efektivní práci v projektu.

---

## 🚀 Rychlý start

1. **Klonuj repozitář a přejdi do složky:**
   ```zsh
   git clone https://github.com/PatrikLuks/hypoteky_django.git
   cd hypoteky
   ```
2. **Vytvoř a aktivuj virtuální prostředí:**
   ```zsh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Nainstaluj závislosti:**
   ```zsh
   pip install -r requirements.txt
   pip install playwright
   python -m playwright install --with-deps
   ```
4. **Nastav MySQL a proveď migrace:**
   - Viz `DB_SETUP_MYSQL.md`
   - 
   ```zsh
   python manage.py migrate
   ```
5. **Spusť server:**
   ```zsh
   python manage.py runserver
   ```
6. **Spusť testy a údržbu workspace:**
   ```zsh
   ./run_all_checks.sh
   ```

---

## 🧑‍🔬 Rychlá kontrola prostředí (doporučeno)

Před prvním vývojem spusť skript:

```zsh
source .venv/bin/activate
./quick_check_onboarding.sh
```

Skript ověří:
- Aktivaci virtuálního prostředí
- Instalaci klíčových balíčků (django, pytest, playwright)
- Připojení k databázi a migrace
- Základní testy

Pokud vše projde, můžeš bezpečně pokračovat v práci!

---

## 🧪 Jak přidat nový skript/test (best practices)
- Inspiruj se soubory:
  - `klienti/scripts/klient_user_overview.py` (+ test, CSV export)
  - `klienti/scripts/rozdel_klienty_mezi_uzivatele.py` (+ test, dry-run, CSV export)
- Hlavní logiku vždy dávej do funkce, kterou lze importovat a testovat.
- Pro CLI použij `argparse` a umožni např. `--csv`, `--dry-run`.
- Testuj přímo funkci, ne přes subprocess.
- Pro export do CSV použij `csv` a `tempfile` v testu.

---

## ✅ Checklist pro přispěvatele
- [ ] Hlavní logika je v samostatné funkci (importovatelná, testovatelná)
- [ ] Skript podporuje CLI parametry (`--csv`, `--dry-run`, `--help`)
- [ ] Existuje odpovídající test v `tests/`, který ověřuje i edge-case scénáře
- [ ] Testy procházejí lokálně i v CI
- [ ] Kód je okomentovaný a srozumitelný
- [ ] Pokud skript mění data, je k dispozici i bezpečný režim (dry-run)
- [ ] Pokud skript exportuje data, je ověřen i obsah exportu

---

## 📚 Důležité odkazy
- [README.md](README.md) – detailní dokumentace, troubleshooting, workflow
- [DB_SETUP_MYSQL.md](DB_SETUP_MYSQL.md) – nastavení databáze
- [E2E_TESTING_CHECKLIST.md](E2E_TESTING_CHECKLIST.md) – checklist pro e2e testy
- [README_snapshot_a11y_management.md](README_snapshot_a11y_management.md) – správa snapshotů a a11y
- `klienti/scripts/` – vzorové skripty
- `klienti/tests/` – vzorové testy

---

> Pokud narazíš na problém, začni od checklistu a logů, nebo se ptej v týmu. Hodně štěstí!
