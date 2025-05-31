"""
clean_html_control_chars.py
Automaticky odstraní nebo nahradí problematické znaky (např. Windows-1250/1252, control characters) ve všech *_snapshot.html souborech v rootu projektu.

- Odstraňuje znaky s kódy: 0x8d, 0x8f, 0x9d, 0x9f (141, 143, 157, 159)
- Nahrazuje:
    0x8a (138) → Š
    0x9a (154) → š
    0x8c (140) → Č
    0x9c (156) → č
    0x91 (145) → &lsquo;
    0x92 (146) → &rsquo;
    0x93 (147) → &bdquo;
    0x94 (148) → &ldquo;
    0x95 (149) → &bull;
    0x96 (150) → &ndash;
    0x97 (151) → &mdash;
    0x98 (152) → ˜
    0x99 (153) → &trade;
    0x85 (133) → &hellip;
    0x86 (134) → &dagger;
    0x87 (135) → &Dagger;
    0x80 (128) → €
    0x82 (130) → &sbquo;
    0x84 (132) → &bdquo;
    0x83 (131) → ƒ
    0x88 (136) → ˆ
    0x89 (137) → ‰
    0x8b (139) → &lsaquo;
    0x9b (155) → &rsaquo;

- Vytvoří zálohu .bak_controlchars
- Vloží komentář na začátek souboru o provedené úpravě

Použití: python3 clean_html_control_chars.py
"""
import glob
import shutil
import os

# Mapování problematických znaků (dec: html entity nebo znak)
REPLACE_MAP = {
    128: '€', 130: '&sbquo;', 131: 'ƒ', 132: '&bdquo;', 133: '&hellip;', 134: '&dagger;', 135: '&Dagger;',
    136: 'ˆ', 137: '‰', 138: 'Š', 139: '&lsaquo;', 140: 'Č', 145: '&lsquo;', 146: '&rsquo;',
    147: '&bdquo;', 148: '&ldquo;', 149: '&bull;', 150: '&ndash;', 151: '&mdash;', 152: '˜', 153: '&trade;',
    154: 'š', 155: '&rsaquo;', 156: 'č', 157: '', 159: '', 141: '', 143: '', 8: '', 9: '\t', 10: '\n', 13: '\n'
}
# Znaky k odstranění (control chars, které nemají význam v HTML)
REMOVE_CODES = [141, 143, 157, 159]

for fname in glob.glob("*_snapshot.html"):
    with open(fname, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        # Pokud není validní UTF-8, dekóduj s chybami a oprav
        text = raw.decode("utf-8", errors="replace")
    # Záloha
    shutil.copy(fname, fname + ".bak_controlchars")
    # Projdeme znaky a nahradíme/odstraníme
    new_chars = []
    for c in text:
        code = ord(c)
        if code in REMOVE_CODES:
            continue
        if code in REPLACE_MAP:
            new_chars.append(REPLACE_MAP[code])
        elif 0 <= code < 32 and c not in ('\t', '\n', '\r'):
            continue  # Odstraníme ostatní control chars kromě tab/newline
        else:
            new_chars.append(c)
    new_text = ''.join(new_chars)
    # Komentář o úpravě
    comment = '<!-- Tento soubor byl automaticky očištěn od neplatných/control znaků skriptem clean_html_control_chars.py -->\n'
    if not new_text.lstrip().startswith('<!-- Tento soubor byl automaticky očištěn'):
        new_text = comment + new_text
    with open(fname, "w", encoding="utf-8") as f:
        f.write(new_text)
    print(f"[OK] Opraveno: {fname} (záloha: {fname}.bak_controlchars)")
print("Hotovo. Zkontrolujte validitu HTML a případně spusťte znovu check_html_validity.sh.")
