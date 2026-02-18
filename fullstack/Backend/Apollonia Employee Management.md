## 1️⃣ ¿Qué es lo que se requiere? (requisitos claros)

### Requisitos funcionales (lo mínimo indispensable)

Basado en el briefing :

#### Entidades

* **Employees**

  * Nombre
  * Apellido
  * Departamento (relación)
* **Departments**

  * Nombre del departamento

#### Funcionalidad

* CRUD completo para:

  * Employees
  * Departments
* Visualización en UI web
* Relación empleado → departamento
* API REST para manejar datos

#### Datos iniciales

* 10 empleados
* 5 departamentos
* Relación ya definida (puede ser seed o manual)

---

### Requisitos técnicos

* Backend: **Node.js + Express**
* DB: **MongoDB**
* ODM: **Mongoose**
* Frontend: **HTML + CSS + JS vanilla**
* Comunicación: **REST API (JSON)**
* Contenerización: **Docker + docker-compose**

---

### Requisitos no funcionales

* Código entendible (nivel entry-level)
* Fácil de extender en el futuro
* Separación clara de responsabilidades
* Funcione con `docker-compose up`

---

## 2️⃣ Cómo será la solución (visión general)

Vamos a construir una **arquitectura clásica de 3 capas**, simple pero profesional:

```
[ Browser ]
     |
     v
[ Frontend (HTML/CSS/JS) ]
     |
     v
[ REST API - Node.js + Express ]
     |
     v
[ MongoDB ]
```

Todo dentro de Docker.

---

## 3️⃣ Herramientas a usar (stack definitivo)

### Backend

* Node.js
* Express
* Mongoose
* dotenv
* cors (opcional pero recomendable)

### Base de datos

* MongoDB (contenedor Docker)
* Mongo Express (opcional para debug rápido)

### Frontend

* HTML
* CSS
* JavaScript (fetch API)

### Infraestructura

* Docker
* docker-compose

### Dev tools

* VS Code
* Postman / Thunder Client (para testear API)

---

## 4️⃣ Modelo de datos (clave para hacerlo rápido)

### Department (colección)

```js
{
  _id: ObjectId,
  name: String
}
```

### Employee (colección)

```js
{
  _id: ObjectId,
  firstName: String,
  lastName: String,
  department: ObjectId (ref: "Department")
}
```

👉 **Decisión importante (buena práctica)**
Usar referencias (`ObjectId`) y no strings → escalable para futuro CRM.

---

## 5️⃣ Arquitectura del backend (escalable pero simple)

Estructura de carpetas recomendada:

```
backend/
├── src/
│   ├── config/
│   │   └── db.js
│   ├── models/
│   │   ├── Employee.js
│   │   └── Department.js
│   ├── routes/
│   │   ├── employee.routes.js
│   │   └── department.routes.js
│   ├── controllers/
│   │   ├── employee.controller.js
│   │   └── department.controller.js
│   ├── app.js
│   └── server.js
├── Dockerfile
├── package.json
└── .env
```

### Principios aplicados

* **Separación de responsabilidades**
* **Escalabilidad** (futuro: patients, projects, etc.)
* **Fácil testeo**

---

## 6️⃣ Arquitectura de la API REST

### Departments

| Método | Endpoint               | Acción     |
| ------ | ---------------------- | ---------- |
| GET    | `/api/departments`     | Listar     |
| POST   | `/api/departments`     | Crear      |
| PUT    | `/api/departments/:id` | Actualizar |
| DELETE | `/api/departments/:id` | Eliminar   |

### Employees

| Método | Endpoint             | Acción                |
| ------ | -------------------- | --------------------- |
| GET    | `/api/employees`     | Listar (con populate) |
| POST   | `/api/employees`     | Crear                 |
| PUT    | `/api/employees/:id` | Actualizar            |
| DELETE | `/api/employees/:id` | Eliminar              |

---

## 7️⃣ Frontend (mínimo viable y rápido)

### Páginas

* `index.html`

  * Lista de empleados
  * Formulario para crear/editar
* `departments.html`

  * CRUD de departamentos

### Comunicación

* `fetch()` contra la API
* JSON
* Sin frameworks (más rápido, menos setup)

---

## 8️⃣ Dockerización (clave para aprobar y practicar)

### Servicios en docker-compose

```yaml
services:
  api:
    build: ./backend
    ports:
      - "3000:3000"
    env_file:
      - .env
    depends_on:
      - mongo

  mongo:
    image: mongo
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
```

👉 Esto demuestra **entendimiento real de backend profesional**.

---

## 9️⃣ Plan de ejecución cronometrado (FAST MODE ⚡)

### ⏱️ Fase 1 – Setup (30–45 min)

* Init Node
* Instalar deps
* Docker + docker-compose
* Conexión Mongo

### ⏱️ Fase 2 – Backend core (60–90 min)

* Models
* Controllers
* Routes
* Test API con Postman

### ⏱️ Fase 3 – Frontend (60 min)

* HTML básico
* JS con fetch
* CRUD funcional

### ⏱️ Fase 4 – Seed + polish (30 min)

* Datos iniciales
* Populate departments
* README

⏱️ **Total estimado: 3.5 – 4.5 horas**

---

## 🔟 ¿Por qué esta arquitectura es buena a futuro?

