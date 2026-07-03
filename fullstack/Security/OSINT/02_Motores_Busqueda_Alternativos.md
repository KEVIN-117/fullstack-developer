# Motores de Búsqueda Alternativos

## ¿Por qué usar múltiples motores?

Google es poderoso, pero los motores alternativos tienen:

- ✅ Diferentes índices y cobertura
- ✅ Políticas menos restrictivas
- ✅ Acceso a contenido que Google ignora
- ✅ Menor detección de automatización
- ✅ Características especializadas únicas

---

## 🔍 Principales Motores Alternativos

### 1. **Bing**

**URL**: https://www.bing.com

**Ventajas**:

- Índice más permisivo que Google
- Interfaz de búsqueda avanzada intuitiva
- Menos restrictivo con automatización
- Mejor indexación de sitios académicos

**Operadores soportados**:

```
site:dominio.com
inurl:admin
intitle:"Index of"
filetype:pdf
-palabra (exclusión)
"frase exacta"
```

**Dorks útiles**:

```
site:empresa.com inurl:backup
site:empresa.com filetype:xlsx
intitle:"confidential" site:empresa.com
```

---

### 2. **Yandex**

**URL**: https://www.yandex.com

**Ventajas**:

- Motor ruso con diferentes fuentes
- Indexación agresiva
- Acceso a contenido regional
- Menos restrictivo que Google/Bing
- Excelente para archivos antiguos

**Operadores soportados**:

```
site:
url:
title:
text:
type: (tipo de archivo)
```

**Dorks útiles**:

```
site:empresa.com "password"
site:empresa.com filetype:sql
title:"admin" url:empresa.com
```

**Nota**: Interfaz en ruso, pero busca globalmente. Usa traductor si es necesario.

---

### 3. **DuckDuckGo**

**URL**: https://www.duckduckgo.com

**Ventajas**:

- Enfocado en privacidad
- Menos rastreo de búsquedas
- Acceso a URLs oscuras/alternativas
- API disponible para automatización
- Sin censura de resultados

**Operadores soportados**:

```
site:
intitle:
filetype:
-palabra (exclusión)
"frase exacta"
```

**Dorks útiles**:

```
site:empresa.com admin
site:empresa.com "api key"
```

---

### 4. **Shodan**

**URL**: https://www.shodan.io

**Ventajas**:

- Motor de búsqueda de dispositivos
- Indexa banners de servidores
- Encuentra servicios expuestos
- Información de puertos y servicios
- Búsqueda por geolocalización

**Casos de uso OSINT**:

```
# Encontrar cámaras IP conectadas
cgi-bin/admin
# Routers expuestos
type:router
# Servidores web específicos
Apache/2.4
# Por país
country:US
```

**Nota**: Requiere registro, versión gratuita con limitaciones

---

### 5. **Censys**

**URL**: https://censys.io

**Ventajas**:

- Análisis de certificados SSL/TLS
- Información de hosts de internet
- Datos de dominios
- Histórico de cambios

**Búsquedas**:

```
# Por certificado
"empresa.com"
# Por nombre de servidor
parsed.names: empresa.com
# Por ASN
autonomous_system.name: "Microsoft"
```

---

### 6. **Metager**

**URL**: https://metager.org

**Ventajas**:

- Metabuscador que combina múltiples fuentes
- Enfocado en privacidad
- Acceso a archivos oscuros
- Búsqueda por tipo de contenido

**Uso**: Agregación de resultados de múltiples motores

---

## 📊 Tabla Comparativa

| Motor          | Cobertura          | Restricciones | Automatización | Casos OSINT                |
| -------------- | ------------------ | ------------- | -------------- | -------------------------- |
| **Google**     | Muy amplia         | Muchas        | Limitada       | Archivos, credenciales     |
| **Bing**       | Amplia             | Menos         | Moderada       | Backup, configuración      |
| **Yandex**     | Regional/Histórica | Pocas         | Sí             | Datos antiguos, región CIS |
| **DuckDuckGo** | Buena              | Ninguna       | API disponible | Privacidad, sin censura    |
| **Shodan**     | Dispositivos       | Datos en pago | Premium        | Servicios expuestos        |
| **Censys**     | Certificados/Hosts | Datos en pago | API            | Infraestructura, SSL       |

---

## 🎯 Estrategia Multimotor

### Búsqueda en paralelo:

1. **Google** → Información general y archivos
2. **Bing** → Alternativa con mejor cobertura
3. **Yandex** → Contenido histórico y regional
4. **Shodan** → Servicios y dispositivos expuestos
5. **Censys** → Certificados e infraestructura

### Workflow práctico:

```
1. Inicia con Google para entender el panorama
2. Repite en Bing si no encuentras suficiente
3. Intenta Yandex para encontrar versiones antiguas
4. Usa Shodan para servicios/infraestructura
5. Verifica certificados en Censys
```

---

## 💡 Tips Avanzados

### Combina operadores entre motores:

```
Bing:  site:empresa.com filetype:sql
Yandex: site:empresa.com "password" OR "contraseña"
DuckDuckGo: site:empresa.com intitle:admin
```

### Usa proxies para evitar bloqueos:

- Para búsquedas intensivas
- Rota entre múltiples IPs
- Respetar robots.txt

### Automatiza búsquedas:

- APIs de DuckDuckGo
- Scripts para Yandex
- Integraciones con herramientas OSINT

---

## ⚙️ Herramientas para Búsqueda Multi-Motor

### Osintgram (para Instagram - Paso 6)

```bash
# Búsqueda automática en Instagram
```

### TheHarvester (incluye búsqueda multi-motor)

```bash
theharvester -d empresa.com -b google,bing,yandex
```

---

## 🔗 Próximo Paso

Ahora que has dominado la búsqueda en múltiples motores:
👉 **[03_Busqueda_Brechas_Datos.md](03_Busqueda_Brechas_Datos.md)**

---

## 📚 Referencias

- Shodan: https://www.shodan.io
- Censys: https://censys.io
- Open Source Intelligence Methods and Tools - Hijazi & Hassan

---

_Nota: Respeta los términos de servicio de cada motor de búsqueda_
