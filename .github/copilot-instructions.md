<!-- Tento soubor slouží k zadání workspace-specifických instrukcí pro GitHub Copilot. Další informace: https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->
- Uživatel je chudý, ale ambiciózní student, který si nemůže dovolit jiné nástroje než Copilot, proto na Copilota spoléhá při cestě za lepší budoucností. Copilot by měl být maximálně nápomocný, trpělivý a poskytovat jasné, srozumitelné rady a návody.
- Tento soubor pravidelně aktualizuj podle vývoje projektu a potřeb uživatele.
- Nezapomeň, že uživatel je student, který se učí programovat a potřebuje detailní a trpělivé vysvětlení každého kroku, včetně příkladů a komentářů v kódu.
Is a high-performance individual on a journey to become a 10× stronger version of themselves — strategic, mentally unshakable, and an effective reality creator. They want ChatGPT to function as their personal training system: teacher, sparring partner, growth architect, and consultant.

Is building a productivity system as an operating system for the mind, using tools like Notion, dashboards, Pomodoro tracking, and GitHub as the brain of operations.

Aims to master themselves, chaos, and key domains such as business, markets, investing, compliance, Web3, blockchain, AI, SSI, and digital identity.

Uživatel chce, aby mu ChatGPT poskytoval co nejlepší, nejširší, nejobsáhlejší, nejpodrobnější a nejchytřejší odpovědi – chce, aby se ChatGPT ukázal v tom nejlepším.

Uživatel si přeje detailně naučit compliance a vytvořit vlastní checklist jako junior IT konzultant.

Uživatel chce detailně porozumět digitální identitě, včetně konceptů jako SSI (Self-Sovereign Identity), Web3, tokenizace identity a decentralizované identifikátory (DID). Tyto oblasti se ve škole moc neprobírají, takže očekává kompletní výuku od ChatGPT.

Wants a personal growth roadmap structured as a weekly course, covering topics such as mental models, digital competencies, productivity, negotiation, compliance, business, and personal development.

Uživatel chce získat maximum z chatu a naučit se vše obsažené v tématu „životní dovednosti, které škola neučí“, včetně vytvoření osobního vzdělávacího plánu, který je praktický, efektivní a vede k neignorovatelnosti.

Uživatel se chce naučit více o mentálních modelech a digitálních kompetencích & produktivitě.

Is an 18-year-old student in their third year at a prestigious school and will graduate in a year. They want to pass their graduation exams, become powerful and wealthy, and are interested in business, economics, investing, markets, assets, and taxes. They seek money, experiences, people, and knowledge, and aim to grow as quickly as possible.

Is skilled in programming (Python, C, C++), databases, graphics, modeling, networking, Linux, Apple technologies, Docker, and other IT skills.

Uses OneDrive, Microsoft licenses, iCloud, Apple Calendar and Reminders. Their Focus mode is set based on their school location. They do not have chaotic folders.

Uživatel ve škole často používá GitHub.

Uživatel se chce naučit perfektně využívat principy hry s dlouhým časovým horizontem, specifické znalosti, kompenzaci a páku podle Navalovy filozofie.

Wants ChatGPT to provide long-term learning in the areas of artificial intelligence, blockchain, and cybersecurity.

Uživatel má MacBook Air 2020 s procesorem i3 a 256 GB úložištěm. Používá macOS a má AirPods 2. generace a iPhone SE 2020 (také 256 GB). Doma má Synology NAS.

Uživatel má školní licence na software jako Microsoft 365, JetBrains produkty a Packet Tracer.

Uživatel studuje obor Informační a komunikační technologie se zaměřením na počítačové sítě a programování. Ve škole se věnují i grafice, elektrotechnice, mikroprocesorům a programují v jazycích jako C, Python, SQL, HTML a mnoho dalších.

Uživatel chce hluboký osobní rozvojový plán zahrnující jasné myšlení, strategii, komunikaci a adaptabilitu, s důrazem na praktické, reálné dovednosti a široké mentální modely.

Uživatel chce jít více do hloubky v oblasti kognitivního tréninku a soustředění (deep work, Pomodoro, mindfulness).

Uživatel chce jít do hloubky v tématu mentální odolnosti, strukturování pracovního týdne na hlubokou práci a překonávání vnitřního odporu, například z práce, která vyvolává trauma nebo nepohodlí.

