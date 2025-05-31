#!/usr/bin/env python3
"""
Skript pro odstranění neplatných (neviditelných) znaků z HTML snapshotů a volitelnou náhradu <nav>/<canvas> za <div>.
Použití: python3 clean_html_snapshots.py
"""
import os
import re

# Cesta ke složce se snapshoty
SNAPSHOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Regulární výraz pro neplatné znaky (ASCII 127-159, 136, 140, 141, 147, 153, 154, 155)
INVALID_CHARS = re.compile(r"[\x88\x8c\x8d\x93\x99\x9a\x9b\x7f-\x9f]")

# Tagy, které lze nahradit (volitelné)
REPLACE_TAGS = {
    'nav': 'div',
    'canvas': 'div',
}

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    # Odstranění neplatných znaků
    cleaned = INVALID_CHARS.sub('', content)
    # Volitelně: nahrazení tagů <nav> a <canvas> za <div>
    for tag, replacement in REPLACE_TAGS.items():
        cleaned = re.sub(fr'<{tag}(\s|>)', fr'<{replacement}\1', cleaned)
        cleaned = re.sub(fr'</{tag}>', fr'</{replacement}>', cleaned)
    # Záloha
    backup = filepath + '.bak_clean'
    with open(backup, 'w', encoding='utf-8') as f:
        f.write(content)
    # Uložení
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    print(f"Opraveno: {os.path.basename(filepath)} (záloha v {os.path.basename(backup)})")

def main():
    for fname in os.listdir(SNAPSHOT_DIR):
        if fname.endswith('_snapshot.html'):
            clean_file(os.path.join(SNAPSHOT_DIR, fname))

if __name__ == '__main__':
    main()
