# WORKSPACE_STATUS.md

> Rychlý přehled stavu projektu, checklistů a klíčových skriptů pro bezpečné nasazení a onboarding.

---

## 1. Stav hlavních oblastí

| Oblast                | Stav      | Poznámka / Odkaz |
|-----------------------|-----------|-----------------|
| Bezpečnost & compliance | ⬜         | [REAL_DEPLOYMENT_ACTION_PLAN.md](REAL_DEPLOYMENT_ACTION_PLAN.md) |
| Testování (unit/e2e)   | ⬜         | [E2E_TESTING_CHECKLIST.md](E2E_TESTING_CHECKLIST.md) |
| Snapshoty & a11y       | ⬜         | [README_snapshot_a11y_management.md](README_snapshot_a11y_management.md) |
| Zálohování & obnova    | ⬜         | [DB_MIGRATION_CHECKLIST.md](DB_MIGRATION_CHECKLIST.md) |
| Dokumentace & onboarding | ⬜         | [ONBOARDING.md](ONBOARDING.md) |

> Vyplň stav (✅ hotovo, ⬜ čeká, ⚠️ pozor) podle aktuální situace v projektu.

---

## 2. Klíčové skripty a workflow

- Údržba: `run_all_maintenance.sh`, `full_workspace_maintenance.sh`
- Úklid: `cleanup_bak_files.sh`, `cleanup_backups.sh`, `cleanup_duplicates_and_empty.sh`
- Testy: `run_e2e_with_server.sh`, `check_pytest_env.sh`, `check_current_snapshots.sh`
- Bezpečnost: `check_requirements_security.sh`, `safety scan`
- Snapshoty: `run_and_update_snapshots.sh`, `compare_snapshots.sh`
- Přístupnost: `pa11y_batch_snapshots.sh`, `pa11y_batch_csv.sh`
- Zálohování: `backup_workspace.sh`, `restore_workspace_from_backup.sh`

---

## 3. Doporučený postup před nasazením

1. Projdi všechny checklisty a označ splněné body.
2. Spusť údržbové a testovací skripty.
3. Ověř výstup CI/CD a oprav případné chyby.
4. Zálohuj data a snapshoty.
5. Proveď pilotní provoz a audit.
6. Teprve poté proveď ostré nasazení.

---

> Tento dashboard pravidelně aktualizuj a sdílej s týmem. Pomůže udržet projekt v kondici a onboarding rychlý a přehledný.
