# SOCMINT - Inteligencia en Redes Sociales

## ¿Qué es SOCMINT?

**SOCMINT** (Social Media Intelligence) es la recopilación y análisis de información de redes sociales públicas para investigación. Las redes sociales contienen:

- ✅ Información personal detallada
- ✅ Conexiones y relaciones
- ✅ Ubicaciones y movimientos
- ✅ Intereses y comportamientos
- ✅ Historial de cambios
- ✅ Metadatos de contenido

---

## 📱 Principales Plataformas para OSINT

### Facebook

**Características OSINT**:

- Información personal completa
- Lista de amigos (incluso privada a veces)
- Historial de posts
- Geolocalización por checkins
- Fotos con fecha y ubicación
- Empleador y educación

**Técnicas**:

```
# Búsqueda de perfil
nombre + ciudad
nombre + empresa
nombre + teléfono (si público)

# Información disponible sin ser amigo
- Foto de perfil
- Información básica
- Algunos posts públicos
- Amigos en común
```

---

### Instagram

**Características OSINT**:

- Fotos frecuentes con ubicaciones
- Hashtags que revelan contexto
- Geolocalización exacta
- Bio con información
- Relaciones mediante follows
- Historias desaparecidas (pero capturadas)

**Herramientas**:

#### **Osintgram** (Instagram OSINT)

**URL**: https://github.com/thewhiteh4t/osintgram

**Características**:

- Descarga fotos de usuarios
- Extrae ubicaciones (tags)
- Análisis de hashtags
- Información de followers
- Metadatos de posts

**Instalación**:

```bash
git clone https://github.com/thewhiteh4t/osintgram
cd osintgram
pip install -r requirements.txt
python3 osintgram.py
```

**Uso**:

```bash
python3 osintgram.py

# Dentro del programa:
target username
info          # Info básica
posts         # Descargar posts
followers     # Listar followers
following     # Seguidos
hashtags      # Hashtags usados
locations     # Ubicaciones
```

**Casos OSINT**:

```
# Mapeo de ubicaciones
- Descargar todas las fotos
- Extraer tags de ubicación
- Crear mapa de movimientos
- Identificar patrones

# Análisis de relaciones
- Ver followers y following
- Identificar círculo social
- Encontrar conexiones
```

---

### LinkedIn

**Características OSINT**:

- Información profesional verificada
- Historial de empleos
- Educación
- Conexiones profesionales
- Recomendaciones
- Skills y endorsements

**Técnicas**:

```
# Búsqueda de empleados
site:linkedin.com/in/ "empresa nombre"

# Búsqueda de empleadores
"empresa" site:linkedin.com

# Búsqueda de skills específicos
site:linkedin.com "skill" "empresa"
```

**Casos OSINT**:

```
# Mapeo organizacional
- Encontrar todos los empleados
- Identificar estructura
- Localizar roles específicos
- Análisis de rotación

# Inteligencia laboral
- Cambios de empleo
- Crecimiento de empresa
- Nuevas áreas de negocio
```

---

### Twitter/X

**Características OSINT**:

- Tweets históricos
- Ubicaciones mencionadas
- Links a otros perfiles
- Hashtags
- Followers/Following
- Retweets y menciones

**Herramientas**:

```
# Búsqueda avanzada
from:usuario since:2024-01-01
until:2024-12-31

# Búsqueda de ubicación
near:"ciudad" within:15km

# Búsqueda de links
url:dominio.com
```

**Casos OSINT**:

```
# Análisis de actividad
- Patrones de posteo
- Horarios activos
- Intereses
- Conexiones

# Detección de identidad
- Información personal revelada
- Ubicaciones compartidas
- Movimientos públicos
```

---

### TikTok

**Características OSINT**:

- Videos con ubicación exacta
- Sonidos/música que dating de contenido
- Comentarios y engagement
- Contactos/amigos sugeridos
- Patrones de comportamiento

**Desafíos**:

