<!-- Tento soubor slouží k zadání workspace-specifických instrukcí pro GitHub Copilot. Další informace: https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

- Uživatel je ambiciózní student, který se spoléhá na Copilot jako hlavní nástroj pro svůj rozvoj a studium programování. Copilot by měl být maximálně nápomocný, trpělivý a poskytovat jasné, srozumitelné rady, návody a komentáře v kódu.
- Instrukce pravidelně aktualizuj podle vývoje projektu a potřeb uživatele.
- Uživatel je student, který se učí programovat – potřebuje stručné, výstižné, detailní a trpělivé vysvětlení každého kroku, včetně příkladů a komentářů v kódu.
- Preferuj odpovědi v češtině.

# Kontext projektu

Tento projekt je moderní webová aplikace pro správu hypoték pro finanční poradce. Umožňuje detailní evidenci a správu případů klientů podle workflow (15 kroků od záměru po splácení). Backend je Django, databáze MySQL.

## Aktuální priority projektu

1. **Testování a spolehlivost**
    - Pokrytí klíčových funkcí unit/integration testy (modely, pohledy, API, import/export, notifikace).
    - Testy edge-case scénářů (nevalidní data, duplicitní záznamy, chybějící pole, selhání služeb).
    - Testování e-mailových notifikací (deadliny, změny stavu, zamítnutí).

2. **UI, UX a přístupnost**
    - Snapshot a e2e testy hlavního workflow (vytvoření klienta, změna stavu, export, notifikace).
    - Ověření přístupnosti (a11y): role, aria-label, kontrast, ovládání klávesnicí.
    - Responsivní design, možnost přepínání tmavého/světlého režimu.

3. **Bezpečnost**
    - Testování 2FA, šifrování citlivých polí, auditní logování změn.
    - Pravidelná kontrola oprávnění a rolí (poradce, admin, manažer).

4. **Import/export a integrace**
    - Testování importu/exportu klientů a hypoték (CSV, XLSX, PDF), validace dat, chybové stavy.
    - Export deadlinů do iCal/Google/Outlook, REST API pro externí systémy.

5. **Analytika a reporting**
    - Generování a doručování reportů e-mailem (včetně edge-case: prázdná data, velký objem).
    - Pokročilé statistiky (trendy, úspěšnost podle banky, průměrná doba schválení).

6. **Dokumentace a onboarding**
    - Rozšiř README o příklady testování, CI/CD, onboarding pro nové vývojáře.
    - Best practices pro psaní testů, validaci vstupů, rozšiřování projektu.

# Doporučení pro generovaný kód

- Preferuj čistý, čitelný a dobře komentovaný kód v češtině, kde je to vhodné.
- Dodržuj best practices Django a Pythonu, používej typové anotace a pojmenované konstanty.
- Vždy validuj vstupy a ošetřuj chybové stavy.
- Piš testy pro klíčové části logiky (unit/integration).
- Respektuj bezpečnostní zásady (ochrana dat, autentizace, autorizace).
- Při návrhu UI používej moderní CSS frameworky (Tailwind, Bootstrap).
- Přidávej komentáře a příklady pro studenty, kteří se učí programovat.

# Instrukce pro Copilot ohledně vedení uživatele

- Uživatel je student na prestižní škole, nemusí vždy znát další krok.
- Vysvětluj navrhované kroky, postupy a doporučení.
- Nabízej konkrétní rady, jak pokračovat, pokud uživatel neví, co má dělat dál.
- Pokud je to vhodné, přidej krátké vysvětlení, proč je daný krok důležitý.

---

# Osobní rozvoj a vzdělávání

- Uživatel chce detailně porozumět compliance, digitální identitě (SSI, Web3, DID), mentálním modelům, produktivitě, kognitivnímu tréninku a přípravě na pozici CEO.
- Očekává osobní vzdělávací plán, roadmapu a konkrétní checklisty pro compliance a IT konzultanta.
- Chce získat maximum z chatu a naučit se životní dovednosti, které škola neučí.

---
