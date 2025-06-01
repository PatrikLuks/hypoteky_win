"""
Test: Kontrola shell skriptů ve workspace
- Ověřuje, že všechny check_*, cleanup_*, fix_*.sh skripty mají správný shebang, popis a nejsou prázdné.
- Pomáhá udržet konzistenci a onboarding.
"""
import os
import glob
import pytest

SHEBANG = "#!/bin/zsh"

# Najdi všechny relevantní skripty
SCRIPT_PATTERNS = ["check_*.sh", "cleanup_*.sh", "fix_*.sh"]
SCRIPTS = []
for pattern in SCRIPT_PATTERNS:
    SCRIPTS.extend(glob.glob(pattern))

@pytest.mark.parametrize("script_path", SCRIPTS)
def test_shell_script_header_and_content(script_path):
    with open(script_path, encoding="utf-8") as f:
        lines = f.readlines()
    assert lines, f"Skript {script_path} je prázdný."
    assert lines[0].strip() == SHEBANG, f"Skript {script_path} musí začínat shebangem {SHEBANG}."
    assert any("#" in l and "skript" in l.lower() for l in lines[:5]), f"Skript {script_path} musí mít krátký popis v komentáři v prvních 5 řádcích."
