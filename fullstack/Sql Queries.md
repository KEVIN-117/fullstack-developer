---
aliases:
  - SQL
  - DLL
sticker: emoji//1f636-200d-1f32b-fe0f
---
## 🔎 1. Tablas involucradas

Se están uniendo 4 tablas:

* `uatf_datos d` → contiene datos geográficos (departamento, localidad, país)
* `dar_tramites dt` → información de trámites
* `academico.alumnos a` → datos del alumno
* `fac_programas p` → información académica (programa, facultad, carrera)

Relaciones:

```sql
d.nro_dip = dt.nro_dip
a.id_ra = d.id_ra
a.id_programa = p.id_programa
```

---

## 📊 2. Qué está contando

La consulta usa `COUNT(DISTINCT CASE WHEN ...)` para clasificar trámites en categorías:

### 🏙️ Ciudad

```sql
d.id_loc = 1494 AND d.id_dep = 5
```

→ Trámites de personas en una localidad específica dentro del departamento 5.

---

### 🌄 Provincia

```sql
d.id_loc <> 1494 AND d.id_dep = 5
```

→ Mismo departamento (5), pero fuera de esa ciudad.

---

### 🌎 Interior - Ciudad

```sql
d.id_dep <> 5 AND d.id_loc IN (...)
```

→ Otras ciudades específicas fuera del departamento 5.

---

### 🌎 Interior - Provincia

```sql
d.nac_pais = 27 
AND d.id_dep <> 5 
AND d.id_loc NOT IN (...)
```

→ Resto del país (27), fuera del departamento 5 y fuera de esas ciudades específicas.

---

### 🌍 Exterior

```sql
d.nac_pais <> 27
```

→ Personas de otros países.

---

### 📌 Total

```sql
COUNT(DISTINCT dt.id_tramite)
```

→ Total de trámites sin importar ubicación.

---

## ⚠️ 3. Problema importante en el GROUP BY

Estás agrupando por:

```sql
GROUP BY 
  a.id_programa, 
  p.facultad, 
  p.carreras, 
  p.orden4, 
  dt.id_tramite, 
  a.id_alumno
```

👉 Esto rompe el sentido de los `COUNT`, porque:

* Estás agrupando por `dt.id_tramite`
* Entonces cada grupo probablemente tiene **1 solo trámite**
* Resultado: los `COUNT(DISTINCT ...)` tienden a ser **0 o 1**, no agregados reales

🔴 Esto es un error típico.

---

## 📅 4. Filtros aplicados

* Solo trámites tipo `'A'`
* Solo programa `'IMI'`
* Rango de fechas: **todo 2013**
* Se excluyen varios programas (`NOT IN (...)`)

---

## 🧠 5. Qué intenta hacer realmente

Parece que quieres:

👉 “Contar cuántos trámites hay por ubicación geográfica dentro de un programa académico”

Pero actualmente estás agrupando demasiado fino (por trámite y alumno).

---

## ✅ 6. Cómo debería ser (idea corregida)

Si quieres agregación real, deberías quitar `dt.id_tramite` del `GROUP BY`:

```sql
GROUP BY 
  a.id_programa, 
  p.facultad, 
  p.carreras, 
  p.orden4
```

Y probablemente también revisar si necesitas `a.id_alumno`.

---

## 🚀 7. Conclusión

La consulta:

✔ Clasifica trámites por ubicación geográfica
✔ Filtra por programa y fecha
❌ Pero está mal agregada por incluir `dt.id_tramite` en el GROUP BY

---

# 🎯 Objetivo del reporte (interpretado)

Quieres algo como:

👉 “Cantidad de trámites por programa (`IMI`) en 2013, clasificados en:

* Ciudad
* Provincia
* Interior (ciudad/provincia)
* Exterior
* Total”

---

# ❌ Problema actual

Tu query actual:

* Agrupa por `dt.id_tramite` → rompe la agregación
* Mezcla nivel detalle (alumno/trámite) con nivel resumen

---

# ✅ Rediseño correcto (nivel programa)

Este sería el diseño limpio y correcto:

