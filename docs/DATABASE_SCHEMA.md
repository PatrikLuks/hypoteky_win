# Schéma Databáze - Dokumentace

## Přehled

Aplikace používá 7 hlavních tabulek, které tvoří kompletní databázové schéma pro správu hypotéčních klientů:

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATABÁZOVÉ SCHÉMA                           │
│                                                                 │
│  auth_user ──────┐                                              │
│  (Django)        ├──→ klienti_userprofile (RBAC)               │
│                  │                                              │
│                  └──→ klienti_klient ──────┬────→ klienti_hypoteka│
│                        (56 polí, 14 šif.)  │                   │
│                                            ├────→ klienti_zmena│
│                                            ├────→ klienti_poznamka
│                                            └────→ klienti_notifikace
└─────────────────────────────────────────────────────────────────┘
```

## Detailní Popis Modelů

### 1. **auth_user** (Django Auth)
Vestavěný Django model pro autentizaci uživatelů.

**Hlavní pole:**
- `id` (Int, PK)
- `username` (Str, unique) - přihlašovací jméno
- `password` (Str, hashed) - zabezpečené heslo
- `email` (Email) - kontaktní e-mail
- `first_name` (Str) - jméno uživatele
- `is_active` (Boolean) - aktivní/neaktivní účet
- `is_staff` (Boolean) - staff přístup
- `is_superuser` (Boolean) - superuživatel

---

### 2. **klienti_userprofile** (Role-Based Access Control)
Rozšíření Django User modelu o role specifické pro aplikaci.

**Pole:**
- `id` (BigInt, PK)
- `user` (OneToOneField → auth_user) - vazba 1:1
- `role` (CharField, choices) - hodnoty: `"poradce"`, `"klient"`

**Účel:** Určuje, jaké právo má uživatel v aplikaci.

---

### 3. **klienti_klient** (Hlavní Tabulka Klientů)
Obsahuje kompletní informace o hypotéčních klientech a jejich případech.

**Počet polí:** 56 (z toho 14 šifrovaných)

#### Základní Identifikační Údaje:
- `id` (BigInt, PK)
- `jmeno` **[ENCRYPTED]** - jméno klienta
- `jmeno_index` (Str) - indexované jméno pro vyhledávání
- `datum` (DateTime) - datum vytvoření záznamu
- `user` (ForeignKey → auth_user) - přiřazený uživatel/klient

#### Finanční Pole - Krok 2 (Návrh Financování):
- `cena` (DecimalField) - cena nemovitosti
- `navrh_financovani_castka` (DecimalField) - výše hypotéky
- `vlastni_zdroj` (DecimalField) - vlastní vklady
- `ltv` (DecimalField) - LTV ratio (automaticky počítáno)

#### Workflow Pole - Krok 1 (Co Chce Financovat):
- `co_financuje` **[ENCRYPTED]** (TextField) - popis financovaného
- `splneno_co_financuje` (DateField) - datum splnění
- `deadline_co_financuje` (DateField) - termín

#### Workflow Pole - Krok 3 (Výběr Banky):
- `vyber_banky` (CharField) - vybraná banka
- `splneno_vyber_banky` (DateField)
- `deadline_vyber_banky` (DateField)

#### Workflow Pole - Krok 4 (Schválené Financování):
- `schvalena_hypoteka_castka` (DecimalField) - schválená výše
- `schvaleny_vlastni_zdroj` (DecimalField)
- `schvalene_ltv` (DecimalField)
- `splneno_schvalene_financovani` (DateField)
- `deadline_schvalene_financovani` (DateField)

#### Workflow Pole - Kroky 5-15 (Texty s Deadliny):
Následující 11 kroků má stejnou strukturu - TextField (šifrovaný) + splneno + deadline:

- **Krok 5:** `priprava_zadosti`, `splneno_priprava_zadosti`, `deadline_priprava_zadosti`
- **Krok 6:** `kompletace_podkladu`, `splneno_kompletace_podkladu`, `deadline_kompletace_podkladu`
- **Krok 7:** `podani_zadosti`, `splneno_podani_zadosti`, `deadline_podani_zadosti`
- **Krok 8:** `odhad`, `splneno_odhad`, `deadline_odhad`
- **Krok 9:** `schvalovani`, `splneno_schvalovani`, `deadline_schvalovani`
- **Krok 10:** `priprava_uverove_dokumentace`, `splneno_priprava_uverove_dokumentace`, `deadline_priprava_uverove_dokumentace`
- **Krok 11:** `podpis_uverove_dokumentace`, `splneno_podpis_uverove_dokumentace`, `deadline_podpis_uverove_dokumentace`
- **Krok 12:** `priprava_cerpani`, `splneno_priprava_cerpani`, `deadline_priprava_cerpani`
- **Krok 13:** `cerpani`, `splneno_cerpani`, `deadline_cerpani`
- **Krok 14:** `zahajeni_splaceni`, `splneno_zahajeni_splaceni`, `deadline_zahajeni_splaceni`
- **Krok 15:** `podminky_pro_splaceni`, `splneno_podminky_pro_splaceni`, `deadline_podminky_pro_splaceni`

#### Speciální Pole:
- `duvod_zamitnuti` **[ENCRYPTED]** - důvod zamítnutí (je-li vyplněno, hypotéka je zamítnutá)
- `aktualni_krok` (SmallInt, nullable) - číslo aktuálního kroku

#### Šifrovaná Pole (14 Celkem):
1. `jmeno`
2. `co_financuje`
3. `duvod_zamitnuti`
4. `priprava_zadosti`
5. `kompletace_podkladu`
6. `podani_zadosti`
7. `odhad`
8. `schvalovani`
9. `priprava_uverove_dokumentace`
10. `podpis_uverove_dokumentace`
11. `priprava_cerpani`
12. `cerpani`
13. `zahajeni_splaceni`
14. `podminky_pro_splaceni`

---

### 4. **klienti_hypoteka** (Workflow Historie)
Zaznamenává průchod klienta jednotlivými kroky workflow.

**Pole:**
- `id` (BigInt, PK)
- `klient` (ForeignKey → klienti_klient, cascade)
- `krok` (SmallIntegerField, choices 1-15) - číslo kroku workflow
- `datum` (DateTimeField, auto_now_add) - čas zaznamenání
- `poznamka` (TextField, blank=True) - volná poznámka k tomuto kroku

**Vztah:** 1 Klient : N Hypoteka (historické záznamy)

**Použití:** Audit trail a sledování postupu hypotéky

---

### 5. **klienti_zmena** (Audit Log)
Zaznamenává všechny změny u klientů pro auditní účely.

**Pole:**
- `id` (BigInt, PK)
- `klient` (ForeignKey → klienti_klient, cascade) 
- `popis` **[ENCRYPTED]** (TextField) - popis změny
- `created` (DateTimeField, auto_now_add) - čas změny
- `author` (CharField, max_length=100) - autor změny (jméno/username)

**Vztah:** 1 Klient : N Zmena

**Důvod šifrování:** Audit log může obsahovat citlivé údaje

---

### 6. **klienti_poznamka** (Poznámky ke Klientům)
Umožňuje přidávat volné poznámky k jednotlivým klientům.

**Pole:**
- `id` (BigInt, PK)
- `klient` (ForeignKey → klienti_klient, cascade)
- `text` **[ENCRYPTED]** (TextField) - obsah poznámky
- `created` (DateTimeField, auto_now_add) - čas vytvoření
- `author` (CharField, max_length=100) - autor poznámky

**Vztah:** 1 Klient : N Poznamka

**Příklad:** Osobní poznámky z telefonů, osobních schůzek atp.

---

### 7. **klienti_notifikace** (Email Log)
Zaznamenává odesílané email notifikace.

**Pole:**
- `id` (BigInt, PK)
- `prijemce` (EmailField) - na jakou adresu byl e-mail odeslán
- `typ` (CharField, choices) - typ notifikace: `"deadline"`, `"stav"`, `"zamítnutí"`
- `klient` (ForeignKey → klienti_klient, null=True, blank=True)
- `datum` (DateTimeField, auto_now_add) - čas odeslání
- `obsah` (TextField, blank=True) - obsah e-mailu
- `uspesne` (BooleanField, default=True) - úspěšnost odeslání

**Vztah:** 1 Klient : N Notifikace

**Účel:** Sledování e-mailů odeslaných systémem

---

## Definice Relací (1:N)

| Vztah | Parent | Child | Popis |
|-------|--------|-------|-------|
| **Uživatel → Profil** | auth_user | klienti_userprofile | 1:1 - Každý uživatel má přesně jednu roli |
| **Uživatel → Klient** | auth_user | klienti_klient | 1:N - Jeden uživatel (poradce) spravuje více klientů |
| **Klient → Workflow** | klienti_klient | klienti_hypoteka | 1:N - Každý klient má historii kroků |
| **Klient → Audit** | klienti_klient | klienti_zmena | 1:N - Všechny změny vázány na klienta |
| **Klient → Poznámky** | klienti_klient | klienti_poznamka | 1:N - Více poznámek na jednoho klienta |
| **Klient → Notifikace** | klienti_klient | klienti_notifikace | 1:N - Více notifikací na jednoho klienta |

---

## Šifrování Dat

**Knihovna:** `django-encrypted-model-fields` (Fernet symetrické šifrování)

**Šifrovaná pole:**
- Citlivé osobní údaje: `jmeno`
- Finanční/obchodní údaje: `co_financuje`, `duvod_zamitnuti`
- Workflow texty: 11 stepů (kroky 5-15)
- Audit log: `popis`
- Poznámky: `text`

**Bezpečnost:** Data jsou šifrována na úrovni databáze, v aplikaci se dešifrují v paměti.

---

## Indexy a Constraints

**Indexované pole:**
- `klienti_klient.jmeno_index` - umožňuje rychlé vyhledávání klientů

**Omezení ON_DELETE:**
- `cascade` - pokud se smaže klient, smažou se všechny jeho záznamy (workflow, změny, poznámky)
- `SET_NULL` - notifikace zůstávají, ale vazba na klienta je nastavena na NULL

---

## SQL Struktura

### Tabulka klienti_klient
```sql
CREATE TABLE klienti_klient (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    jmeno VARBINARY(255) NOT NULL,  -- Encrypted
    jmeno_index VARCHAR(255) INDEXED,
    datum DATETIME AUTO_SET,
    co_financuje LONGBLOB,  -- Encrypted
    cena DECIMAL(12, 2),
    navrh_financovani_castka DECIMAL(12, 2),
    vlastni_zdroj DECIMAL(12, 2),
    ltv DECIMAL(5, 2),
    vyber_banky VARCHAR(255),
    schvalena_castka DECIMAL(12, 2),
    -- ... (44 dalších polí)
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES auth_user(id),
    CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci
);
```

---

## Dotazy a Příklady

### Získání Klienta s Kompletním Workflow
```python
from klienti.models import Klient

klient = Klient.objects.prefetch_related('hypoteka_set', 'zmena_set').get(id=1)
```

### Audit Trail Klienta
```python
zmeny = klient.zmeny.all().order_by('-created')
```

### E-maily Odesílané u Klienta
```python
notifikace = klient.notifikace.filter(typ='stav')
```

### Aktivní Klienti (Bez Zamítnutí)
```python
aktivni = Klient.objects.filter(duvod_zamitnuti__isnull=True)
```

---

## Poznámky k Designu

1. **14 Šifrovaných Polí** - Zajišťují GDPR compliance a bezpečnost citlivých údajů
2. **15 Workflow Kroků** - Odpovídají reálnému procesu hypotečního poradenství
3. **Elastické Deadline** - Každý krok má vlastní deadline a datum splnění
4. **Audit Trail** - Všechny změny jsou zaznamenávány v `zmena` tabulce
5. **Role-Based** - UserProfile odděluje uživatele od jejich rol
6. **Cascade Delete** - Smazání klienta čistí všechny související záznamy

---

## ER Diagram

Podrobný ER diagram s TikZ grafikou je součástí práce v `hypoteky.tex` - sekce "Databáze" → "Schéma databáze -- ER diagram".

