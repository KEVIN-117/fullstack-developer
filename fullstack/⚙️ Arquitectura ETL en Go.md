# 🧠 🎯 VISIÓN DEL PROYECTO

> **Sistema de Data Warehouse con ETL concurrente en Go y API REST para análisis estadístico universitario**

---

# 🧱 📦 ARQUITECTURA DEFINIDA

```text
cmd/
 ├── api/        → servidor REST
 ├── etl/        → runner ETL

internal/
 ├── extract/
 ├── transform/
 ├── load/
 ├── pipeline/
 ├── repository/
 ├── domain/
 ├── service/

pkg/
 ├── db/
 ├── logger/
 ├── config/
```

---

# 🧩 🧠 ROLES (Scrum adaptado)

Dado tu caso:

* 🧑‍💻 **Kevin → Developer + Tech Lead**
* 🎯 **Product Owner → tú mismo (visión del DW)**
* 📋 **Scrum Master → tú (gestión ligera)**

👉 Esto es normal en proyectos individuales.

---

# 🗂️ 📌 PRODUCT BACKLOG (alto nivel)

## 🔥 Épicas principales

### 1. 🧱 Data Warehouse

* diseño esquema estrella
* creación de tablas
* índices y optimización

---

### 2. ⚙️ ETL en Go

* extracción desde OLTP
* transformación
* carga al DW
* pipeline concurrente

---

### 3. 🔄 ETL incremental

* control de cambios
* tabla de metadata
* reejecución segura

---

### 4. 🌐 API REST

* endpoints estadísticos
* consultas optimizadas
* serialización JSON

---

### 5. 📊 Métricas y monitoreo

* logs
* conteo de registros
* tiempos de ejecución

---

### 6. 🧪 Testing

* pruebas unitarias
* pruebas de integración

---

# 🏃‍♂️ 📅 SPRINTS (propuesta realista)

👉 Sprints de **1 semana** (ideal para tu ritmo)

---

## 🟢 SPRINT 1: Fundaciones

🎯 Objetivo: tener base del sistema

### 📌 Historias

* [ ] Definir esquema estrella
* [ ] Configurar PostgreSQL
* [ ] Crear estructura del proyecto en Go
* [ ] Configuración de conexión DB
* [ ] Logger básico

### 🎁 Entregable:

* Proyecto corre
* DB lista

---

## 🔵 SPRINT 2: ETL básico (full pipeline)

🎯 Objetivo: pipeline funcionando end-to-end

### 📌 Historias

* [ ] Implementar `extract`
* [ ] Implementar `transform`
* [ ] Implementar `load`
* [ ] Pipeline con channels
* [ ] Runner ETL (`cmd/etl`)

### 🎁 Entregable:

* Datos migran OLTP → DW

---

## 🟡 SPRINT 3: Concurrencia + performance

🎯 Objetivo: ETL eficiente

### 📌 Historias

* [ ] Worker pool
* [ ] Batch processing
* [ ] Manejo de errores
* [ ] Retry básico

### 🎁 Entregable:

* ETL concurrente optimizado

---

## 🟠 SPRINT 4: ETL incremental

🎯 Objetivo: ETL inteligente

### 📌 Historias

* [ ] Tabla `etl_metadata`
* [ ] Campo `updated_at`
* [ ] Filtros incrementales
* [ ] Guardado de estado

### 🎁 Entregable:

* ETL solo procesa cambios

---

## 🔴 SPRINT 5: API REST

🎯 Objetivo: exponer datos

### 📌 Historias

* [ ] Setup servidor HTTP
* [ ] Endpoint `/stats/graduados`
* [ ] Endpoint `/stats/carrera`
* [ ] Endpoint `/stats/tendencias`

### 🎁 Entregable:

* API funcional

---

## 🟣 SPRINT 6: Integración total

🎯 Objetivo: sistema completo

### 📌 Historias

* [ ] Conectar API con DW
* [ ] Validar consistencia
* [ ] Testing básico
* [ ] Documentación inicial

---

## ⚫ SPRINT 7 (OPCIONAL PRO): Inteligencia

🎯 Objetivo: diferenciación de tesis

### 📌 Historias

* [ ] clustering
* [ ] predicción simple
* [ ] endpoints avanzados

---

# 🧾 📋 EJEMPLO DE HISTORIA DE USUARIO

```text
Como analista académico
Quiero consultar el número de graduados por carrera
Para analizar tendencias educativas
```

### ✅ Criterios de aceptación:

* devuelve JSON
* agrupado por carrera
* tiempo de respuesta < 1s

---