✔ Permite agregar:

* Patients
* Projects
* Trainings
* Revenue

✔ Permite:

* Autenticación
* Roles
* Escalado horizontal
* Frontend framework más adelante

✔ Es exactamente lo que espera un evaluador técnico

---

Perfecto 😈⏱️
Vamos con el **CHECKLIST EXACTO TIPO EXAMEN**, pensado para:

* No pensar de más
* No olvidar nada evaluable
* Poder ir marcando ✔ mientras avanzas
* Terminar **rápido y limpio**

Imagina que esto lo tienes impreso al lado.

---

# ✅ CHECKLIST OFICIAL – Employee Management CRUD App

*Apollonia Dental Practice*

---

## 🧩 FASE 0 — Preparación (ANTES de escribir código)

⬜ Leer Business Briefing
⬜ Identificar entidades:

* Employees
* Departments

⬜ Decidir stack:

* Node.js
* Express
* MongoDB
* Mongoose
* Docker

⬜ Crear carpeta raíz del proyecto

---

## ⚙️ FASE 1 — Inicialización del proyecto

### Node.js

⬜ `npm init -y`
⬜ Instalar dependencias:

* express
* mongoose
* dotenv
* cors (opcional)

⬜ Crear estructura base:

```
src/
 ├─ app.js
 ├─ server.js
 ├─ config/
 ├─ models/
 ├─ routes/
 └─ controllers/
```

⬜ Configurar script en `package.json`:

* `"start": "node src/server.js"`
* `"dev": "nodemon src/server.js"` (opcional)

---

## 🗄️ FASE 2 — Base de datos (MongoDB + Mongoose)

### Conexión

⬜ Crear `src/config/db.js`
⬜ Conectar a MongoDB usando `mongoose.connect`
⬜ Usar variable de entorno `MONGO_URI`

---

### Modelos

#### Department

⬜ Crear `Department.js`
⬜ Campos:

* name (String, required, unique)

#### Employee

⬜ Crear `Employee.js`
⬜ Campos:

* firstName (String, required)
* lastName (String, required)
* department (ObjectId, ref: Department)

⬜ Exportar modelos correctamente

---

## 🧠 FASE 3 — Lógica de negocio (Controllers)

### Departments Controller

⬜ Crear departamento
⬜ Obtener todos los departamentos
⬜ Actualizar departamento
⬜ Eliminar departamento

---

### Employees Controller

⬜ Crear empleado
⬜ Obtener empleados
⬜ Usar `.populate("department")`
⬜ Actualizar empleado
⬜ Eliminar empleado

⬜ Manejar errores básicos (`try/catch`)

---

## 🌐 FASE 4 — Rutas REST API

### Departments Routes

⬜ `GET /api/departments`
⬜ `POST /api/departments`
⬜ `PUT /api/departments/:id`
⬜ `DELETE /api/departments/:id`

---

### Employees Routes

⬜ `GET /api/employees`
⬜ `POST /api/employees`
⬜ `PUT /api/employees/:id`
⬜ `DELETE /api/employees/:id`

⬜ Registrar rutas en `app.js`

---

## 🚀 FASE 5 — Servidor Express

⬜ Configurar `app.js`:

* express.json()
* cors
* rutas API

⬜ Crear `server.js`:

* importar app
* conectar DB
* escuchar puerto

⬜ Probar que el servidor levanta correctamente

---

## 🧪 FASE 6 — Testing de API (OBLIGATORIO)

⬜ Probar endpoints con Postman:

* Crear departamento
* Crear empleado
* Listar empleados con departamento
* Actualizar empleado
* Eliminar empleado

⬜ Verificar datos en MongoDB

---

## 🎨 FASE 7 — Frontend (mínimo viable)

### Estructura

⬜ Crear carpeta `public/`
⬜ Archivos:

* index.html
* departments.html
* style.css
* script.js

---

### Funcionalidad

⬜ Mostrar lista de empleados
⬜ Formulario para crear empleado
⬜ Dropdown con departamentos
⬜ Botón eliminar empleado
⬜ CRUD básico de departamentos

⬜ Uso de `fetch()` a la API

---

## 🐳 FASE 8 — Dockerización

### Dockerfile (Backend)

⬜ Usar imagen oficial Node
⬜ Copiar package.json
⬜ Instalar dependencias
⬜ Copiar código
⬜ Exponer puerto 3000
⬜ Comando `npm start`

---

### docker-compose.yml

⬜ Servicio API
⬜ Servicio MongoDB
⬜ Volumen persistente
⬜ Variables de entorno
⬜ `depends_on` configurado

⬜ `docker-compose up` funciona sin errores

---

## 📦 FASE 9 — Datos iniciales (PLUS)

⬜ Crear departamentos iniciales
⬜ Crear empleados iniciales
⬜ Relación correcta empleado → departamento

*(manual o seed script)*

---

## 📝 FASE 10 — Entrega

⬜ Proyecto corre con un solo comando
⬜ API documentada (README corto)
⬜ Estructura clara y ordenada
⬜ Código entendible (sin hacks raros)

---

## 🧠 CHECKLIST MENTAL DEL EVALUADOR

✔ Usa REST correctamente
✔ Relación entre colecciones
✔ CRUD completo
✔ Docker funcional
✔ Pensado para crecer

---