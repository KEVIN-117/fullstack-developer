# Búsqueda Inversa de Imágenes y Extracción de Metadatos

## ¿Por qué es importante el análisis de imágenes?

Las imágenes contienen información valiosa:

- ✅ Metadatos EXIF (ubicación, fecha, cámara)
- ✅ Identificación de ubicaciones
- ✅ Validación de identidades
- ✅ Detección de falsificaciones
- ✅ Vinculación entre perfiles

---

## 🖼️ Búsqueda Inversa de Imágenes

### **TinEye** - Búsqueda inversa profesional

**URL**: https://www.tineye.com

**Características**:

- Motor de búsqueda inversa especializado
- Indexación de miles de millones de imágenes
- Histórico de cambios de imagen
- Detección de ediciones
- Información de ubicaciones donde aparece

**Cómo usar**:

```
1. Sube imagen o URL en TinEye
2. Obtén resultados de dónde aparece la imagen
3. Revisa las versiones anteriores
4. Identifica manipulaciones
```

**Casos OSINT**:

```
# Valida identidad
- Foto de perfil en múltiples plataformas
- Busca dónde más aparece esa foto
- Identifica cuentas falsas

# Detecta manipulación
- Búsqueda inversa de foto editada
- Compara con original
- Identifica diferencias

# Encuentra ubicación
- Información de dónde fue publicada
- Contexto de uso
- Posibles conexiones
```

**Ventajas sobre Google Images**:

- ✅ Más exhaustivo
- ✅ Mejor para OSINT
- ✅ Acceso a datos históricos
- ✅ API disponible para automatización

---

### Google Images - Alternativa

**URL**: https://www.google.com/imghp

**Cómo usar**:

```
1. Click en cámara
2. Sube imagen o URL
3. Google busca imágenes similares
```

**Limitaciones para OSINT**:

- Menos exhaustivo que TinEye
- No muestra histórico completo
- Limitado para imágenes antiguas

---

## 📊 Metadatos EXIF - Información oculta

### ¿Qué es EXIF?

EXIF (Exchangeable Image File Format) es metadata embebida en imágenes que contiene:

```
📍 Ubicación: Latitud, Longitud
📅 Fecha/Hora: Cuándo se tomó
📷 Cámara: Modelo exacto
⚙️ Configuración: Apertura, ISO, velocidad
🖼️ Modificaciones: Editores, software
📱 Dispositivo: Tipo de teléfono/cámara
```

### Información típicamente disponible:

```
GPS Latitude:  40.7128° N
GPS Longitude: 74.0060° W
Date Taken:    2024-06-01 14:32:15
Camera Model:  Apple iPhone 15 Pro
Software:      Adobe Lightroom
```

---

## 🔧 Herramientas de Extracción EXIF

### 1. **ExifTool** - Herramienta de línea de comandos

**Instalación**:

```bash
# Linux/Mac
brew install exiftool

# Windows
# Descargar desde https://exiftool.org
```

**Uso básico**:

```bash
# Ver todos los metadatos
exiftool imagen.jpg

# Ver solo GPS
exiftool -GPS* imagen.jpg

# Ver solo información de cámara
exiftool -Make -Model -LensModel imagen.jpg

# Exportar a JSON
exiftool -json imagen.jpg > metadata.json

# Procesar múltiples imágenes
exiftool *.jpg > todo_metadata.txt

# Eliminar EXIF (privacidad)
exiftool -all= -overwrite_original imagen.jpg
```

**Casos OSINT**:

```bash
# Investigación de foto comprometida
exiftool foto_sospechosa.jpg

# Analizar múltiples fotos de red social
for archivo in descargas/*.jpg; do
  echo "=== $archivo ==="
  exiftool "$archivo" | grep -E "GPS|Date|Model"
done
```

---

### 2. **ExifData.com** - Extractor web

**URL**: https://www.exifdata.com

**Características**:

