# Visualización de Datos - Conexiones e Inteligencia

## ¿Por qué visualizar datos?

La visualización de datos permite:

- ✅ Identificar patrones rápidamente
- ✅ Revelar conexiones ocultas
- ✅ Comunicar hallazgos claramente
- ✅ Descubrir actores principales
- ✅ Mapear redes complejas
- ✅ Presentar resultados profesionales

---

## 🌐 Maltego - Principal Herramienta de Visualización

### Conceptos Básicos

**Transformaciones**: Conversiones automáticas entre entidades

```
Email → Dominio → Subdominios → IPs → Ubicación
Persona → Emails → Dominios → Redes sociales → Teléfonos
```

**Entidades**: Objetos que se pueden transformar

```
- Persona
- Email
- Dominio
- IP
- Teléfono
- Ubicación
- Documento
- Red social
```

---

### Flujo de Trabajo en Maltego

#### Paso 1: Crear Máquina (Gráfo)

```
1. Abrir Maltego
2. New → Transform Hub
3. Seleccionar plantilla o crear nueva
```

#### Paso 2: Agregar Entidad Inicial

```
1. Drag & drop entidad (ej: dominio)
2. Escribir valor (ej: empresa.com)
```

#### Paso 3: Aplicar Transformaciones

```
1. Click derecho en entidad
2. Seleccionar transformación
3. Esperar resultados
4. Visualizar conexiones
```

#### Paso 4: Expandir Grafo

```
1. Aplicar más transformaciones
2. Explorar ramas del grafo
3. Identificar patrones
4. Anotar hallazgos
```

#### Paso 5: Análisis

```
1. Identificar nodos clave
2. Buscar patrones
3. Validar información
4. Documentar hallazgos
```

---

### Transformaciones OSINT Comunes

```
PERSONA:
Nombre → Email → Dominio → Redes sociales → IP
Nombre → Teléfono → Ubicación → LinkedIn

EMPRESA:
Dominio → Subdominios → IPs → Ubicaciones → Empleados
Empresa → Empleados → Emails → Redes sociales

DOMINIO:
Dominio → Registrador WHOIS → Email contacto → Persona
Dominio → Certificados SSL → Información legal
Dominio → Subdominios → Servidores → IPs públicas

IP:
IP → Ubicación geográfica → ISP → Rango de IPs
IP → Puertos abiertos → Servicios → Vulnerabilidades
```

---

## 📊 Otras Herramientas de Visualización

### 1. **Gephi** - Análisis de Redes

**URL**: https://gephi.org/

**Características**:

- Visualización de redes complejas
- Análisis de comunidades
- Estadísticas de red
- Animaciones
- Exportación profesional

**Casos OSINT**:

```
- Mapeo de redes sociales
- Análisis de conexiones
- Identificación de influenciadores
- Detección de comunidades
```

---

### 2. **Neo4j** - Base de Datos de Grafos

**URL**: https://neo4j.com/

**Características**:

- Almacenamiento de relaciones complejas
- Queries poderosas
- Visualización integrada
- Community edition gratuita

**Casos OSINT**:

```
# Almacenar y consultar relaciones
MATCH (p:Persona)-[:CONOCE]->(p2:Persona)
WHERE p.nombre = "Target"
RETURN p, p2

# Análisis de caminos
MATCH path = (a:Persona)-[*]-(b:Persona)
WHERE a.nombre = "A" AND b.nombre = "B"
RETURN path
```

---

### 3. **Microsoft Power BI** - Análisis Corporativo

**Características**:

- Dashboards profesionales
- Análisis de datos
- Reportes interactivos
- Integración con múltiples fuentes

**Usos OSINT**:

```
- Reportes ejecutivos
- Análisis temporal
- Comparativas
- KPIs de investigación
```

---

## 🎨 Elementos de Visualización Efectiva

### 1. Nodos (Entidades)

```
Color: Tipo de entidad
  - Rojo: Personas objetivo
  - Azul: Dominios
  - Verde: Emails
  - Amarillo: IPs
  - Morado: Ubicaciones

Tamaño: Importancia/Centralidad
  - Grande: Nodo central/importante
  - Pequeño: Nodo periférico

Forma: Categoría
  - Círculo: Persona
  - Cuadrado: Empresa
  - Triángulo: Ubicación
```

### 2. Enlaces (Relaciones)

```
Tipo de enlace:
  - Línea sólida: Relación confirmada
  - Línea punteada: Relación probable
  - Línea gruesa: Relación fuerte
  - Línea fina: Relación débil

Dirección:
  - Flecha: Relación direccional
  - Bidireccional: Relación mutua
```

### 3. Anotaciones

```
- Fecha de descubrimiento
- Nivel de confianza
- Fuente de información
- Notas relevantes
```

---

## 📋 Workflow Completo de Visualización

### Fase 1: Recopilación

```
TheHarvester / SpiderFoot
  ↓
Exportar datos
```

### Fase 2: Importación

```
Maltego / Neo4j
  ↓
Cargar datos
```

### Fase 3: Transformación

```
Aplicar transformaciones
  ↓
Expandir relaciones
```

### Fase 4: Análisis

```
Identificar patrones
  ↓
Validar información
```

### Fase 5: Visualización

```
Crear gráficos
  ↓
Ajustar layout
```

### Fase 6: Reporte

```
Documentar hallazgos
  ↓
Exportar para presentación
```

---

## 🎯 Ejemplos Prácticos

### Ejemplo 1: Mapeo Organizacional

```
Empresa XYZ
  ├─ CEO (Nombre A)
  │  ├─ Email: ceo@xyz.com
  │  ├─ LinkedIn: /in/nombreA
  │  └─ Teléfono: +34-123-456-789
  │
  ├─ CTO (Nombre B)
  │  ├─ Email: cto@xyz.com
  │  └─ GitHub: nombreB
  │
  └─ Empleado (Nombre C)
     ├─ Email: empleado@xyz.com
     └─ Twitter: @nombreC
```

### Ejemplo 2: Timeline de Eventos

```
2024-01-15: Target cambió de empresa
2024-02-20: Publicó en LinkedIn sobre seguridad
2024-03-10: Compartió artículo sobre OSINT
2024-04-05: Actualizó perfil de GitHub
2024-05-12: Posteó en Twitter sobre evento
```

### Ejemplo 3: Red de Contactos

```
Target A ─── conoce ──→ Contacto B
    ↓                          ↓
    └─── trabaja en ──→ Empresa X
                           ↓
                       ─── empleado ──→ Contacto C
```

---

## 📊 Herramientas Complementarias

### 1. **MindMap** - Lluvia de Ideas

```
Target
  ├─ Información personal
  ├─ Información profesional
  ├─ Presencia digital
  └─ Conexiones
```

### 2. **Timeline** - Cronología

```
2024-01-01: Evento A
2024-02-15: Evento B
2024-03-20: Evento C
2024-04-10: Evento D
```

### 3. **Heatmap** - Intensidad de Actividad

```
Mapa con colores indicando:
- Rojo: Actividad alta
- Amarillo: Actividad media
- Verde: Actividad baja
```

---

## 🔗 Próximo Paso

Con la visualización completa, protege tu propia información:
👉 **[09_Defensa_Mitigacion.md](09_Defensa_Mitigacion.md)**

---

## 📚 Referencias

- Maltego: https://www.maltego.com/
- Gephi: https://gephi.org/
- Neo4j: https://neo4j.com/
- The OSINT Handbook by Dale Meredith

---

_Visualiza datos responsablemente y siempre verifica la precisión_
