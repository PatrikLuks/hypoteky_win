# DB Migration Checklist

> Bezpečnostní a procesní checklist pro změny v databázi (Django/MySQL)
> Doporučeno použít při každé úpravě schématu, migraci nebo zásahu do produkce.

---

## 1. Příprava
- [ ] Zálohuj aktuální databázi (dump, snapshot, export).
- [ ] Ověř, že máš přístup k produkční i testovací DB.
- [ ] Zkontroluj, že máš aktuální verzi kódu a migrací.

## 2. Analýza změn
- [ ] Projdi všechny plánované změny (modely, migrace, ruční SQL skripty).
- [ ] Ověř, že změny jsou zpětně kompatibilní (pokud to projekt vyžaduje).
- [ ] Zkontroluj, zda změny neovlivní integrace, reporting, exporty.

## 3. Testování
- [ ] Proveď migrace na testovací DB a spusť všechny testy.
- [ ] Ověř, že data zůstala konzistentní (počty řádků, klíčová data, relace).
- [ ] Otestuj edge-case scénáře (NULL hodnoty, cizí klíče, unikáty).

## 4. Nasazení
- [ ] Informuj tým o plánované změně a možném výpadku.
- [ ] Proveď migraci v produkci mimo špičku.
- [ ] Sleduj logy a výstup migrace (chyby, warningy).

## 5. Kontrola po migraci
- [ ] Ověř, že aplikace funguje (login, CRUD, exporty, reporting).
- [ ] Zkontroluj integritu dat (např. pomocí `check_db_integrity.py`).
- [ ] Projdi monitoring a alerty (výkon, chybovost).

---

> **Tip:** Po každé větší změně aktualizuj dokumentaci a sdílej zkušenosti s týmem.

---

*Checklist připravil Copilot pro bezpečnější a efektivnější správu databáze.*
