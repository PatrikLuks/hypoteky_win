"""
Automatizované testy pro údržbové a bezpečnostní shell skripty ve workspace.

Tento testovací runner spouští vybrané shell skripty a ověřuje, že skončí bez chyby (návratový kód 0).
Pokud některý skript selže, vypíše chybovou hlášku a selhání.

Jak rozšířit:
- Přidej další skripty do seznamu SCRIPTS_TO_TEST.
- Pro složitější testy můžeš přidat kontrolu výstupu nebo simulovat různé scénáře.

Spouštění:
$ python tests/test_scripts.py

Autor: GitHub Copilot (vysvětlující komentáře pro studenty)
"""

import subprocess
import sys
from pathlib import Path

# Seznam skriptů, které chceme testovat (relativně ke kořeni workspace)
SCRIPTS_TO_TEST = [
    "check_python_syntax.sh",
    "check_requirements_security.sh",
    "cleanup_workspace.sh",
    "check_git_clean.sh",
    "cleanup_snapshot_backups.sh",  # nově přidaný skript
    # Přidej další skripty podle potřeby
]

WORKSPACE_ROOT = Path(__file__).parent.parent.resolve()


def check_executable(script_path):
    """Ověří, že skript má nastavený spustitelný příznak."""
    if not script_path.exists():
        return False, "Skript neexistuje."
    if not script_path.stat().st_mode & 0o111:
        return False, "Skript není spustitelný (chybí chmod +x)."
    return True, ""


def check_shebang(script_path):
    """Ověří, že skript začíná správným shebangem."""
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if first_line.startswith("#!"):
                if "bash" in first_line or "zsh" in first_line:
                    return True, ""
                else:
                    return False, f"Shebang není bash/zsh: {first_line}"
            else:
                return False, "Chybí shebang (#!) na prvním řádku."
    except Exception as e:
        return False, f"Chyba při čtení: {e}"


def check_not_empty(script_path):
    """Ověří, že skript není prázdný."""
    if script_path.stat().st_size == 0:
        return False, "Skript je prázdný."
    return True, ""


def check_header(script_path):
    """Ověří, že skript obsahuje komentář s popisem a autorem v prvních 5 řádcích."""
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            lines = [f.readline() for _ in range(5)]
            joined = "".join(lines)
            if "Autor" in joined and (
                "popis" in joined or "Popis" in joined or "účel" in joined
            ):
                return True, ""
            else:
                return False, "Chybí komentář s popisem a autorem v prvních 5 řádcích."
    except Exception as e:
        return False, f"Chyba při čtení: {e}"


# Pomocná funkce (pytest ji nebude spouštět jako test)
def _test_script(script_name):
    script_path = WORKSPACE_ROOT / script_name
    print(f"\nTestuji skript: {script_path}")
    if not script_path.exists():
        print(f"[CHYBA] Skript {script_name} neexistuje!")
        return False
    # --- Nové kontroly ---
    checks = [
        (check_executable, "spustitelnost"),
        (check_shebang, "shebang"),
        (check_not_empty, "neprázdnost"),
        (check_header, "hlavička s popisem a autorem"),
    ]
    for check_func, desc in checks:
        ok, msg = check_func(script_path)
        if not ok:
            print(f"[SELHÁNÍ] {script_name}: {desc} – {msg}")
            return False
    # --- Spuštění skriptu ---
    try:
        result = subprocess.run(
            ["zsh", str(script_path)], capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"[OK] {script_name} proběhl úspěšně.")
            return True
        else:
            print(
                f"[SELHÁNÍ] {script_name} skončil s chybou (kód {result.returncode}):\n{result.stderr}"
            )
            return False
    except Exception as e:
        print(f"[VÝJIMKA] {script_name}: {e}")
        return False


def main():
    print("\n=== Testování údržbových skriptů ===")
    all_ok = True
    for script in SCRIPTS_TO_TEST:
        ok = _test_script(script)
        all_ok = all_ok and ok
    if all_ok:
        print("\nVšechny skripty proběhly úspěšně!\n")
        sys.exit(0)
    else:
        print("\nNěkteré skripty selhaly. Zkontroluj výstup výše.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
