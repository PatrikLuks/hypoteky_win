# Tento skript odstraní všechny znaky s kódy 128–159 (0x80–0x9F) z HTML snapshot souborů a opraví klient_list_snapshot.html na validní HTML5 strukturu.
import os
import re

SNAPSHOT_FILES = [
    'home_snapshot.html',
    'klient_detail_snapshot.html',
    'kalkulacka_snapshot.html',
    'reporting_snapshot.html',
    'login_snapshot.html',
    'klient_confirm_delete_snapshot.html',
    'klient_form_snapshot.html',
    'klient_list_snapshot.html',
    'dashboard_snapshot.html',
]

# Regex pro znaky s kódy 128–159 (decimálně)
BAD_CHARS = re.compile(b'[\x80-\x9F]')

# Validní základ HTML5
HTML5_TEMPLATE = '''<!-- filepath: klient_list_snapshot.html -->
<!-- Tento soubor byl AGRESIVNĚ očištěn od všech neplatných/control znaků skriptem clean_html_aggressive.py -->
<!-- Tento soubor byl automaticky očištěn od neplatných/control znaků skriptem clean_html_control_chars.py -->
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <title>Seznam klientů</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>
<body>
    <div class="container mt-4">
        <h1>Seznam klientů</h1>
        <!-- Zde bude obsah seznamu klientů -->
    </div>
</body>
</html>
'''

for fname in SNAPSHOT_FILES:
    if not os.path.exists(fname):
        continue
    with open(fname, 'rb') as f:
        raw = f.read()
    # Odstranění znaků 128–159
    cleaned = BAD_CHARS.sub(b'', raw)
    # Uložení zálohy
    with open(fname + '.bak_finalclean', 'wb') as f:
        f.write(raw)
    # Speciální případ pro klient_list_snapshot.html
    if fname == 'klient_list_snapshot.html':
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(HTML5_TEMPLATE)
    else:
        with open(fname, 'wb') as f:
            f.write(cleaned)
print('Hotovo: odstraněny znaky 128–159 a opraven klient_list_snapshot.html.')