```sql
SELECT
    p.orden4,
    a.id_programa,
    p.facultad,
    p.carreras,

    COUNT(DISTINCT CASE 
        WHEN d.id_loc = 1494 AND d.id_dep = 5 
        THEN dt.id_tramite 
    END) AS ciudad,

    COUNT(DISTINCT CASE 
        WHEN d.id_loc <> 1494 AND d.id_dep = 5 
        THEN dt.id_tramite 
    END) AS provincia,

    COUNT(DISTINCT CASE 
        WHEN d.id_dep <> 5 
             AND d.id_loc IN (2794, 729, 2059, 821, 2234, 2773, 2680, 2526) 
        THEN dt.id_tramite 
    END) AS int_ciudad,

    COUNT(DISTINCT CASE 
        WHEN d.nac_pais = 27 
             AND d.id_dep <> 5 
             AND d.id_loc NOT IN (2794, 729, 2059, 821, 2234, 2773, 2680, 2526) 
        THEN dt.id_tramite 
    END) AS int_provincia,

    COUNT(DISTINCT CASE 
        WHEN d.nac_pais <> 27 
        THEN dt.id_tramite 
    END) AS exterior,

    COUNT(DISTINCT dt.id_tramite) AS total

FROM uatf_datos d
JOIN public.dar_tramites dt 
    ON d.nro_dip = dt.nro_dip
JOIN academico.alumnos a 
    ON a.id_ra = d.id_ra
JOIN fac_programas p 
    ON a.id_programa = p.id_programa

WHERE dt.tipo_tramite = 'A'
  AND dt.fecha BETWEEN DATE '2013-01-01' AND DATE '2013-12-31'
  AND p.id_programa = 'IMI'
  AND p.id_programa NOT IN (
        'PEN','EDI','EDT','ACP','AEC','LAT','PCO','TMC','TME','TMO','TMS',
        'TMT','TCG','TSC','AES','AMA','ACM','ALF','ALQ','CIN','EXI','EXQ',
        'CLI','LBC','PIC','LMA','LAB','SAG','SEN','CIF','UEN','INT','VIC'
  )

GROUP BY 
    p.orden4,
    a.id_programa,
    p.facultad,
    p.carreras

ORDER BY p.orden4 ASC;
```

---

# 🧠 Mejora conceptual clave

Ahora:

✔ Cada fila = **un programa**
✔ Los `COUNT` = agregaciones reales
✔ No hay duplicación por trámite

---

# ⚡ Optimización recomendada (muy importante)

Para que esto vuele en producción:

### Índices clave

```sql
-- Trámites
CREATE INDEX idx_tramites_filtro 
ON public.dar_tramites (tipo_tramite, fecha, nro_dip);

-- Datos geográficos
CREATE INDEX idx_uatf_join 
ON uatf_datos (nro_dip, id_ra, id_dep, id_loc, nac_pais);

-- Alumnos
CREATE INDEX idx_alumnos_ra_programa 
ON academico.alumnos (id_ra, id_programa);

-- Programas
CREATE INDEX idx_programas 
ON fac_programas (id_programa);
```

---

# 🚀 Variante avanzada (más limpia y rápida)

Si quieres evitar repetir lógica, puedes usar una subconsulta:

```sql
WITH base AS (
    SELECT DISTINCT
        dt.id_tramite,
        a.id_programa,
        p.facultad,
        p.carreras,
        p.orden4,
        d.id_dep,
        d.id_loc,
        d.nac_pais
    FROM uatf_datos d
    JOIN public.dar_tramites dt ON d.nro_dip = dt.nro_dip
    JOIN academico.alumnos a ON a.id_ra = d.id_ra
    JOIN fac_programas p ON a.id_programa = p.id_programa
    WHERE dt.tipo_tramite = 'A'
      AND dt.fecha BETWEEN DATE '2013-01-01' AND DATE '2013-12-31'
      AND p.id_programa = 'IMI'
)

SELECT
    orden4,
    id_programa,
    facultad,
    carreras,

    COUNT(*) FILTER (WHERE id_loc = 1494 AND id_dep = 5) AS ciudad,
    COUNT(*) FILTER (WHERE id_loc <> 1494 AND id_dep = 5) AS provincia,
    COUNT(*) FILTER (WHERE id_dep <> 5 AND id_loc IN (2794, 729, 2059, 821, 2234, 2773, 2680, 2526)) AS int_ciudad,
    COUNT(*) FILTER (WHERE nac_pais = 27 AND id_dep <> 5 AND id_loc NOT IN (2794, 729, 2059, 821, 2234, 2773, 2680, 2526)) AS int_provincia,
    COUNT(*) FILTER (WHERE nac_pais <> 27) AS exterior,
    COUNT(*) AS total

FROM base
GROUP BY orden4, id_programa, facultad, carreras
ORDER BY orden4;
```

