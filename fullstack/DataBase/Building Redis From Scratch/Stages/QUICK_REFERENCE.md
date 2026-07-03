# 🎯 Redis Stages - Quick Reference

## 📍 Ubicación: `Stages/`

Cada carpeta representa una fase del desarrollo de Redis, con todos los recursos necesarios para implementar esa funcionalidad.

---

## 🗂️ Estructura de Carpeta (Ejemplo)

```
01-Core_Commands/
├── README.md              # Descripción y objetivos del stage
├── CHECKLIST.md          # Tareas a completar
├── requirements.md       # Requisitos técnicos (por crear)
│
├── implementation/       # Código de implementación
│   ├── server.rs
│   ├── protocol.rs
│   ├── storage.rs
│   └── main.rs
│
├── tests/                # Suite de pruebas
│   ├── test_ping.rs
│   ├── test_echo.rs
│   ├── test_get_set.rs
│   └── test_concurrency.rs
│
└── docs/                 # Documentación adicional
    ├── RESP_protocol.md
    ├── Architecture.md
    └── Learnings.md
```

---

## 🔄 Flujo de Uso

1. **Lee el README.md** → Entiende los objetivos
2. **Revisa CHECKLIST.md** → Sigue las tareas
3. **Implementa en implementation/** → Tu código aquí
4. **Prueba con tests/** → Valida tu implementación
5. **Commit & Move On** → Pasa al siguiente stage

---

## 📋 Lista de Stages

| #    | Nombre             | Nivel    | Prerequisito |
| ---- | ------------------ | -------- | ------------ |
| 1️⃣   | Core Commands      | ⭐       | Ninguno      |
| 2️⃣   | Lists              | ⭐⭐     | Stage 1      |
| 3️⃣   | Streams            | ⭐⭐⭐   | Stage 1-2    |
| 4️⃣   | Transactions       | ⭐⭐⭐   | Stage 1-3    |
| 5️⃣   | Optimistic Locking | ⭐⭐⭐⭐ | Stage 4      |
| 6️⃣   | Replication        | ⭐⭐⭐⭐ | Stage 1-5    |
| 7️⃣   | RDB Persistence    | ⭐⭐⭐   | Stage 1-3    |
| 8️⃣   | AOF Persistence    | ⭐⭐⭐   | Stage 7      |
| 9️⃣   | Pub/Sub            | ⭐⭐     | Stage 1-2    |
| 🔟   | Sorted Sets        | ⭐⭐⭐   | Stage 1-2    |
| 🔟1️⃣ | Geospatial         | ⭐⭐⭐⭐ | Stage 10     |
| 🔟2️⃣ | Authentication     | ⭐⭐⭐   | Stage 1-9    |

---

## 🎓 Archivos Importantes

### En la Raíz de Stages:

- **README.md** → Descripción general
- **IMPLEMENTATION_GUIDE.md** → Ruta de aprendizaje recomendada
- **QUICK_REFERENCE.md** → Este archivo

### En Cada Carpeta:

- **README.md** → Objetivos del stage
- **CHECKLIST.md** → Tareas específicas
- **requirements.md** → Especificaciones técnicas (en progreso)

---

## 🚀 Cómo Empezar

```bash
# 1. Ve a la carpeta del primer stage
cd 01-Core_Commands

# 2. Lee el README
cat README.md

# 3. Consulta el checklist
cat CHECKLIST.md

# 4. Comienza a implementar en implementation/
cd implementation
# ... tu código aquí ...

# 5. Escribe pruebas en tests/
cd ../tests
# ... tus tests aquí ...

# 6. Cuando todo funcione, commit
git add .
git commit -m "Complete Core Commands stage"
```

---

## 💡 Tips

✅ **DO:**

- Leer TODO el README antes de empezar
- Completar CHECKLIST en orden
- Escribir tests mientras implementas
- Hacer commits frecuentes
- Documentar lo que aprendas

❌ **DON'T:**

- Saltar stages
- Ignorar errores de RESP protocol
- No probar con redis-cli
- Hacer cambios masivos sin tests
- Olvidar commits regularmente

---

## 🔗 Navegación

- 📌 [Volver al README Principal](./README.md)
- 📘 [Ver Guía Completa de Implementación](./IMPLEMENTATION_GUIDE.md)
- 🎯 [Empezar con Core Commands](./01-Core_Commands/README.md)

---

**Last Updated:** 2025-Q2  
**Status:** Structure Ready for Implementation 🚀