# 📊 🧠 DEFINICIÓN DE DONE (muy importante)

Una tarea está “hecha” si:

* ✔ Código funciona
* ✔ Compila sin errores
* ✔ Tiene logs
* ✔ Maneja errores
* ✔ Probado manualmente
* ✔ Integrado al sistema

---

# ⚙️ 🛠️ HERRAMIENTAS

* Go
* PostgreSQL
* Docker (opcional pero recomendado)
* Postman / Insomnia
* DBeaver

---

# 📈 📌 MÉTRICAS (para tu defensa)

Puedes medir:

* ⏱ tiempo ETL
* 📊 registros procesados
* ⚡ throughput
* ❌ errores

---

# 🧠 RIESGOS (y cómo mitigarlos)

| Riesgo               | Mitigación                   |
| -------------------- | ---------------------------- |
| ETL lento            | concurrencia                 |
| datos inconsistentes | validación                   |
| queries lentas       | índices DW                   |
| acoplamiento         | separación cmd/api y cmd/etl |

---

# 🚀 SIGUIENTE PASO

Si esta planificación te gusta, el siguiente paso sería:

👉 **Sprint 1 en modo implementación real**

Y empezamos con:

1. Diseño **esquema estrella basado en tu diagrama real**
2. Estructura de proyecto Go (carpetas + convenciones)
3. Setup PostgreSQL
---

# 🟢 SPRINT 1 — FUNDACIONES

## 🎯 Objetivo

Tener listo:

* esquema estrella (DW)
* base de datos PostgreSQL
* estructura del proyecto en Go
* conexión a DB
* logger básico

---

# 🧠 1. DISEÑO DEL DATA WAREHOUSE (ESQUEMA ESTRELLA)

Primero definimos **granularidad** (esto es CLAVE):

👉 **1 fila = 1 estudiante graduado (evento de graduación)**

---

## ⭐ TABLA DE HECHOS

```sql
fact_graduados
- id (PK)
- id_estudiante (FK)
- id_carrera (FK)
- id_facultad (FK)
- id_tiempo (FK)
- promedio
- tipo_tramite
- fecha_graduacion
```

---

## 📊 DIMENSIONES

### 👤 dim_estudiante

```sql
- id_estudiante (PK)
- ci
- nombre
- apellido
- genero
- fecha_nacimiento
- colegio_origen
```

---

### 🎓 dim_carrera

```sql
- id_carrera (PK)
- nombre_carrera
- nivel (licenciatura, técnico, etc.)
```

---

### 🏫 dim_facultad

```sql
- id_facultad (PK)
- nombre_facultad
```

---

### 📅 dim_tiempo

```sql
- id_tiempo (PK)
- fecha
- anio
- mes
- trimestre
```

---

## ⚡ Notas importantes (nivel DW real)

* ❗ **dim_tiempo se precarga (no viene del OLTP)**
* ❗ evitar joins complejos → ya desnormalizado
* ❗ usar índices en claves

---

# 🧱 2. SCRIPT SQL INICIAL (PostgreSQL)

```sql
CREATE TABLE dim_estudiante (
    id_estudiante SERIAL PRIMARY KEY,
    ci VARCHAR(20),
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    genero VARCHAR(10),
    fecha_nacimiento DATE,
    colegio_origen VARCHAR(255)
);

CREATE TABLE dim_carrera (
    id_carrera SERIAL PRIMARY KEY,
    nombre_carrera VARCHAR(255),
    nivel VARCHAR(50)
);

CREATE TABLE dim_facultad (
    id_facultad SERIAL PRIMARY KEY,
    nombre_facultad VARCHAR(255)
);

CREATE TABLE dim_tiempo (
    id_tiempo SERIAL PRIMARY KEY,
    fecha DATE,
    anio INT,
    mes INT,
    trimestre INT
);

CREATE TABLE fact_graduados (
    id SERIAL PRIMARY KEY,
    id_estudiante INT,
    id_carrera INT,
    id_facultad INT,
    id_tiempo INT,
    promedio NUMERIC,
    tipo_tramite VARCHAR(10),
    fecha_graduacion DATE
);
```

---

# 🗂️ 3. ESTRUCTURA DEL PROYECTO EN GO

```bash
dw-project/
│
├── cmd/
│   ├── api/
│   │   └── main.go
│   ├── etl/
│   │   └── main.go
│
├── internal/
│   ├── extract/
│   ├── transform/
│   ├── load/
│   ├── pipeline/
│   ├── repository/
│   ├── domain/
│   ├── service/
│
├── pkg/
│   ├── db/
│   ├── logger/
│   ├── config/
│
├── migrations/
├── go.mod
└── .env
```