---

👉 **Quieres contar número de graduados (no trámites)** por **área/programa/facultad**, usando `dt.tipo_tramite = 'A'` como indicador de graduación.

---

# 🎯 Problema conceptual clave

Tu query original cuenta:

```sql
COUNT(DISTINCT dt.id_tramite)
```

🔴 Pero eso mide **trámites**, no **graduados**.

👉 Un estudiante podría tener:

* más de un trámite
* o registros duplicados

➡️ Resultado: **sobreconteo**

---

# ✅ Qué deberías contar realmente

👉 **Graduados únicos = estudiantes únicos**

Dependiendo de tu modelo:

* `a.id_alumno` ✅ (recomendado)
* o `a.id_ra` (si es identificador único real)

---

# 🧠 Rediseño correcto (por área/programa)

```sql
SELECT
    p.orden4,
    p.facultad,
    p.carreras,
    a.id_programa,

    COUNT(DISTINCT a.id_alumno) AS total_graduados,

    COUNT(DISTINCT CASE 
        WHEN d.id_loc = 1494 AND d.id_dep = 5 
        THEN a.id_alumno 
    END) AS ciudad,

    COUNT(DISTINCT CASE 
        WHEN d.id_loc <> 1494 AND d.id_dep = 5 
        THEN a.id_alumno 
    END) AS provincia,

    COUNT(DISTINCT CASE 
        WHEN d.id_dep <> 5 
             AND d.id_loc IN (2794, 729, 2059, 821, 2234, 2773, 2680, 2526)
        THEN a.id_alumno 
    END) AS int_ciudad,

    COUNT(DISTINCT CASE 
        WHEN d.nac_pais = 27 
             AND d.id_dep <> 5 
             AND d.id_loc NOT IN (2794, 729, 2059, 821, 2234, 2773, 2680, 2526)
        THEN a.id_alumno 
    END) AS int_provincia,

    COUNT(DISTINCT CASE 
        WHEN d.nac_pais <> 27 
        THEN a.id_alumno 
    END) AS exterior

FROM uatf_datos d
JOIN public.dar_tramites dt 
    ON d.nro_dip = dt.nro_dip
JOIN academico.alumnos a 
    ON a.id_ra = d.id_ra
JOIN fac_programas p 
    ON a.id_programa = p.id_programa

WHERE dt.tipo_tramite = 'A'
  AND dt.fecha BETWEEN DATE '2013-01-01' AND DATE '2013-12-31'

GROUP BY 
    p.orden4,
    p.facultad,
    p.carreras,
    a.id_programa

ORDER BY p.orden4;
```

---

# 🔥 Mejora crítica (evitar duplicados de raíz)

Si un alumno tiene múltiples trámites tipo `'A'`, aún podrías duplicarlo en el JOIN.

👉 Solución robusta: **normalizar primero graduados únicos**

```sql
WITH graduados AS (
    SELECT DISTINCT
        a.id_alumno,
        a.id_programa,
        p.facultad,
        p.carreras,
        p.orden4,
        d.id_dep,
        d.id_loc,
        d.nac_pais
    FROM uatf_datos d
    JOIN public.dar_tramites dt 
        ON d.nro_dip = dt.nro_dip
    JOIN academico.alumnos a 
        ON a.id_ra = d.id_ra
    JOIN fac_programas p 
        ON a.id_programa = p.id_programa
    WHERE dt.tipo_tramite = 'A'
      AND dt.fecha BETWEEN DATE '2013-01-01' AND DATE '2013-12-31'
)

SELECT
    orden4,
    facultad,
    carreras,
    id_programa,

    COUNT(*) AS total_graduados,

    COUNT(*) FILTER (WHERE id_loc = 1494 AND id_dep = 5) AS ciudad,
    COUNT(*) FILTER (WHERE id_loc <> 1494 AND id_dep = 5) AS provincia,
    COUNT(*) FILTER (WHERE id_dep <> 5 AND id_loc IN (2794, 729, 2059, 821, 2234, 2773, 2680, 2526)) AS int_ciudad,
    COUNT(*) FILTER (WHERE nac_pais = 27 AND id_dep <> 5 AND id_loc NOT IN (2794, 729, 2059, 821, 2234, 2773, 2680, 2526)) AS int_provincia,
    COUNT(*) FILTER (WHERE nac_pais <> 27) AS exterior

FROM graduados
GROUP BY orden4, facultad, carreras, id_programa
ORDER BY orden4;
```

