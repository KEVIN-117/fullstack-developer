# Herramientas de Automatización OSINT

## ¿Por qué automatizar OSINT?

La automatización permite:

- ✅ Procesar gran volumen de datos rápidamente
- ✅ Reducir errores humanos
- ✅ Búsquedas exhaustivas en paralelo
- ✅ Escalamiento de investigaciones
- ✅ Automatizar tareas repetitivas
- ✅ Rastreo continuo de objetivos

**Nota**: Siempre respetar robots.txt y términos de servicio

---

## 🔧 Principales Herramientas

### 1. **SpiderFoot** - Reconocimiento Pasivo

**URL**: https://www.spiderfoot.net/

**Características**:

- Recopilación automática de información
- Múltiples fuentes simultáneamente
- Análisis de dominios
- Búsqueda de subdominios
- Análisis de IPs
- Correlación automática de datos

**Qué hace**:

```
Target: empresa.com
  ├─ Resuelve DNS
  ├─ Busca subdominios
  ├─ Análisis de IP
  ├─ Búsqueda en bases de datos de brechas
  ├─ Análisis de registro WHOIS
  ├─ Búsqueda de emails
  ├─ Búsqueda de números de teléfono
  └─ Genera reporte visual
```

**Instalación**:

```bash
# Linux/Mac
git clone https://github.com/smicallef/spiderfoot.git
cd spiderfoot
pip install -r requirements.txt
python3 sf.py -l 127.0.0.1:5001

# Windows - Descargar desde https://www.spiderfoot.net/download
```

**Uso básico**:

```
1. Ingresa objetivo (dominio, email, IP)
2. Selecciona módulos a ejecutar
3. Inicia escaneo
4. Analiza resultados
5. Genera reporte
```

**Módulos destacados**:

```
- Resolución DNS
- Búsqueda de subdominios
- Análisis WHOIS
- Búsqueda en bases de datos públicas
- Análisis de vulnerabilidades
- Correlación de datos
```

---

### 2. **TheHarvester** - Recopilación de Información

**URL**: https://github.com/laramies/theHarvester

**Características**:

- Búsqueda de emails
- Búsqueda de subdominios
- Búsqueda de hosts
- Búsqueda de información de DNS
- Múltiples motores de búsqueda
- API públicas

**Qué recopila**:

```
- Direcciones de email de empleados
- Subdominios
- Hosts
- Información DNS
- Registros de puertos
- Datos de Microsoft Azure
- Datos de GitHub
```

**Instalación**:

```bash
pip install theHarvester
```

**Uso básico**:

```bash
# Búsqueda de emails
theHarvester -d empresa.com -b google

# Múltiples fuentes
theHarvester -d empresa.com -b google,bing,linkedin,baidu

# Con límite de resultados
theHarvester -d empresa.com -b google,bing -l 500

# Exportar resultados
theHarvester -d empresa.com -b google -f reporte.html
```

**Motores disponibles**:

```
- google
- bing
- baidu
- yandex
- github
- linkedin
- twitter
- forumsearch
- virustotal
- crt (Certificate Transparency)
```

**Ejemplos prácticos**:

```bash
# Encontrar infraestructura
theHarvester -d empresa.com -b all

# Búsqueda específica de emails
theHarvester -d empresa.com -b crt

# Análisis de GitHub
theHarvester -d empresa.com -b github

# Generar reporte XML
theHarvester -d empresa.com -b google,bing -f reporte
```

---

### 3. **Maltego** - Visualización de Conexiones

**URL**: https://www.maltego.com/

**Características**:

- Transformaciones de datos (plugins)
- Visualización gráfica de relaciones
- Integración con múltiples fuentes
- Análisis de red
- Reportes profesionales
- Versión Community gratis

**Qué visualiza**:

```
- Personas ↔ Emails ↔ Dominios
- Dominios ↔ IPs ↔ Hosts
- Personas ↔ Teléfonos ↔ Ubicaciones
- Empresas ↔ Empleados ↔ Contactos
```

**Flujo de trabajo**:

