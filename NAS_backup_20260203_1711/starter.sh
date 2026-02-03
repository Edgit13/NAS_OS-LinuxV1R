#!/bin/bash
cd "$(dirname "$0")"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}--------------------------------${NC}"
echo -e "${GREEN}       NAS OS STARTUP           ${NC}"
echo -e "${GREEN}--------------------------------${NC}\n"

echo -e "${YELLOW}Checking dependencies...${NC}"

REQUIRED_MODULES=("rich" "flask" "flask_cors")

if [ -d "venv" ]; then
    source venv/bin/activate
    echo -e "${GREEN}Virtual Environment active${NC}"
fi

MISSING_MODULES=()
for module in "${REQUIRED_MODULES[@]}"; do
    import_name=$(echo $module | tr '-' '_')
    python3 -c "import $import_name" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        MISSING_MODULES+=("$module")
    fi
done

if [ ! -f "translations.py" ]; then
    echo -e "${RED}CRITICAL ERROR: translations.py not found!${NC}"
    exit 1
fi

if [ ${#MISSING_MODULES[@]} -ne 0 ]; then
    echo -e "${YELLOW}Installing missing packages: ${MISSING_MODULES[*]}...${NC}"
    python3 -m pip install "${MISSING_MODULES[@]}"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}All dependencies installed.${NC}\n"
    else
        echo -e "${RED}Error during installation.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}Libraries OK.${NC}\n"
fi

WEB="NAS_OS-LinuxV--MENU -web.py"

if pgrep -f "$WEB" > /dev/null 2>&1; then
    echo -e "${YELLOW}Web Menu already running${NC}"
else
    echo -e "${GREEN}Starting Web Menu...${NC}"
    nohup python3 "$WEB" > web_menu.log 2>&1 &
    sleep 2
    if pgrep -f "$WEB" > /dev/null 2>&1; then
        IP=$(hostname -I | awk '{print $1}')
        echo -e "${GREEN}Web Menu OK -> http://$IP:8000/menu${NC}"
    else
        echo -e "${RED}Web Menu failed - check web_menu.log${NC}"
    fi
fi

echo ""
echo -e "${GREEN}Starting Terminal Menu...${NC}\n"
python3 "NAS_OS-LinuxV--MENU.py"
