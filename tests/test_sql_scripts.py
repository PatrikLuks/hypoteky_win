"""
Test: Kontrola SQL skriptů ve workspace
- Ověřuje, že všechny .sql skripty mají popis, nejsou prázdné a nezačínají nebezpečnými příkazy.
- Pomáhá udržet bezpečnost a onboarding.
"""

import glob
import os

import pytest

DANGEROUS = ("drop ", "delete ", "truncate ", "alter ")

SQL_SCRIPTS = glob.glob("*.sql")


@pytest.mark.parametrize("sql_path", SQL_SCRIPTS)
def test_sql_script_header_and_safety(sql_path):
    with open(sql_path, encoding="utf-8") as f:
        lines = [l.strip().lower() for l in f if l.strip()]
    assert lines, f"SQL skript {sql_path} je prázdný."
    assert lines[0].startswith("--") or lines[0].startswith(
        "#"
    ), f"SQL skript {sql_path} musí začínat komentářem s popisem."
    for l in lines[:5]:
        for danger in DANGEROUS:
            assert not l.startswith(
                danger
            ), f"SQL skript {sql_path} začíná nebezpečným příkazem: {l}"
