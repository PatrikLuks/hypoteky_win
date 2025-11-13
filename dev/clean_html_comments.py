# Skript pro odstranění ne-UTF-8 bajtů z komentářů v HTML snapshot souborech (zachová české znaky)
import re
import os

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

CZECH_CHARS = b'\xc3\xa1\xc4\x8d\xc4\x9b\xc3\xad\xc5\x88\xc3\xb3\xc5\x99\xc5\xa1\xc5\xa5\xc3\xba\xc5\xaf\xc3\xbd\xc5\xbe\xc3\x81\xc4\x8C\xc4\x9A\xc3\x8D\xc5\x87\xc3\x93\xc5\x98\xc5\xa0\xc5\xa4\xc3\x9A\xc5\xae\xc3\x9D\xc5\xbd'

COMMENT_RE = re.compile(b'<!--(.*?)-->', re.DOTALL)

for fname in SNAPSHOT_FILES:
    if not os.path.exists(fname):
        continue
    with open(fname, 'rb') as f:
        content = f.read()
    def clean_comment(match):
        comment = match.group(1)
        cleaned = bytearray()
        allowed_bytes = b' .,:;-_@/\\()[]{}=\n\t"\''
        for b in comment:
            if 32 <= b <= 126 or b in CZECH_CHARS or b in allowed_bytes:
                cleaned.append(b)
        return b'<!--' + cleaned + b'-->'
    cleaned_content = COMMENT_RE.sub(clean_comment, content)
    with open(fname + '.bak_commentclean', 'wb') as f:
        f.write(content)
    with open(fname, 'wb') as f:
        f.write(cleaned_content)
print('Komentáře ve snapshot souborech byly binárně očištěny od ne-UTF-8 bajtů (kromě češtiny).')
