#!/bin/bash

# setup_cron_notifications.sh
# Popis: Skript pro nastavení cron/systemd timer úloh pro automatické notifikace a reporty
# Autor: Copilot, 2026
# Použití: ./setup_cron_notifications.sh [--cron|--systemd|--show]

set -e

# Barvy pro výstup
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

PROJECT_DIR="/home/lenkaluksova/hypoteky_win"
VENV_DIR="$PROJECT_DIR/.venv"
PYTHON="$VENV_DIR/bin/python"
MANAGE="$PYTHON $PROJECT_DIR/manage.py"

# Kontrola, zda je projekt dostupný
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}Chyba: Projekt nenalezen na $PROJECT_DIR${NC}"
    exit 1
fi

# Kontrola virtuálního prostředí
if [ ! -f "$PYTHON" ]; then
    echo -e "${RED}Chyba: Virtuální prostředí nenalezeno na $VENV_DIR${NC}"
    exit 1
fi

echo -e "${BLUE}=== Nastavení automatických notifikací ===${NC}"
echo ""

# Funkce pro zobrazení cron nastavení
show_cron_setup() {
    echo -e "${BLUE}Cron nastavení (pro /etc/cron.d/hypoteky nebo crontab -e):${NC}"
    echo ""
    echo "# Denní notifikace o blížících se deadlinech (08:00 každý den)"
    echo "0 8 * * * cd $PROJECT_DIR && source $VENV_DIR/bin/activate && $MANAGE send_deadline_notifications >> /var/log/hypoteky_notifications.log 2>&1"
    echo ""
    echo "# Týdenní reporting (Pondělí 09:00)"
    echo "0 9 * * 1 cd $PROJECT_DIR && source $VENV_DIR/bin/activate && $MANAGE send_reporting_email >> /var/log/hypoteky_reporting.log 2>&1"
    echo ""
}

# Funkce pro zobrazení systemd timer nastavení
show_systemd_setup() {
    echo -e "${BLUE}Systemd timer nastavení:${NC}"
    echo ""
    cat <<'EOF'
1. Vytvoř soubor /etc/systemd/system/hypoteky-notifications.service:

[Unit]
Description=Hypotéky - Send Deadline Notifications
After=network.target

[Service]
Type=oneshot
User=www-data
WorkingDirectory=/home/lenkaluksova/hypoteky_win
ExecStart=/home/lenkaluksova/hypoteky_win/.venv/bin/python /home/lenkaluksova/hypoteky_win/manage.py send_deadline_notifications
StandardOutput=journal
StandardError=journal

2. Vytvoř soubor /etc/systemd/system/hypoteky-notifications.timer:

[Unit]
Description=Hypotéky - Deadline Notifications Timer

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 08:00:00
Persistent=true

[Install]
WantedBy=timers.target

3. Vytvoř soubor /etc/systemd/system/hypoteky-reporting.service:

[Unit]
Description=Hypotéky - Send Weekly Reporting
After=network.target

[Service]
Type=oneshot
User=www-data
WorkingDirectory=/home/lenkaluksova/hypoteky_win
ExecStart=/home/lenkaluksova/hypoteky_win/.venv/bin/python /home/lenkaluksova/hypoteky_win/manage.py send_reporting_email
StandardOutput=journal
StandardError=journal

4. Vytvoř soubor /etc/systemd/system/hypoteky-reporting.timer:

[Unit]
Description=Hypotéky - Weekly Reporting Timer

[Timer]
OnCalendar=Mon *-*-* 09:00:00
Persistent=true

[Install]
WantedBy=timers.target

5. Aktivuj timery:
sudo systemctl daemon-reload
sudo systemctl enable hypoteky-notifications.timer hypoteky-reporting.timer
sudo systemctl start hypoteky-notifications.timer hypoteky-reporting.timer

6. Zkontroluj stav:
sudo systemctl status hypoteky-notifications.timer
sudo systemctl status hypoteky-reporting.timer
sudo systemctl list-timers

EOF
}

# Funkce pro instalaci cron úloh
install_cron() {
    echo -e "${YELLOW}Přidávání cron úloh...${NC}"
    echo ""
    
    # Kontrola, zda sudo je dostupný
    if ! command -v sudo &> /dev/null; then
        echo -e "${RED}Chyba: sudo není dostupný. Prosím spusť skript s root přístupem.${NC}"
        exit 1
    fi
    
    # Vytvoř cron soubor pro hypotéky
    CRON_FILE="/etc/cron.d/hypoteky"
    CRON_CONTENT="# Hypotéky - Automatické notifikace a reporting
# Denní notifikace o blížících se deadlinech (08:00)
0 8 * * * cd $PROJECT_DIR && source $VENV_DIR/bin/activate && $MANAGE send_deadline_notifications >> /var/log/hypoteky_notifications.log 2>&1

# Týdenní reporting (Pondělí 09:00)
0 9 * * 1 cd $PROJECT_DIR && source $VENV_DIR/bin/activate && $MANAGE send_reporting_email >> /var/log/hypoteky_reporting.log 2>&1
"
    
    echo "$CRON_CONTENT" | sudo tee "$CRON_FILE" > /dev/null
    sudo chmod 644 "$CRON_FILE"
    
    echo -e "${GREEN}✓ Cron úlohy instalovány do $CRON_FILE${NC}"
    echo ""
    echo -e "${YELLOW}Ověř nastavení:${NC}"
    echo "sudo cat $CRON_FILE"
    echo ""
}

# Funkce pro kontrolu protokolů
check_logs() {
    echo -e "${BLUE}Logovací soubory:${NC}"
    echo ""
    echo "Notifikace:"
    echo "  sudo tail -f /var/log/hypoteky_notifications.log"
    echo ""
    echo "Reporting:"
    echo "  sudo tail -f /var/log/hypoteky_reporting.log"
    echo ""
}

# Hlavní logika
case "${1:-}" in
    --cron)
        install_cron
        show_cron_setup
        check_logs
        ;;
    --systemd)
        show_systemd_setup
        check_logs
        ;;
    --show|"")
        show_cron_setup
        echo ""
        echo -e "${YELLOW}Pro instalaci cron úloh spusť:${NC}"
        echo "  ./dev/setup_cron_notifications.sh --cron"
        echo ""
        echo -e "${YELLOW}Pro nastavení systemd timers spusť:${NC}"
        echo "  ./dev/setup_cron_notifications.sh --systemd"
        echo ""
        ;;
    *)
        echo "Použití: $0 [--cron|--systemd|--show]"
        echo ""
        echo "Možnosti:"
        echo "  --cron       Instaluj cron úlohy (vyžaduje sudo)"
        echo "  --systemd    Zobraz systemd timer nastavení"
        echo "  --show       Zobraz cron nastavení (výchozí)"
        exit 1
        ;;
esac
