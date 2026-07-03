#!/usr/bin/env bash

# Script de Autocomprobación - Módulo 0: SysAdmin & Redes
# Este script debe ejecutarse con sudo directamente en el servidor Debian local:
#   chmod +x validate.sh && sudo ./validate.sh

# Colores para salida formateada en consola
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sin color

echo -e "${YELLOW}=======================================================${NC}"
echo -e "${YELLOW}   INICIANDO AUDITORÍA AUTOMÁTICA DE CONFIGURACIÓN    ${NC}"
echo -e "${YELLOW}=======================================================${NC}"

# Validar permisos de root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[ERROR] Por favor, ejecuta este script como root (usando sudo).${NC}"
  exit 1
fi

PASS_SSH_CONF=true

# 1. Verificar configuración de Hardening SSH
echo -e "\n${YELLOW}[1/4] Verificando Hardening en SSH...${NC}"
SSHD_CONFIG="/etc/ssh/sshd_config"

if [ -f "$SSHD_CONFIG" ]; then
    # Chequear PasswordAuthentication
    pwd_auth=$(grep -i "^PasswordAuthentication" "$SSHD_CONFIG" | awk '{print $2}')
    if [ "$pwd_auth" == "no" ]; then
        echo -e "${GREEN}[OK] Autenticación por contraseña desactivada.${NC}"
    else
        echo -e "${RED}[FALLO] Autenticación por contraseña está activa o no configurada explícitamente como 'no'.${NC}"
        PASS_SSH_CONF=false
    fi

    # Chequear PermitRootLogin
    root_login=$(grep -i "^PermitRootLogin" "$SSHD_CONFIG" | awk '{print $2}')
    if [ "$root_login" == "no" ]; then
        echo -e "${GREEN}[OK] Acceso directo al usuario Root deshabilitado.${NC}"
    else
        echo -e "${RED}[FALLO] El usuario Root puede loguearse por SSH (PermitRootLogin no está configurado en 'no').${NC}"
        PASS_SSH_CONF=false
    fi
else
    echo -e "${RED}[ERROR] No se encontró el archivo $SSHD_CONFIG. ¿Está instalado OpenSSH?${NC}"
    PASS_SSH_CONF=false
fi

# 2. Verificar Estado del Firewall (UFW)
echo -e "\n${YELLOW}[2/4] Verificando estado del Firewall (UFW)...${NC}"
if command -v ufw &> /dev/null; then
    ufw_status=$(ufw status | grep -i "Status:" | awk '{print $2}')
    if [ "$ufw_status" == "active" ]; then
        echo -e "${GREEN}[OK] UFW está activo.${NC}"
        
        # Verificar si los puertos necesarios están abiertos
        ufw status | grep -E "22|2022" &> /dev/null
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[OK] El puerto SSH (22 o alternativo) está abierto en el firewall.${NC}"
        else
            echo -e "${RED}[FALLO] No se detectó ninguna regla activa para permitir SSH.${NC}"
        fi
    else
        echo -e "${RED}[FALLO] UFW está instalado pero inactivo. Ejecuta 'sudo ufw enable'.${NC}"
    fi
else
    echo -e "${RED}[FALLO] UFW no está instalado en el sistema. Ejecuta 'sudo apt install ufw'.${NC}"
fi

# 3. Verificar si el usuario administrador existe
echo -e "\n${YELLOW}[3/4] Verificando existencia de usuario administrador...${NC}"
if getent passwd homelab_admin > /dev/null; then
    echo -e "${GREEN}[OK] El usuario 'homelab_admin' existe.${NC}"
    # Chequear si está en el grupo sudo
    groups homelab_admin | grep -q "\bsudo\b"
    if [ $? -eq 0 ]; then
         echo -e "${GREEN}[OK] 'homelab_admin' pertenece al grupo sudo.${NC}"
    else
         echo -e "${RED}[FALLO] 'homelab_admin' existe pero no tiene privilegios de administrador (grupo sudo).${NC}"
    fi
else
    echo -e "${RED}[FALLO] No se ha creado el usuario 'homelab_admin'.${NC}"
fi

# 4. Verificar resolución DNS local
echo -e "\n${YELLOW}[4/4] Verificando red local...${NC}"
ip_address=$(ip addr show | grep -E 'inet\s' | grep -v '127.0.0.1' | awk '{print $2}' | cut -d/ -f1 | head -n 1)
echo -e "${GREEN}[INFO] IP actual del servidor en la red local: $ip_address${NC}"

echo -e "\n${YELLOW}=======================================================${NC}"
echo -e "${YELLOW}                  RESUMEN DE AUDITORÍA                 ${NC}"
echo -e "${YELLOW}=======================================================${NC}"
if [ "$PASS_SSH_CONF" = true ] && [ "$ufw_status" == "active" ]; then
    echo -e "${GREEN}¡Felicidades! Las configuraciones críticas de seguridad del Módulo 0 son correctas.${NC}"
    echo -e "${GREEN}Puedes dar este módulo por completado y avanzar en tu CHECKLIST.md.${NC}"
else
    echo -e "${RED}Existen configuraciones pendientes por asegurar. Revisa los fallos arriba descritos.${NC}"
fi
echo -e "${YELLOW}=======================================================${NC}"