---

# ⚙️ 4. CONFIGURACIÓN DE BASE DE DATOS

## 📄 `.env`

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=dw_universidad
```

---

## 📦 pkg/config/config.go

```go
package config

import (
    "os"
)

type Config struct {
    DBHost string
    DBPort string
    DBUser string
    DBPassword string
    DBName string
}

func LoadConfig() *Config {
    return &Config{
        DBHost: os.Getenv("DB_HOST"),
        DBPort: os.Getenv("DB_PORT"),
        DBUser: os.Getenv("DB_USER"),
        DBPassword: os.Getenv("DB_PASSWORD"),
        DBName: os.Getenv("DB_NAME"),
    }
}
```

---

## 🔌 pkg/db/db.go

```go
package db

import (
    "fmt"
    "log"
    "database/sql"

    _ "github.com/lib/pq"
    "dw-project/pkg/config"
)

func Connect(cfg *config.Config) *sql.DB {
    dsn := fmt.Sprintf(
        "host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
        cfg.DBHost,
        cfg.DBPort,
        cfg.DBUser,
        cfg.DBPassword,
        cfg.DBName,
    )

    db, err := sql.Open("postgres", dsn)
    if err != nil {
        log.Fatal(err)
    }

    if err := db.Ping(); err != nil {
        log.Fatal(err)
    }

    return db
}
```

---

# 🪵 5. LOGGER BÁSICO

## pkg/logger/logger.go

```go
package logger

import (
    "log"
)

func Info(msg string) {
    log.Println("[INFO]", msg)
}

func Error(msg string) {
    log.Println("[ERROR]", msg)
}
```

---

# 🚀 6. MAIN BÁSICO (API)

```go
package main

import (
    "fmt"
    "net/http"

    "dw-project/pkg/config"
    "dw-project/pkg/db"
)

func main() {
    cfg := config.LoadConfig()
    database := db.Connect(cfg)

    fmt.Println("DB connected:", database != nil)

    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte("API running 🚀"))
    })

    http.ListenAndServe(":8080", nil)
}
```

---

# 🚀 7. MAIN BÁSICO (ETL)

```go
package main

import (
    "fmt"

    "dw-project/pkg/config"
    "dw-project/pkg/db"
)

func main() {
    cfg := config.LoadConfig()
    database := db.Connect(cfg)

    fmt.Println("ETL listo con DB:", database != nil)
}
```

---

# ✅ ENTREGABLE DEL SPRINT 1

Debes poder:

* ✔ Crear DB en PostgreSQL
* ✔ Ejecutar scripts DW
* ✔ Levantar API → `localhost:8080`
* ✔ Ejecutar ETL sin errores
* ✔ Conexión DB funcionando

---

# 🧠 VALIDACIÓN (checklist real)

Antes de pasar al siguiente sprint:

* [ ] ¿La DB existe?
* [ ] ¿Las tablas están creadas?
* [ ] ¿Go conecta sin error?
* [ ] ¿API responde?
* [ ] ¿ETL ejecuta?

---

# 🔵 SPRINT 2 — ETL BÁSICO (PIPELINE COMPLETO)

## 🎯 Objetivo

Construir un pipeline ETL funcional:

* Extract → desde OLTP
* Transform → limpieza + adaptación a DW
* Load → inserción en DW
* Pipeline concurrente con channels
* Runner ejecutable (`cmd/etl`)

---

# 🧠 1. FLUJO DEL PIPELINE

```text
OLTP → extract → channel → transform → channel → load → DW
```

---

# 🧱 2. MODELO DE DATOS (clave para separar responsabilidades)

## 📦 internal/domain/model.go

```go
package domain

type OLTPGraduado struct {
    CI              string
    Nombre          string
    Apellido        string
    Genero          string
    Carrera         string
    Facultad        string
    Promedio        float64
    TipoTramite     string
    FechaGraduacion string
}

type DWGraduado struct {
    EstudianteID int
    CarreraID    int
    FacultadID   int
    TiempoID     int
    Promedio     float64
    TipoTramite  string
    Fecha        string
}
```

---

# ⚙️ 3. EXTRACT (leer desde OLTP)

## 📄 internal/extract/extract.go

```go
package extract

import (
    "database/sql"
    "dw-project/internal/domain"
)