Uživatel chce osobní krizový protokol na momenty odporu, vnitřního chaosu nebo traumatu spojeného s prací – konkrétní, praktický krok za krokem plán, bez klišé.

Uživatel chce vytvořit osobní „mentální manifest“ – přehled nových přesvědčení, návyků a nouzových vět jako bitevní plán pro překonávání odporu, růst a budování mentální síly.

Uživatel se chce naučit a připravit na pozici CEO, včetně dovedností, mindsetu a vedení na vysoké úrovni.

Prefers responses in Czech.;  pečlivě uloz do paměti

# Kontext projektu

Tento projekt je moderní webová aplikace pro správu hypoték, určená finančním poradcům. Umožňuje detailní evidenci a správu případů klientů podle přesně definovaného workflow (15 kroků od záměru klienta po čerpání a splácení). Backend je postaven na Django, databáze je MySQL.

## Workflow hypotéky (kroky)

1. Jméno klienta
2. Co chce klient financovat
3. Návrh financování
4. Výběr banky
5. Příprava žádosti
6. Kompletace podkladů
7. Podání žádosti
8. Odhad
9. Schvalování
10. Příprava úvěrové dokumentace
11. Podpis úvěrové dokumentace
12. Příprava čerpání
13. Čerpání
14. Zahájení splácení
15. Podmínky pro splacení

Každý klient prochází těmito kroky. Krok je vždy jednoznačně identifikovatelný a má svůj stav, datum, případně poznámku.

---

# Hlavní cíle a doporučení pro generovaný kód
Aktuální cíle projektu – na co se má Copilot při generování kódu zaměřit:

1. Pokrytí klíčových funkcí testy a zvýšení spolehlivosti
- Doplň unit a integrační testy pro všechny modely, pohledy a API endpointy (včetně edge-case scénářů a chybových stavů).
- Zaměř se na testování importu/exportu klientů a hypoték (CSV, XLSX, PDF), včetně validace dat a chybových hlášek.
- Otestuj generování, odesílání a logování e-mailových notifikací (např. deadliny, změny stavu, zamítnutí).
- Přidej snapshot testy pro UI (různé velikosti obrazovky, tmavý/světlý režim) a e2e testy (Selenium/Playwright) pro hlavní workflow.
- Ověř, že různé role mají správný přístup ke všem klíčovým view a API (poradce, admin, manažer).

2. Pokrytí edge-case scénářů a chybových stavů
- Doplň testy pro importy/exporty s nevalidními daty, duplicitami, chybějícími poli, špatným formátem.
- Otestuj chování API a UI při selhání externích služeb (e-mail, export, DB).
- Ověř robustnost notifikací (např. neexistující e-mail, špatný deadline).

3. Rozšíření e2e a a11y testů
- Přidej e2e testy (Playwright/Selenium) pro hlavní workflow (vytvoření klienta, změna stavu, export, notifikace).
- Rozšiř a11y testy (axe, pa11y) na všechny klíčové view (formuláře, reporting, detail klienta).
- Ověř ovládání klávesnicí, kontrast, popisky, správné role.

4. Testování a dokumentace automatizovaných reportů a e-mailů
- Otestuj generování a doručování reportů e-mailem (včetně edge-case: prázdná data, velký objem).
- Ověř logování a auditní stopu pro všechny automatizované akce.
- Přidej testy pro šablony e-mailů (obsah, lokalizace, přílohy).

5. Rozšíření a aktualizace dokumentace
- Přidej konkrétní příklady testování UI, reportingu, importu/exportu, CI/CD do README.
- Sepiš best practices pro psaní testů, validaci vstupů, rozšiřování projektu.
- Přidej onboarding sekci pro nové vývojáře (jak spustit projekt, testy, CI/CD).

6. Ověření a rozšíření bezpečnostních testů
- Otestuj 2FA v reálném přihlášení (OTP, recovery).
- Ověř šifrování citlivých polí a auditní logování všech změn.
- Pravidelně kontroluj a testuj oprávnění a role (včetně pokusů o zneužití).

7. Příprava na rozšiřitelnost a integrace
- Otestuj export deadlinů do iCal/Google/Outlook (validita, použitelnost).
- Ověř REST API pro integraci s externími systémy (autorizace, limity, edge-case).
- Připrav architekturu na snadné přidávání nových modulů (modulární struktura, jasné rozhraní).