```
1. Ingresa objetivo (persona, dominio, empresa)
2. Aplica transformaciones automáticas
3. Visualiza conexiones en grafo
4. Expande relaciones
5. Analiza patrones
6. Genera reporte
```

**Transformaciones OSINT**:

```
- Persona → Emails
- Email → Dominios
- Dominio → Subdominios
- IP → Ubicación
- Email → Redes sociales
- Teléfono → Persona
```

**Instalación**:

```
1. Descargar desde https://www.maltego.com/downloads/
2. Instalar (versión Community incluida)
3. Registrar cuenta
4. Usar transformaciones
```

---

## 🎯 Workflow de Automatización

### Paso 1: Recopilación Inicial

```
SpiderFoot / TheHarvester
  ↓
→ Emails encontrados
→ Subdominios
→ Hosts
→ IPs
```

### Paso 2: Correlación

```
Maltego
  ↓
→ Conectar todos los datos
→ Visualizar relaciones
→ Identificar patrones
```

### Paso 3: Enriquecimiento

```
Búsquedas manuales adicionales
  ↓
→ Verificar información
→ Completar vacíos
→ Análisis detallado
```

### Paso 4: Análisis

```
Correlación de datos
  ↓
→ Identificar actores principales
→ Mapear red completa
→ Generar reporte
```

---

## 📋 Scripts de Automatización

### Script Python - TheHarvester Automático

```python
#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

targets = [
    "empresa1.com",
    "empresa2.com",
    "empresa3.com"
]

sources = ["google", "bing", "linkedin", "crt"]

for target in targets:
    print(f"\n[+] Analizando {target}...")

    cmd = ["theHarvester", "-d", target, "-b", ",".join(sources), "-f", f"{target}_report"]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"[✓] {target} completado")
    else:
        print(f"[✗] Error con {target}")

print("\n[+] Análisis completado - Revisar reportes HTML generados")
```

### Script Bash - Búsqueda en Cascada

```bash
#!/bin/bash

DOMAIN=$1

echo "[*] Iniciando análisis de $DOMAIN"

# Búsqueda DNS
echo "[+] Resolución DNS..."
nslookup $DOMAIN

# TheHarvester
echo "[+] Buscando con TheHarvester..."
theHarvester -d $DOMAIN -b google,bing,linkedin -f report_harvester

# SpiderFoot (si disponible)
echo "[+] SpiderFoot..."
# Adicionar configuración de SpiderFoot aquí

echo "[✓] Análisis completado"
```

---

## 📊 Comparativa de Herramientas

| Herramienta         | Función                   | Automatización | Escalabilidad | Costo          |
| ------------------- | ------------------------- | -------------- | ------------- | -------------- |
| **SpiderFoot**      | Reconocimiento pasivo     | Alta           | Excelente     | Gratis         |
| **TheHarvester**    | Recopilación de datos     | Alta           | Muy buena     | Gratis         |
| **Maltego**         | Visualización             | Media          | Buena         | Community/Pago |
| **OSINT Framework** | Agregador de herramientas | Media          | Buena         | Gratis         |

---

## ⚠️ Consideraciones Importantes

### Ética:

- ✅ Usar solo para información pública
- ✅ Respetar robots.txt
- ✅ Cumplir términos de servicio
- ❌ No hacer fuerza bruta
- ❌ No acceder a sistemas
- ❌ No obtener datos privados

### Técnico:

- ⚠️ Puede ser detectado por IDS/WAF
- ⚠️ Respeta rate limits
- ⚠️ Usa proxies si es necesario
- ⚠️ Documentar todo

### Legal:

- ✅ Investigación autorizada
- ✅ Propósitos legítimos
- ❌ No violación de privacidad
- ❌ Cumplir regulaciones locales

---

## 🔗 Próximo Paso

Después de automatizar, visualiza los resultados:
👉 **[08_Visualizacion_Datos.md](08_Visualizacion_Datos.md)**

---

## 📚 Referencias

- SpiderFoot: https://www.spiderfoot.net/
- TheHarvester: https://github.com/laramies/theHarvester
- Maltego: https://www.maltego.com/
- The OSINT Handbook by Dale Meredith

---

_Usa la automatización responsablemente dentro de marcos legales_