---

# 🧠 Insight importante

Ahora estás midiendo correctamente:

✅ **personas graduadas**
❌ ya no “eventos de trámite”

---

# 🚀 Posibles extensiones útiles

Con este modelo ya puedes fácilmente:

* 📊 Graduados por **facultad**
* 📅 Evolución por **año**
* 👨‍🎓 Graduados por **género** (si tienes ese campo)
* 📍 Mapas geográficos reales

---
# METRICAS

---

# 🧠 🎯 PRINCIPIO CLAVE

Toda métrica debe responder:

```text
¿Qué decisión permite tomar?
```

---

# 📊 🧩 1. MÉTRICAS DE ESTUDIANTES

---

## 🎯 Básicas

### Total de estudiantes por gestión

```text
¿Cuántos estudiantes hay este año?
```

---

### ✔ Crecimiento interanual

```text
¿Estamos creciendo o cayendo?
```

```sql
COUNT(year N) vs COUNT(year N-1)
```

---

### ✔ Estudiantes activos vs inactivos

```text
¿cuántos abandonaron?
```

---

## 🔥 Interesantes

### ✔ Tasa de retención

```text
estudiantes que continúan / estudiantes del año anterior
```

👉 clave para:

* detectar deserción

---

### ✔ Tasa de deserción

```text
1 - retención
```

---

### ✔ Distribución por edad

```text
¿tenemos población joven o adulta?
```

---

# 🎓 🧩 2. MATRÍCULAS

---

## ✔ Matrículas por gestión

```text
volumen académico
```

---

## ✔ Matrículas por facultad

```text
qué facultad crece más
```

---

## ✔ Matrículas por programa

```text
ranking de carreras
```

---

## 🔥 Avanzadas

### ✔ Ticket promedio (si hay pagos)

```text
SUM(amount) / COUNT(*)
```

---

### ✔ Tipo de matrícula

```text
regular vs extraordinaria
```

---

# 🏫 🧩 3. ADMISIONES

---

## ✔ Número de admitidos

---

## ✔ Tasa de aceptación

```text
admitidos / postulantes
```

---

## ✔ Puntaje promedio

```text
AVG(score)
```

---

## 🔥 Muy útil

### ✔ Distribución de puntajes

```text
histograma (ej: 0-50, 50-70, 70-100)
```

---

# 🎓 🧩 4. GRADUADOS

---

## ✔ Graduados por gestión

---

## ✔ Tiempo promedio de graduación

```text
fecha_graduación - fecha_ingreso
```

---

## ✔ Modalidad de titulación

```text
tesis, examen, proyecto
```

---

## 🔥 Insight fuerte

### ✔ Eficiencia terminal

```text
graduados / admitidos (cohorte)
```

👉 métrica MUY importante institucionalmente

---

# 💰 🧩 5. BECAS

---

## ✔ Número de becarios

---

## ✔ % de estudiantes con beca

```text
becados / total estudiantes
```

---

## ✔ Promedio de porcentaje de beca

```text
AVG(percentage)
```

---

## 🔥 Avanzado

### ✔ Distribución por tipo de beca

```text
mérito, económica, deportiva
```

---

# 👨‍🏫 🧩 6. DOCENTES

---

## ✔ Número de docentes por facultad

---

## ✔ Tipo de docente

```text
tiempo completo vs parcial
```

---

## ✔ Nivel académico

```text
licenciatura, maestría, doctorado
```

---

## 🔥 Métrica clave

### ✔ Ratio estudiante/docente

```text
# estudiantes / # docentes
```

👉 calidad educativa

---

# 🧠 🧩 7. MÉTRICAS TRANSVERSALES (MUY PRO)

---

