"""
clean_html_aggressive.py
Odstraní všechny neplatné/control znaky z HTML snapshotů:
- Všechny znaky s kódem < 32 (kromě \n, \t)
- Všechny znaky s kódem 128–159 (včetně 140, 141, 147, 153, 154, 155 atd.)
- Nahrazuje podle mapy, jinak odstraní
- Vloží komentář o úpravě
Použití: python3 clean_html_aggressive.py
"""
import glob
import shutil

# Mapování problematických znaků na entity nebo znaky
REPLACE_MAP = {
    128: '€', 130: '&sbquo;', 131: 'ƒ', 132: '&bdquo;', 133: '&hellip;', 134: '&dagger;', 135: '&Dagger;',
    136: 'ˆ', 137: '‰', 138: 'Š', 139: '&lsaquo;', 140: 'Č', 145: '&lsquo;', 146: '&rsquo;',
    147: '&bdquo;', 148: '&ldquo;', 149: '&bull;', 150: '&ndash;', 151: '&mdash;', 152: '˜', 153: '&trade;',
    154: 'š', 155: '&rsaquo;', 156: 'č',
}

for fname in glob.glob("*_snapshot.html"):
    with open(fname, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("utf-8", errors="replace")
    shutil.copy(fname, fname + ".bak_aggressive")
    new_chars = []
    for c in text:
        code = ord(c)
        # Odstranit všechny control chars < 32 kromě \n, \t
        if code < 32 and c not in ('\n', '\t'):
            continue
        # Nahraď podle mapy, jinak odstraň všechny 128–159
        if 128 <= code <= 159:
            if code in REPLACE_MAP:
                new_chars.append(REPLACE_MAP[code])
            # Pokud není v mapě, odstraníme
            continue
        new_chars.append(c)
    new_text = ''.join(new_chars)
    comment = '<!-- Tento soubor byl AGRESIVNĚ očištěn od všech neplatných/control znaků skriptem clean_html_aggressive.py -->\n'
    if not new_text.lstrip().startswith('<!-- Tento soubor byl AGRESIVNĚ očištěn'):
        new_text = comment + new_text
    with open(fname, "w", encoding="utf-8") as f:
        f.write(new_text)
    print(f"[OK] Agresivně opraveno: {fname} (záloha: {fname}.bak_aggressive)")
print("Hotovo. Spusť znovu check_html_validity.sh pro ověření.")