8. Uživatelská zkušenost, přístupnost a moderní UI
- Otestuj a dolaď responsivitu UI (tabulky, grafy, formuláře) pro mobily, tablety i desktop.
- Přidej možnost přepínání tmavého/světlého režimu a ověř jeho funkčnost testy.
- Ověř přístupnost (a11y): role, aria-label, alt popisky, kontrast, ovládání klávesnicí.
- Přidej testy pro automatizované reporty a jejich zasílání e-mailem.

9. Dokumentace, best practices a onboarding
- Rozšiř README o konkrétní příklady testování UI, reportingu, importu/exportu a CI/CD.
- Sepiš doporučení pro vývojáře: jak psát nové testy, jak rozšiřovat projekt, jak validovat vstupy.
- Přidej ukázky edge-case scénářů a best practices pro bezpečnost a správu dat.

10. Integrace, automatizace a rozšiřitelnost
- Otestuj export deadlinů do iCal/Google/Outlook kalendáře (validita a použitelnost souborů).
- Nastav a dokumentuj CI/CD pipeline (např. GitHub Actions) pro automatizované spouštění testů a kontrolu kvality.
- Ověř REST API: autorizace, chybové stavy, limity, edge-case scénáře.
- Připrav projekt na snadné rozšíření (modulární architektura, jasné rozhraní mezi komponentami).

11. Analytika a reporting
- Otestuj generování pokročilých statistik (trendy, úspěšnost podle banky, průměrná doba schválení, heatmapy).
- Ověř správnost a bezpečnost automatizovaných reportů zasílaných e-mailem.

12. Důraz na čistotu, čitelnost a komentáře v kódu
- Piš kód v češtině tam, kde je to vhodné (modely, proměnné, komentáře).
- Dodržuj best practices Django a Pythonu, používej typové anotace a pojmenované konstanty.
- Vždy přidávej komentáře a příklady pro studenty, kteří se učí programovat.


Tyto cíle a doporučení vycházejí z aktuálního stavu projektu a zaměřují se na zvýšení kvality, bezpečnosti, použitelnosti a rozšiřitelnosti aplikace. Pomohou ti nejen při studiu, ale i při budoucím rozvoji projektu.

## Uživatelská zkušenost a UI

- Implementuj e-mailové notifikace pro klienty i poradce (deadliny, změny stavu, zamítnutí).
- Dbej na plně responsivní design (tabulky, grafy, formuláře).
- Přidej možnost přepínání tmavého/světlého režimu.

## Funkcionalita

- U každého klienta eviduj historii změn (kdo, kdy, co upravil).
- Umožni přidávat poznámky, úkoly a připomínky ke klientovi.
- Implementuj export/import klientů a hypoték do/z CSV/XLSX.
- Umožni pokročilé filtrování a vyhledávání klientů (stav, banka, částka, datum atd.).

## Bezpečnost a správa

- Vytvoř auditní log všech důležitých akcí v systému.
- Implementuj role a oprávnění (poradce, administrátor, manažer).
- Přidej dvoufaktorovou autentizaci.

## Analytika a reporting

- Zobrazuj pokročilé statistiky (trendy, úspěšnost podle banky, průměrná doba schválení, heatmapy).
- Umožni automatizované reporty zasílané e-mailem.

## Integrace

- Vytvoř REST API pro napojení na externí systémy.
- Umožni export deadlinů do Google/Outlook kalendáře.

---

# Další doporučení pro Copilot

- Preferuj čistý, čitelný a dobře komentovaný kód.
- Dodržuj best practices Django a Pythonu.
- Používej pojmenované konstanty a typové anotace.
- Vždy validuj vstupy a ošetřuj chybové stavy.
- Piš testy pro klíčové části logiky (unit/integration).
- Respektuj bezpečnostní zásady (ochrana dat, autentizace, autorizace).
- Kód piš v češtině, pokud je to vhodné (např. názvy modelů, proměnných, komentáře).
- Při návrhu UI používej moderní CSS frameworky (např. Tailwind, Bootstrap).
---

# Instrukce pro Copilot ohledně vedení uživatele

- Uživatel je velmi nadějný student na prestižní škole a nemusí vždy znát následující krok.
- Vysvětluj navrhované kroky, postupy a doporučení
- Nabízej konkrétní rady, jak pokračovat, pokud uživatel neví, co má dělat dál.
- Pokud je to vhodné, přidej krátké vysvětlení, proč je daný krok důležitý.

---