## 🔥 Cohortes

```text
grupo de estudiantes que ingresaron el mismo año
```

---

### ✔ Seguimiento de cohorte

```text
2020 → cuántos siguen en 2021, 2022, 2023
```

👉 🔥 esto es nivel BI real

---

## 🔥 Funnel educativo

```text
admisión → matrícula → graduación
```

Ejemplo:

```text
1000 postulantes
→ 600 admitidos
→ 500 matriculados
→ 300 graduados
```

---

## 🔥 KPIs ejecutivos

---

### ✔ Tasa de conversión

```text
matriculados / admitidos
```

---

### ✔ Tasa de graduación

```text
graduados / matriculados
```

---

# 🧠 🧩 8. MÉTRICAS TEMPORALES

Gracias a `dim_tiempo`:

---

## ✔ Por mes

```text
tendencias
```

---

## ✔ Por trimestre

---

## ✔ Series de tiempo

```text
evolución histórica
```

---

# 🚀 🎯 9. ENDPOINTS SUGERIDOS

---

```text
GET /stats/students?gestion=2025
GET /stats/students/growth
GET /stats/matriculas/by-faculty
GET /stats/admissions/acceptance-rate
GET /stats/graduates
GET /stats/scholarships/distribution
GET /stats/teachers/ratio
GET /stats/cohorts/2020
GET /stats/funnel
```

---

# 🧠 🔥 NIVEL PRO (lo que diferencia tu sistema)

---

## 👉 No te quedes en conteos

Evita esto:

```text
❌ solo COUNT(*)
```

---

## Apunta a esto:

```text
✔ tasas (%)
✔ ratios
✔ tendencias
✔ comparaciones
```

---



# 🎯 1. Definir el enfoque del DW

Primero: en un esquema estrella debes pensar en **hechos (facts)** y **dimensiones (dimensions)**.

En tu caso, los procesos principales son:

### 🔥 Hechos (Fact Tables)

1. **Fact_Registration (matrículas)** → eje principal
2. **Fact_Admissions (admisiones)**
3. **Fact_Scholarships (becas)**
4. **Fact_Graduates (graduaciones)**

---

# 🧱 2. Definir Dimensiones

Estas serán reutilizadas por múltiples hechos:

### 📅 Dim_Time

```sql
CREATE TABLE dim_time (
    time_key INT PRIMARY KEY, -- YYYYMMDD
    date DATE,
    year INT,
    semester INT,
    month INT,
    day INT,
    quarter INT
);
```

---

### 👨‍🎓 Dim_Student

(SCD Tipo 2 recomendado si quieres histórico)

```sql
CREATE TABLE dim_student (
    student_key SERIAL PRIMARY KEY,
    student_id UUID,
    student_code VARCHAR(50),
    gender CHAR(1),
    birth_date DATE,
    student_type VARCHAR(50),
    state VARCHAR(50),
    start_date TIMESTAMPTZ,
    end_date TIMESTAMPTZ,
    is_current BOOLEAN
);
```

---

### 📘 Dim_Program

```sql
CREATE TABLE dim_program (
    program_key SERIAL PRIMARY KEY,
    program_id UUID,
    program_name VARCHAR(150),
    academic_level VARCHAR(50),
    program_type VARCHAR(50),
    faculty_name VARCHAR(150)
);
```

---

### 🏫 Dim_Location

(denormalizamos country + department + province + location)

```sql
CREATE TABLE dim_location (
    location_key SERIAL PRIMARY KEY,
    country_name VARCHAR(200),
    department_name VARCHAR(200),
    province_name VARCHAR(200),
    location_name VARCHAR(200)
);
```

---

### 🎓 Dim_School

```sql
CREATE TABLE dim_school (
    school_key SERIAL PRIMARY KEY,
    school_id UUID,
    name VARCHAR(100),
    type VARCHAR(10),
    shift VARCHAR(10),
    area VARCHAR(10)
);
```

---

### 👨‍🏫 Dim_Teacher (opcional para análisis docente)

```sql
CREATE TABLE dim_teacher (
    teacher_key SERIAL PRIMARY KEY,
    teacher_id UUID,
    full_name VARCHAR(150),
    academic_level VARCHAR(50),
    profession VARCHAR(100),
    faculty_name VARCHAR(150)
);
```

