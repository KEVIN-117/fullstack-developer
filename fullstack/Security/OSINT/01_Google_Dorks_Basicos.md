# Google Dorks - Técnicas Fundamentales

## ¿Qué es Google Dorking?

Google Dorking es una técnica de búsqueda avanzada que utiliza operadores especiales para encontrar información específica indexada por Google. Es una de las herramientas más potentes en OSINT porque:

- ✅ Es completamente legal
- ✅ Acceso público a información
- ✅ Requiere solo creatividad y paciencia
- ✅ Resultados altamente precisos

---

## 📚 Google Hacking Database

La Google Hacking Database (GHDB) contiene miles de dorks descubiertos y documentados para encontrar:

- Archivos de configuración expuestos
- Credenciales
- Información sensible
- Documentos privados
- Logs de servidores

📌 **Referencia**: https://www.exploit-db.com/google-hacking-database

---

## 🔍 Operadores Básicos

### 1. **site:** - Limita búsqueda a un dominio específico

```
site:ejemplo.com contraseña
site:github.com tokens_api
site:linkedin.com intitle:Resume
```

**Uso práctico**: Encontrar todas las páginas indexadas de un dominio objetivo

### 2. **inurl:** - Busca palabras en la URL

```
inurl:admin
inurl:login
inurl:backup
inurl:config.php
```

**Uso práctico**: Localizar paneles de administración expuestos

### 3. **intitle:** - Busca en el título de la página

```
intitle:"Index of" /admin
intitle:"confidential" filetype:pdf
intitle:"password"
```

**Uso práctico**: Encontrar directorios indexados sin protección

### 4. **intext:** / **cache:** - Búsqueda en contenido

```
intext:"api_key"
intext:"database password"
cache:ejemplo.com
```

**Uso práctico**: Encontrar información de configuración en páginas

### 5. **filetype:** - Filtra por tipo de archivo

```
filetype:pdf
filetype:xlsx
filetype:docx
filetype:config
filetype:sql
```

**Uso práctico**: Limitar búsquedas a documentos específicos

---

## 🎯 Ejemplos Prácticos

### Búsqueda Simple

```
"que quiero buscar" site:donde-lo-quiero-buscar
```

### Búsqueda Combinada (Avanzada)

```
"que quiero buscar" site:dominio.com -inurl:ignorar filetype:pdf
```

**Desglose**:

- `"que quiero buscar"` - Frase exacta entre comillas
- `site:dominio.com` - Solo en ese dominio
- `-inurl:ignorar` - EXCLUYE URLs con esta palabra (el signo - excluye)
- `filetype:pdf` - Solo archivos PDF

---

## 📋 Estrategias de Búsqueda

### Estrategia 1: Descubrimiento de Archivos Sensibles

```
site:empresa.com filetype:xlsx
site:empresa.com filetype:docx "contraseña" OR "password"
site:empresa.com filetype:pdf "confidencial"
```

### Estrategia 2: Exposición de Credenciales

```
site:github.com "api_key" empresa
site:pastebin.com contraseña usuario@empresa.com
"FTP password" OR "database password"
```

### Estrategia 3: Exposición de Configuración

```
inurl:config filetype:php
inurl:wp-config.php
inurl:.env filetype:txt
```

### Estrategia 4: Directorios Indexados

```
intitle:"Index of" /admin
intitle:"Index of" /backup
intitle:"Index of" /uploads
```

### Estrategia 5: Información de Contacto

```
intitle:"employee directory" site:empresa.com
intext:"@empresa.com" "phone" OR "extension"
```

---

## ⚠️ Limitaciones de Google Dorks

1. **Google indexa solo páginas públicas** - No accede a contenido detrás de logins
2. **Limitaciones de tasa** - Google puede bloquear demasiadas búsquedas automatizadas
3. **Cambios frecuentes** - El índice de Google se actualiza continuamente
4. **Operadores limitados** - Google ha eliminado algunos operadores históricos

---

## 💡 Tips Profesionales

### Usar comillas para búsquedas exactas

```
"password: 123456"  ← Busca exactamente esta cadena
password: 123456    ← Busca variaciones
```

### Combinar múltiples operadores

```
site:empresa.com inurl:admin intitle:"Login"
```

### Usar comodín (\*)

```
inurl:*/admin/backup
"apikey: *" filetype:php
```

### Excluir dominios con (-)

```
"password" -site:ejemplo.com -site:otro.com
```

---

## 🔗 Próximo Paso

👉 Una vez domines Google Dorks, expande tu alcance con:
**[02_Motores_Busqueda_Alternativos.md](02_Motores_Busqueda_Alternativos.md)**

---

## 📚 Referencias

- Google Hacking Database (GHDB): https://www.exploit-db.com/google-hacking-database
- Google Search Operators: https://www.google.com/advanced_search
- The OSINT Handbook by Dale Meredith

---

_Nota: Asegúrate de cumplir con todas las leyes locales y políticas de uso de Google._