func ExtractGraduados(db *sql.DB, out chan<- domain.OLTPGraduado) {
    defer close(out)

    rows, err := db.Query(`
        SELECT ci, nombre, apellido, genero, carrera, facultad,
               promedio, tipo_tramite, fecha_graduacion
        FROM oltp_graduados;
    `)
    if err != nil {
        panic(err)
    }

    defer rows.Close()

    for rows.Next() {
        var g domain.OLTPGraduado

        rows.Scan(
            &g.CI,
            &g.Nombre,
            &g.Apellido,
            &g.Genero,
            &g.Carrera,
            &g.Facultad,
            &g.Promedio,
            &g.TipoTramite,
            &g.FechaGraduacion,
        )

        out <- g
    }
}
```

---

# 🔄 4. TRANSFORM (lógica de negocio DW)

👉 Aquí haces lo importante: convertir OLTP → DW

## 📄 internal/transform/transform.go

```go
package transform

import (
    "dw-project/internal/domain"
)

func TransformGraduado(in <-chan domain.OLTPGraduado, out chan<- domain.DWGraduado) {
    for g := range in {

        dw := domain.DWGraduado{
            EstudianteID: 0, // se resolverá luego
            CarreraID:    0,
            FacultadID:   0,
            TiempoID:     0,
            Promedio:     g.Promedio,
            TipoTramite:  g.TipoTramite,
            Fecha:        g.FechaGraduacion,
        }

        out <- dw
    }
}
```

👉 Nota:
En Sprint 3 vamos a resolver IDs reales (dimensiones).

---

# 📥 5. LOAD (insertar en DW)

## 📄 internal/load/load.go

```go
package load

import (
    "database/sql"
    "dw-project/internal/domain"
)

func LoadGraduados(db *sql.DB, in <-chan domain.DWGraduado) {
    for g := range in {

        _, err := db.Exec(`
            INSERT INTO fact_graduados
            (id_estudiante, id_carrera, id_facultad, id_tiempo,
             promedio, tipo_tramite, fecha_graduacion)
            VALUES ($1,$2,$3,$4,$5,$6,$7)
        `,
            g.EstudianteID,
            g.CarreraID,
            g.FacultadID,
            g.TiempoID,
            g.Promedio,
            g.TipoTramite,
            g.Fecha,
        )

        if err != nil {
            panic(err)
        }
    }
}
```

---

# 🚀 6. PIPELINE (orquestador)

## 📄 internal/pipeline/pipeline.go

```go
package pipeline

import (
    "database/sql"

    "dw-project/internal/extract"
    "dw-project/internal/transform"
    "dw-project/internal/load"
    "dw-project/internal/domain"
)

func RunETL(db *sql.DB) {

    extractChan := make(chan domain.OLTPGraduado)
    transformChan := make(chan domain.DWGraduado)

    // Extract
    go extract.ExtractGraduados(db, extractChan)

    // Transform
    go func() {
        transform.TransformGraduado(extractChan, transformChan)
        close(transformChan)
    }()

    // Load
    load.LoadGraduados(db, transformChan)
}
```

---

# 🏃‍♂️ 7. RUNNER ETL

## 📄 cmd/etl/main.go

```go
package main

import (
    "dw-project/pkg/config"
    "dw-project/pkg/db"
    "dw-project/internal/pipeline"
    "dw-project/pkg/logger"
)

func main() {
    cfg := config.LoadConfig()
    database := db.Connect(cfg)

    logger.Info("Iniciando ETL...")

    pipeline.RunETL(database)

    logger.Info("ETL finalizado ✅")
}
```

---

# ⚡ 8. PRUEBA RÁPIDA

Antes de correr:

👉 necesitas una tabla OLTP mock:

```sql
CREATE TABLE oltp_graduados (
    ci VARCHAR(20),
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    genero VARCHAR(10),
    carrera VARCHAR(100),
    facultad VARCHAR(100),
    promedio NUMERIC,
    tipo_tramite VARCHAR(10),
    fecha_graduacion DATE
);
```

---

# 🧠 9. QUÉ LOGRAMOS EN ESTE SPRINT

✔ Pipeline ETL completo
✔ Separación por capas
✔ Uso de channels (Go idiomático)
✔ Flujo funcional end-to-end

---

# 🚨 LIMITACIONES ACTUALES (intencional)

Todavía NO tenemos:

* ❌ manejo de dimensiones (IDs reales)
* ❌ concurrencia avanzada
* ❌ batch insert
* ❌ incremental

👉 eso viene en los siguientes sprints

---

# 🧠 CHECKPOINT (importante)

Antes de avanzar:

* [ ] ¿Se leen datos del OLTP?
* [ ] ¿Se insertan en fact?
* [ ] ¿No crashea?
* [ ] ¿Pipeline fluye?

---