- Extración de EXIF online
- Sin instalación requerida
- Interfaz visual clara
- Muestra ubicación en mapa
- Información de privacidad

**Cómo usar**:

```
1. Sube imagen
2. Ver EXIF automáticamente
3. Ubicación mostrada en Google Maps
4. Descargar datos en JSON
```

**Ventajas**:

- ✅ Rápido y sin instalación
- ✅ Visualización en mapa
- ✅ Ideal para investigadores ocasionales

---

### 3. **ViewExifData.com**

**URL**: https://www.viewexifdata.com

**Características**:

- Interfaz simple
- Extracción completa de metadatos
- Visualización de ubicación
- Información técnica detallada

---

## 🗺️ Geolocalización a partir de EXIF

### Workflow:

```
1. Descarga imagen de red social
2. Extrae EXIF con ExifTool
3. Obtén coordenadas GPS
4. Ingresa en Google Maps
5. Identifica ubicación exacta
6. Verifica con imágenes satélite/Street View
```

### Conversión de coordenadas:

```
Formato grados: 40.7128° N, 74.0060° W
Formato decimal: 40.7128, -74.0060

Google Maps search: https://maps.google.com/?q=40.7128,-74.0060
```

---

## 🔍 Casos de Uso OSINT

### Caso 1: Validación de Ubicación

```
Investigación: ¿Dónde estaba la persona?

1. Obtén foto de red social
2. Extrae EXIF
3. Compara con declaraciones públicas
4. Verifica timeline
```

### Caso 2: Identificación de Dispositivo

```
Investigación: ¿Qué dispositivo usa?

1. Analiza múltiples fotos del perfil
2. Extrae modelo de cámara
3. Identifica patrón de software
4. Conecta con otras investigaciones
```

### Caso 3: Detección de Falsificación

```
Investigación: ¿Es auténtica esta foto?

1. Búsqueda inversa en TinEye
2. Compara versiones
3. Analiza metadatos
4. Busca inconsistencias
```

### Caso 4: Análisis de Series de Fotos

```
Investigación: Mapear movimiento de persona

1. Recopila múltiples fotos de diferentes fechas
2. Extrae GPS de cada una
3. Ordena cronológicamente
4. Mapea ruta en Google Maps
5. Identifica patrones de comportamiento
```

---

## 📋 Checklist de Análisis

```
☐ Búsqueda inversa en TinEye
☐ Búsqueda inversa en Google Images
☐ Extracción de EXIF completa
☐ Revisión de coordenadas GPS
☐ Verificación en Google Maps
☐ Análisis de modelo de cámara
☐ Revisión de fechas/horas
☐ Búsqueda de software usado
☐ Análisis de versiones anteriores
☐ Detección de ediciones/modificaciones
☐ Validación cruzada con otros datos
☐ Documentación de hallazgos
```

---

## ⚠️ Consideraciones

### Privacidad:

- ⚠️ EXIF puede revelar ubicación exacta
- ⚠️ Cuidado con fotos de casa/trabajo
- ✅ Remover EXIF antes de compartir en redes

### Precisión de GPS:

- GPS puede tener margen de error: ±5-20 metros
- Función de triangulación en edificios
- Ubicación aproximada en interiores

### Modificación de Metadatos:

- Algunos editores de fotos mantienen EXIF original
- Algunos apps de redes sociales lo eliminan
- Verificar antes de compartir información sensible

---

## 🔗 Próximo Paso

Con análisis de imágenes dominado, investiga las redes sociales:
👉 **[06_SOCMINT_Redes_Sociales.md](06_SOCMINT_Redes_Sociales.md)**

---

## 📚 Referencias

- TinEye: https://www.tineye.com
- ExifTool: https://exiftool.org
- ExifData: https://www.exifdata.com
- The OSINT Handbook by Dale Meredith

---

_Respeta la privacidad de las personas durante tu investigación_
