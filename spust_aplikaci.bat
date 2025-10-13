@echo off
REM --- Spustí Django server a otevře aplikaci v Google Chrome ---

REM 1. Ukončí všechny běžící Django servery na portu 8000 (volitelné, bezpečné pro vývoj)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /F /PID %%a >nul 2>&1

REM 2. Spustí Django server v novém okně, které zůstane otevřené (musí běžet)
start "DjangoServer" cmd /k ".venv\Scripts\activate.bat && python manage.py runserver"

REM 3. Počkej 2 sekundy, než se server rozběhne
ping 127.0.0.1 -n 3 > nul

REM 4. Otevři aplikaci v Google Chrome
start chrome http://127.0.0.1:8000

REM 5. Skript se ukončí (server běží v novém okně)
exit