---

# 🔥 3. Tablas de Hechos

---

## 📊 Fact_Registration (CENTRAL)

```sql
CREATE TABLE fact_registration (
    registration_key BIGSERIAL PRIMARY KEY,

    student_key INT,
    program_key INT,
    time_key INT,
    location_key INT,

    year INT,
    period INT,

    -- métricas
    registrations_count INT DEFAULT 1,

    FOREIGN KEY (student_key) REFERENCES dim_student(student_key),
    FOREIGN KEY (program_key) REFERENCES dim_program(program_key),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key),
    FOREIGN KEY (location_key) REFERENCES dim_location(location_key)
);
```

---

## 📥 Fact_Admissions

```sql
CREATE TABLE fact_admissions (
    admission_key BIGSERIAL PRIMARY KEY,

    student_key INT,
    time_key INT,

    admission_type VARCHAR(100),

    admissions_count INT DEFAULT 1,

    FOREIGN KEY (student_key) REFERENCES dim_student(student_key),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key)
);
```

---

## 🎓 Fact_Scholarships

```sql
CREATE TABLE fact_scholarships (
    scholarship_key BIGSERIAL PRIMARY KEY,

    student_key INT,
    time_key INT,

    scholarship_type VARCHAR(50),
    amount NUMERIC(10,2),

    FOREIGN KEY (student_key) REFERENCES dim_student(student_key),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key)
);
```

---

## 🎓 Fact_Graduates

```sql
CREATE TABLE fact_graduates (
    graduate_key BIGSERIAL PRIMARY KEY,

    student_key INT,
    program_key INT,
    time_key INT,

    final_grade NUMERIC(5,2),

    graduates_count INT DEFAULT 1,

    FOREIGN KEY (student_key) REFERENCES dim_student(student_key),
    FOREIGN KEY (program_key) REFERENCES dim_program(program_key),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key)
);
```

---

# 🔄 4. Mapeo OLTP → DW (ETL)

Ejemplo:

### 🔹 Student → dim_student

* `student.id` → `student_id`
* `person.gender` → `gender`
* `student.state` → `state`

---

### 🔹 Registration → fact_registration

* `registration.student_id` → dim_student
* `registration.year` → dim_time
* `student.program_id` → dim_program

---

### 🔹 Ubicación (JOIN complejo en ETL)

```sql
person → location → province → department → country
```

➡️ se aplana en `dim_location`

---

# ⚡ 5. Buenas prácticas clave

### ✔️ 1. Denormalización

En DW está BIEN repetir datos (ej: faculty_name en dim_program)

---

### ✔️ 2. Surrogate Keys

Siempre usar:

```sql
SERIAL / BIGSERIAL
```

NO usar UUID en facts/dims

---

### ✔️ 3. Índices en facts

```sql
CREATE INDEX idx_fact_registration_time ON fact_registration(time_key);
CREATE INDEX idx_fact_registration_program ON fact_registration(program_key);
```

---

### ✔️ 4. Slowly Changing Dimensions (SCD)

* Student → Tipo 2 ✅
* Program → Tipo 1
* Location → Tipo 1

---

# 🧠 6. Ejemplos de consultas analíticas

### 📊 Matrículas por programa por año

```sql
SELECT 
    p.program_name,
    t.year,
    SUM(f.registrations_count)
FROM fact_registration f
JOIN dim_program p ON f.program_key = p.program_key
JOIN dim_time t ON f.time_key = t.time_key
GROUP BY p.program_name, t.year;
```

---

### 🎓 Graduados por facultad

```sql
SELECT 
    p.faculty_name,
    COUNT(*) 
FROM fact_graduates f
JOIN dim_program p ON f.program_key = p.program_key
GROUP BY p.faculty_name;
```

---

# 🚀 7. Siguiente paso (recomendado)

Podemos avanzar a:

✅ Diseño de **ETL (SQL o Airflow)**
✅ Crear **materialized views staging**
✅ Estrategia incremental (CDC)
✅ Optimización para Power BI / Tableau

---

Si quieres, en el siguiente paso te puedo diseñar:

👉 **Pipeline ETL completo (staging → DW)** listo para producción**

---

Follow GPT creator on X [https://x.com/khanukov](https://x.com/khanukov)
