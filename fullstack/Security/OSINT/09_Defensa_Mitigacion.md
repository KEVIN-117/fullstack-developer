# Defensa y Mitigación - Protege tu Privacidad OSINT

## ¿Por qué defenderse de OSINT?

Si otros pueden investigarte con OSINT, también necesitas saber qué información está expuesta y cómo protegerte:

- ✅ Reduce tu "huella digital"
- ✅ Controla tu narrativa pública
- ✅ Protege información sensible
- ✅ Previene suplantación de identidad
- ✅ Disminuye riesgo de ataques dirigidos

---

## 🔍 Auditoría de tu Información

### Paso 1: Google Tu Propio Nombre

```
Búsquedas a ejecutar:
- "tu nombre"
- "tu nombre" "tu ciudad"
- "tu nombre" "tu empresa"
- "tu email"
- "tu teléfono"
```

**¿Qué buscar?**

- Perfiles en redes sociales
- Información personal en directorios
- Fotos comprometidas
- Información de ubicación
- Datos de contacto antiguos

---

### Paso 2: Búsqueda en Redes Sociales

```
☐ Google todo en Facebook
☐ Google todo en LinkedIn
☐ Google todo en Instagram
☐ Google todo en Twitter
☐ Google todo en TikTok
☐ Buscar en otros perfiles que podrían linkear
```

---

### Paso 3: Búsqueda en Bases de Datos de Brechas

```
☐ Have I Been Pwned (HIBP)
☐ DeHashed
☐ Breach Directory
☐ Otros agregadores
```

**¿Qué revisar?**

- ¿Tus emails están en brechas?
- ¿Tus contraseñas están comprometidas?
- ¿Cuándo ocurrieron los compromisos?
- ¿Qué información fue filtrada?

---

### Paso 4: Búsqueda Inversa de Imágenes

```
Herramientas:
- TinEye
- Google Reverse Image Search
- Bing Image Search

Buscar todas tus fotos de perfil:
- ¿Dónde aparecen?
- ¿Han sido manipuladas?
- ¿Están asociadas a perfiles falsos?
```

---

### Paso 5: OSINT sobre Ti Mismo

```
Simula una investigación OSINT:
1. Usa SpiderFoot en tu dominio personal
2. TheHarvester para encontrar tus emails
3. Maltego para mapear tus conexiones
4. Shodan para IPs de tu casa/oficina
```

---

## 🛡️ Estrategias de Defensa

### 1. **Privacidad en Redes Sociales**

#### Facebook

```
✅ Privacidad máxima:
- Solo amigos ven posts
- Perfil no aparece en búsquedas
- Historial de actividad privado
- Sin geolocalización
- Bloquear descarga de fotos

⚙️ Configuración:
Settings → Privacy → Who can see your posts → Friends Only
Settings → Privacy → Who can look you up → Disabled
```

#### LinkedIn

```
✅ Privacidad corporativa:
- Perfil privado (requiere conexión para ver)
- Sin mostrar ubicación exacta
- Desactivar recomendaciones en Google
- Limitar conexiones públicas
- Cambiar visibilidad de empleos

⚙️ Configuración:
Settings & Privacy → Public profile → Edit public profile URL
Settings → Visibility → Turn on/off visibility
```

#### Instagram

```
✅ Privacidad máxima:
- Cuenta privada
- Sin ubicaciones en fotos
- Sin actividad pública
- Sin suggestions en buscador
- Desactivar histórico de localización

⚙️ Configuración:
Settings → Privacy → Make account private
Settings → Privacy → Story
Settings → Location → Turn off location history
```

---

### 2. **Gestión de Metadatos**

#### Remover EXIF de fotos antes de compartir

```bash
# Linux/Mac - usar ExifTool
exiftool -all= -overwrite_original foto.jpg

# Online: https://www.verexif.com/es/remove/
# Simplemente sube la foto
```

#### Configurar cámara para no guardar datos

```
Smartphone:
- Desactivar GPS/Location
- Desactivar timestamp en cámara
- No guardar ubicación en fotos

Apps de fotografía:
- Flickr → Desactivar geotagging
- Google Photos → Desactivar Timeline
```

---

### 3. **Gestión de Emails**

```
✅ Mejores prácticas:
- Usar emails diferentes para diferentes servicios
- Emails desechables (temp-mail, guerrillamail)
- Dominio personal para emails principales
- No revelar email personal en redes públicas
- Crear alias de email

Herramientas:
- ProtonMail (cifrado)
- StartMail (privacidad)
- Alias en iCloud
- Gmail aliases (@domain)
```

---

### 4. **Protección de Números de Teléfono**

