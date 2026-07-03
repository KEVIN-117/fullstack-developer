# Búsqueda en Bases de Datos de Brechas

## ¿Qué son las Brechas de Datos?

Una brecha de datos (data breach) es la exposición no autorizada de información sensible. Durante un ataque, los actores maliciosos acceden a:

- Contraseñas
- Direcciones de correo
- Números de teléfono
- Información financiera
- Datos personales

Estos datos se vuelcan en bases de datos públicas que los investigadores OSINT utilizan para investigaciones.

---

## 🔓 Principales Fuentes de Brechas

### 1. **Have I Been Pwned (HIBP)**

**URL**: https://www.haveibeenpwned.com

**Características**:

- Base de datos de más de 700 millones de cuentas comprometidas
- Búsqueda por correo electrónico
- Notificaciones automáticas
- API para consultas programáticas
- 100% gratuito

**Cómo usar**:

```
1. Ingresa correo electrónico en la búsqueda
2. Verifica si aparece en brechas conocidas
3. Revisa en qué brechas específicas apareció
4. Ve qué datos fueron comprometidos
```

**Casos OSINT**:

```
# Investiga email de empleado
- buscar@empresa.com
- usuario@empresa.com
- contacto@empresa.com

# Encuentra emails alternativos
- usuario@gmail.com
- usuario@yahoo.com
```

**API HIBP**:

```bash
# Verificar si email fue pwnado
curl https://haveibeenpwned.com/api/v3/breachedaccount/usuario@ejemplo.com
```

---

### 2. **DeHashed**

**URL**: https://dehashed.com

**Características**:

- Más de 15 mil millones de registros
- Búsqueda por email, username, hash de contraseña
- Información detallada de brechas
- Datos históricos
- Acceso freemium (limitado)

**Cómo usar**:

```
1. Busca por email/username
2. Obtén lista de brechas relacionadas
3. Descarga datos en CSV
4. Analiza patrones de contraseñas
```

**Datos típicamente disponibles**:

- Email
- Username
- Contraseña (hash o texto plano)
- IP address
- Ubicación
- Número de teléfono
- Nombre completo

**Casos OSINT**:

```
# Busca emails corporativos
empresa@dominio.com

# Busca por nombre de usuario
admin_usuario
username_target

# Busca por teléfono
+34-123-456-789
```

---

### 3. **Breach Directory**

**URL**: https://breachdir.webonomic.nl/

**Características**:

- Agregador de múltiples bases de datos de brechas
- Búsqueda gratuita por email
- Interfaz simple
- Resultados de múltiples fuentes

**Ventajas**:

- Centraliza múltiples brechas
- Busca rápida
- Sin registro requerido

---

### 4. **Searching.pwndbmgr.com**

**URL**: https://searching.pwndbmgr.com/

**Características**:

- Motor de búsqueda de brechas
- Busca en múltiples databases
- Resultados detallados
- Información de contexto

---

### 5. **Weleakinfo**

**URL**: https://weleakinfo.com/

**Características**:

- Base de datos de múltiples brechas
- Búsqueda por email, username, dominio
- Alertas de nuevas filtraciones
- Análisis de brechas

**Nota**: Requiere suscripción para acceso completo

---

## 📊 Flujo de Investigación

### Paso 1: Búsqueda Inicial

```
1. Ingresa email objetivo en HIBP
2. Nota las brechas donde aparece
3. Anota fechas y plataformas comprometidas
```

### Paso 2: Profundización

```
1. Busca en DeHashed con mismo email
2. Obtén detalles de cada brecha
3. Busca usernames relacionados
4. Busca números de teléfono asociados
```

### Paso 3: Análisis

```
1. Compara información entre brechas
2. Identifica patrones de contraseñas
3. Encuentra emails alternativos
4. Mapea relaciones entre cuentas
```

### Paso 4: Validación

```
1. Verifica contraseñas en múltiples plataformas
2. Valida información en redes sociales
3. Corrobora con fuentes públicas
```

---

## 🔍 Técnicas Avanzadas

### 1. Búsqueda por Dominio

```
# En DeHashed
busca: @empresa.com
Resultado: todos los emails de esa empresa en brechas

# En HIBP
múltiples búsquedas para cada empleado
```

### 2. Búsqueda Inversa

```
# Tienes una contraseña, encuentra la cuenta
busca en DeHashed: "contraseña123"

# Encuentra quién comparte credenciales
```

### 3. Análisis de Patrones

```
# Contraseñas débiles
Patrón: empresa + año = empresa2024

# Variaciones de email
usuario@gmail.com, usuario@yahoo.com, usuario.apellido@empresa.com
```

### 4. Timeline de Brechas

```
2020: email@gmail.com en brecha A
2021: mismo email en brecha B
2023: mismo email en brecha C

→ Usuario probablemente reusa credenciales
```

---

## 📋 Checklist de Búsqueda

```
☐ Búsqueda en HIBP con email objetivo
☐ Búsqueda en HIBP con emails alternativos
☐ Búsqueda en DeHashed con email
☐ Búsqueda en DeHashed con username
☐ Búsqueda en Breach Directory
☐ Búsqueda por dominio en todas las fuentes
☐ Búsqueda por número de teléfono
☐ Análisis de patrones de contraseñas
☐ Búsqueda de usernames relacionados
☐ Validación de información encontrada
```

---

## ⚠️ Consideraciones Éticas y Legales

✅ **Legal**:

- Buscar si TU OWN email fue comprometido
- Investigación de seguridad autorizada
- Cumplimiento de GDPR/CCPA

❌ **Ilegal**:

- Acceder a datos privados no autorizados
- Usar credenciales para acceso no autorizado
- Publicar información de terceros
- Venta de datos

---

## 🔧 Automatización

### Script Python para búsqueda en HIBP

```python
import requests
import time

emails = [
    "email1@empresa.com",
    "email2@empresa.com",
    "admin@empresa.com"
]

for email in emails:
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"[+] {email} comprometido en:")
        for breach in response.json():
            print(f"    - {breach['Name']} ({breach['BreachDate']})")
    elif response.status_code == 404:
        print(f"[-] {email} no encontrado en brechas")

    time.sleep(1)  # Respetar rate limit
```

---

## 🔗 Próximo Paso

Una vez domines la búsqueda de brechas:
👉 **[04_Analisis_Contactos.md](04_Analisis_Contactos.md)**

---

## 📚 Referencias

- Have I Been Pwned: https://haveibeenpwned.com
- DeHashed: https://dehashed.com
- The OSINT Handbook by Dale Meredith
- Open Source Intelligence Methods and Tools - Hijazi & Hassan

---

_Nota: Utiliza esta información solo para propósitos legales y autorizados_
