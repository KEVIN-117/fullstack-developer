# Análisis y Verificación de Información de Contacto

## ¿Por qué investigar contactos?

La información de contacto es crítica en OSINT porque:

- ✅ Valida identidades
- ✅ Vincula múltiples cuentas
- ✅ Revela relaciones profesionales
- ✅ Expone números de teléfono comprometidos
- ✅ Conecta datos de diferentes fuentes

---

## 🔍 Principales Herramientas

### 1. **OkCaller** (Búsqueda inversa de teléfono)

**URL**: https://www.okcaller.com

**Características**:

- Búsqueda inversa de números telefónicos
- Información del titular de la línea
- Validación de números
- Histórico de reportes de spam

**Cómo usar**:

```
1. Ingresa número telefónico completo
2. Obtén información del propietario
3. Revisa reportes y comentarios
4. Identifica si es spam o legítimo
```

**Formato de búsqueda**:

```
+34 612 345 678      (España)
+1 (555) 123-4567    (USA)
+44 20 1234 5678     (UK)
```

**Casos OSINT**:

```
# Valida número de empleado
- Número de contacto de empresa
- Número personal asociado a email
- Número en perfil de LinkedIn

# Encuentra información del dueño
- Nombre completo
- Ubicación
- Historial de cambios
```

---

### 2. **ClarityCheck**

**URL**: https://www.claritycheck.com

**Características**:

- Verificación de información de contacto
- Validación de emails y teléfonos
- Información de identidad
- Búsqueda de personas
- Integración con datos públicos

**Cómo usar**:

```
1. Busca por nombre y ubicación
2. Obtén información de contacto verificada
3. Consulta si el email es válido
4. Verifica empleabilidad actual
```

**Campos búsquedables**:

- Nombre completo
- Email
- Número telefónico
- Ciudad
- Empresa

**Casos OSINT**:

```
# Verifica empleado
- ¿Trabaja actualmente aquí?
- ¿Cuál es su número correcto?
- ¿Tiene múltiples números?

# Encuentra información relacionada
- Empleos anteriores
- Ubicaciones confirmadas
- Redes de contactos
```

---

### 3. **TrueCaller**

**URL**: https://www.truecaller.com

**Características**:

- Base de datos global de teléfonos
- Identificación de números desconocidos
- Detección de spam
- Información del titular
- Búsqueda inversa

**Ventajas**:

- Cobertura internacional
- Datos muy actualizados
- Identificación en tiempo real
- Información verificada

**Casos OSINT**:

```
# Identifica números en investigación
- Números en correos comprometidos
- Números en redes sociales
- Números en documentos públicos

# Valida información de contacto
- Verifica si el número es activo
- Identifica propietario actual
- Detecta cambios de titular
```

---

### 4. **WhitePages**

**URL**: https://www.whitepages.com

**Características**:

- Directorio de personas y negocios
- Búsqueda inversa de teléfono y email
- Información de propiedades
- Historial de direcciones
- Información de familiares

**Cobertura**: Principalmente USA, pero cobertura internacional

**Casos OSINT**:

```
# Búsqueda por teléfono
- Encuentra propietario del número
- Historial de direcciones
- Familiares conocidos

# Búsqueda por email
- Valida propiedad de email
- Encuentra información asociada

# Búsqueda por nombre
- Localiza a personas
- Múltiples direcciones
- Información de empleadores
```

---

## 📊 Flujo de Investigación

### Paso 1: Recopila contactos iniciales

```
Fuentes:
- Búsqueda en Google
- Redes sociales
- Brechas de datos
- Registros públicos
- LinkedIn
```

### Paso 2: Valida teléfonos

```
1. Ingresa número en OkCaller
2. Verifica información del titular
3. Busca reportes de spam
4. Consulta en TrueCaller
```

### Paso 3: Valida emails

```
1. Busca email en base de datos de brechas
2. Consulta en ClarityCheck
3. Verifica propiedad en WhitePages
```

### Paso 4: Cruza información

```
1. Vincula números con identidades
2. Encuentra múltiples números de misma persona
3. Identifica cambios históricos
4. Mapea relaciones
```

### Paso 5: Documentación

```
Registra:
- Número → Titular (Fecha validación)
- Email → Número (Fuente)
- Cambios históricos
- Inconsistencias detectadas
```

---

## 🔍 Técnicas Avanzadas

### 1. Búsqueda Inversa en Cascada

```
Email conocido
  ↓ (Busca en brechas)
→ Número de teléfono
  ↓ (OkCaller)
→ Nombre de titular
  ↓ (Google)
→ Múltiples números
  ↓ (TrueCaller)
→ Redes de contactos
```

### 2. Validación Cruzada

```
# Tengo estos datos:
- nombre@empresa.com
- Teléfono: +34 612 345 678

# Valido en múltiples plataformas:
1. OkCaller: ¿El número pertenece a esa persona?
2. HIBP: ¿Está ese email en brechas?
3. LinkedIn: ¿El nombre coincide con perfil?
4. Whitepages: ¿La dirección es consistente?
```

### 3. Análisis de Patrones de Teléfono

```
# Empresa XYZ:
- Empleado 1: +34 612 345 xxx
- Empleado 2: +34 612 345 yyy
- Empleado 3: +34 612 346 zzz

→ Probable rango de números corporativos
```

### 4. Histórico de Cambios

```
# Tracking de cambios:
2022: Número A para usuario X
2023: Número B para usuario X
2024: Número C para usuario X

→ Usuario cambió de teléfono 2 veces
```

---

## 📋 Checklist

```
☐ Búsqueda inicial de contactos
☐ Validación en OkCaller
☐ Validación en TrueCaller
☐ Búsqueda en HIBP
☐ Verificación en ClarityCheck
☐ Búsqueda en WhitePages
☐ Validación cruzada de información
☐ Búsqueda de números relacionados
☐ Análisis de patrones
☐ Documentación de hallazgos
☐ Identificación de inconsistencias
☐ Mapeo de relaciones
```

---

## ⚠️ Limitaciones y Consideraciones

### Limitaciones:

- ❌ Información puede estar desactualizada
- ❌ Números VoIP pueden ser anónimos
- ❌ Privacidad: algunos números no disponibles
- ❌ Acceso limitado en algunos países

### Consideraciones Legales:

- ✅ Legal: Usar datos públicos verificados
- ✅ Legal: Investigación de seguridad
- ❌ Ilegal: Acoso o spam
- ❌ Ilegal: Revelar privacidad sin consentimiento

---

## 🔗 Próximo Paso

Después de validar contactos, explora la información multimedia:
👉 **[05_Busqueda_Inversa_Metadatos.md](05_Busqueda_Inversa_Metadatos.md)**

---

## 📚 Referencias

- OkCaller: https://www.okcaller.com
- ClarityCheck: https://www.claritycheck.com
- TrueCaller: https://www.truecaller.com
- WhitePages: https://www.whitepages.com
- The OSINT Handbook by Dale Meredith

---

_Utiliza siempre información public y cumple con regulaciones de privacidad_