```
✅ Medidas:
- No publicar número completo
- Usar números virtuales para servicios
- Registrar número en lista de no-llamadas
- Ser selectivo con quién compartes
- Usar apps de segunda línea

Servicios:
- Google Voice (virtual)
- Skype (virtual)
- Línea privada de operador
```

---

### 5. **Búsqueda y Opt-Out de Directorios**

#### Directorios a revisar:

```
- WhitePages: https://www.whitepages.com/opt-out
- Yellowpages: https://www.yellowpages.com
- TrueCaller: https://www.truecaller.com/unlisting
- 411: https://www.411.com/about/privacy
- Otros directorios locales
```

#### Proceso:

```
1. Encuentra tu información
2. Localiza opción de "Remove" u "Opt-out"
3. Sigue instrucciones (generalmente requiere verificación)
4. Verifica que fue removida
5. Repite mensualmente (algunos re-indexan)
```

---

### 6. **OPSEC - Operational Security**

```
✅ Prácticas de seguridad operacional:

Navegación:
- Usar VPN para privacidad
- Navegar en modo incógnito
- Limpiar cookies regularmente
- Usar navegadores privados (Tor, Brave)

Datos sensibles:
- No usar información real en pruebas
- Usar nombres ficticios en apps de prueba
- No mezclar identidades personales
- Separar cuentas por propósito

Comunicaciones:
- Mensajes cifrados (Signal)
- Email cifrado (ProtonMail)
- Videocalls seguras (Jitsi, Element)
- Sin compartir información real en chats
```

---

### 7. **Monitoreo Continuo**

#### Google Alerts

```
1. Crear alertas para:
   - "Tu nombre completo"
   - "Tu email"
   - "Tu teléfono"
   - "Tu empresa"

2. Configura frecuencia: Diaria
3. Recibe notificaciones de nuevos resultados
```

#### Monitoreo de Brechas

```
- Have I Been Pwned: Activar notificaciones
- Breach Database alerts: Subscribirse a actualizaciones
- Revisar mensualmente tu información
```

---

## 📋 Checklist de Defensa Personal

```
AUDITORÍA INICIAL:
☐ Búsqueda de nombre en Google
☐ Búsqueda de email en bases de datos de brechas
☐ Búsqueda inversa de fotos principales
☐ Revisión de perfil en cada red social
☐ Búsqueda de teléfono en OkCaller
☐ Análisis de información pública accesible

REDES SOCIALES:
☐ Configurar privacidad en Facebook
☐ Configurar privacidad en LinkedIn
☐ Configurar privacidad en Instagram
☐ Revisar Twitter/X configuración
☐ Desactivar ubicación en TikTok
☐ Revisar aplicaciones conectadas

DATOS PERSONALES:
☐ Remover de directorios (WhitePages, etc.)
☐ Desactivar geolocalización en dispositivos
☐ Remover EXIF de fotos antes de compartir
☐ Usar alias de email en servicios
☐ No publicar número completo
☐ Opt-out de búsquedas de personas

MONITOREO:
☐ Crear Google Alerts
☐ Activar notificaciones HIBP
☐ Revisar mensualmente
☐ Auditoría trimestral completa
```

---

## 🔒 Herramientas de Privacidad

### VPN

```
- NordVPN
- ExpressVPN
- ProtonVPN (gratis)
- Mullvad
```

### Navegadores Privados

```
- Tor Browser
- Brave
- Firefox con extensiones de privacidad
```

### Almacenamiento Cifrado

```
- Synology Moments (privado)
- Nextcloud
- Tresorit
```

### Comunicaciones

```
- Signal (mensajes)
- ProtonMail (email)
- Jitsi (video)
```

---

## ⚖️ Consideraciones Legales

### Derechos que tienes:

**GDPR (Europa)**:

- Derecho a saber qué datos se tienen
- Derecho a ser olvidado
- Derecho a acceso de datos
- Derecho a rectificación

**CCPA (California)**:

- Derecho a saber qué datos se recopilan
- Derecho a eliminar
- Derecho a opt-out
- Derecho a no discriminación

### Cómo usarlos:

```
1. Contacta a organizaciones que tengan tus datos
2. Solicita "Data Subject Access Request" (DSAR)
3. Solicita eliminación de datos
4. Solicita información de fuentes
5. Mantén documentación
```

---

## 🔗 Próximo Paso

Entender los aspectos éticos y legales de tu investigación:
👉 **[10_Etica_Legal_OSINT.md](10_Etica_Legal_OSINT.md)**

---

## 📚 Referencias

- The OSINT Handbook by Dale Meredith
- Open Source Intelligence Methods and Tools - Hijazi & Hassan
- GDPR Official: https://gdpr-info.eu/
- Privacy International: https://privacyinternational.org/

---

_Tu privacidad es importante - defiéndela activamente_