- ⚠️ Menos datos públicos que otras plataformas
- ⚠️ API limitado para OSINT
- ⚠️ Datos eliminados rápidamente

---

## 🛠️ Herramientas SOCMINT Avanzadas

### Dante's Gate

**Características**:

- Herramienta de scraping de redes sociales
- Automatización de búsquedas
- Análisis de datos
- Conexión de múltiples plataformas

**Nota**: Requiere configuración técnica

---

## 📊 Flujo de Investigación SOCMINT

### Paso 1: Identificación

```
1. Nombre del objetivo
2. Ubicación aproximada
3. Empleador (si conocido)
4. Edad aproximada
```

### Paso 2: Búsqueda Inicial

```
1. Google: "nombre" + "ciudad"
2. Búsqueda en cada plataforma
3. Variaciones de nombre
4. Nicknames conocidos
```

### Paso 3: Recopilación

```
1. Descargar información disponible
2. Captura de pantalla de perfiles
3. Documentar ubicaciones y fechas
4. Guardar fotos (con metadata)
```

### Paso 4: Análisis

```
1. Timeline de movimientos
2. Análisis de relaciones
3. Patrones de comportamiento
4. Verificación cruzada de información
```

### Paso 5: Documentación

```
1. Crear mapa de red social
2. Cronología de eventos
3. Puntos de contacto identificados
4. Hallazgos clave
```

---

## 🔍 Técnicas Avanzadas

### 1. Análisis de Ubicación en Timeline

```
Ejemplo:
- 6 Junio 14:00 - Post en Barcelona (check-in)
- 6 Junio 16:30 - Post en Valencia (fotos)
- 7 Junio 09:00 - Post en Madrid

→ Movimiento probable hacia el norte
```

### 2. Análisis de Red Social

```
Target A
  ├─ Amigo con Target B
  ├─ Amigo con Target C
  └─ Amigo con Target D
      └─ Amigo con Target E

→ Mapeo de red completa
```

### 3. Análisis Temporal

```
Posteos activos: 14:00-16:00 (probablemente está en el trabajo)
Posteos activos: 22:00-23:00 (actividad nocturna)

→ Inferir ubicación y horarios
```

### 4. Análisis de Hashtags

```
#MisVacaciones2024
#Barcelona
#Playa

→ Información de viajes y ubicaciones
```

---

## 📋 Checklist SOCMINT

```
☐ Búsqueda en Facebook
☐ Búsqueda en Instagram
☐ Búsqueda en LinkedIn
☐ Búsqueda en Twitter
☐ Búsqueda en TikTok
☐ Búsqueda en otras plataformas (Telegram, Discord, etc.)
☐ Análisis de perfil y bio
☐ Documentación de conexiones
☐ Recopilación de ubicaciones
☐ Análisis de timeline
☐ Identificación de patrones
☐ Verificación cruzada de datos
☐ Captura de pantallas/evidencia
☐ Mapeo de red social
```

---

## ⚠️ Consideraciones Éticas y Legales

### ✅ Legal:

- Investigar información pública
- Investigación de seguridad
- Propósitos académicos
- Compliance y cumplimiento

### ❌ Ilegal:

- Acceso a cuentas privadas
- Scraping violando TOS
- Acoso o suplantación
- Venta de datos personales
- Distribución no autorizada

### Privacidad:

- Respeta privacidad de terceros
- No revelar información personal
- Cumplir GDPR/CCPA
- Datos sensibles con protección

---

## 🔗 Próximo Paso

Con SOCMINT dominado, automatiza tus investigaciones:
👉 **[07_Herramientas_Automatizacion.md](07_Herramientas_Automatizacion.md)**

---

## 📚 Referencias

- Osintgram: https://github.com/thewhiteh4t/osintgram
- The OSINT Handbook by Dale Meredith
- Open Source Intelligence Methods and Tools - Hijazi & Hassan

---

_Investiga siempre dentro de los límites legales y éticos_
