# 🗂️ Índice de Stages - Navegación Rápida

## 📌 Estructura Organizativa

Este documento te ayuda a navegar entre todas las fases de construcción de Redis.

---

## 🎯 Stages por Dificultad

### ⭐ Principiante (Empieza aquí)

1. **[01-Core_Commands](./01-Core_Commands/)**
   - 🎯 Objetivo: Servidor TCP básico
   - 📋 [README](./01-Core_Commands/README.md) | [CHECKLIST](./01-Core_Commands/CHECKLIST.md)
   - 📝 Comandos: PING, ECHO, SET, GET, EXPIRE
   - ⏱️ Tiempo: 2-3 semanas

2. **[02-Lists](./02-Lists/)**
   - 🎯 Objetivo: Listas (Queues/Stacks)
   - 📋 [README](./02-Lists/README.md)
   - 📝 Comandos: LPUSH, RPUSH, LPOP, RPOP, LRANGE

3. **[09-Pub_Sub](./09-Pub_Sub/)**
   - 🎯 Objetivo: Mensajería Publish/Subscribe
   - 📋 [README](./09-Pub_Sub/README.md)
   - 📝 Comandos: SUBSCRIBE, PUBLISH, UNSUBSCRIBE

---

### ⭐⭐ Intermedio

4. **[03-Streams](./03-Streams/)**
   - 🎯 Objetivo: Logs y análisis en tiempo real
   - 📋 [README](./03-Streams/README.md)
   - 📝 Comandos: XADD, XRANGE, XREAD

5. **[04-Transactions](./04-Transactions/)**
   - 🎯 Objetivo: Operaciones atómicas ACID
   - 📋 [README](./04-Transactions/README.md)
   - 📝 Comandos: MULTI, EXEC, DISCARD, INCR

6. **[07-RDB_Persistence](./07-RDB_Persistence/)**
   - 🎯 Objetivo: Snapshots a disco
   - 📋 [README](./07-RDB_Persistence/README.md)
   - 📝 Funcionalidades: Guardar y recuperar estado

---

### ⭐⭐⭐ Avanzado

7. **[05-Optimistic_Locking](./05-Optimistic_Locking/)**
   - 🎯 Objetivo: Control de concurrencia sin deadlocks
   - 📋 [README](./05-Optimistic_Locking/README.md)
   - 📝 Comandos: WATCH, UNWATCH

8. **[08-AOF_Persistence](./08-AOF_Persistence/)**
   - 🎯 Objetivo: Log de comandos (Append-Only File)
   - 📋 [README](./08-AOF_Persistence/README.md)
   - 📝 Funcionalidades: Escribir, replayear comandos

9. **[10-Sorted_Sets](./10-Sorted_Sets/)**
   - 🎯 Objetivo: Conjuntos ordenados por score
   - 📋 [README](./10-Sorted_Sets/README.md)
   - 📝 Comandos: ZADD, ZRANGE, ZRANK, ZSCORE

10. **[12-Authentication](./12-Authentication/)**
    - 🎯 Objetivo: ACL y autenticación
    - 📋 [README](./12-Authentication/README.md)
    - 📝 Comandos: AUTH, ACL WHOAMI, ACL GETUSER

---

### ⭐⭐⭐⭐ Experto

11. **[06-Replication](./06-Replication/)**
    - 🎯 Objetivo: Master-Replica replication
    - 📋 [README](./06-Replication/README.md)
    - 📝 Conceptos: Handshake, RDB transfer, Command propagation

12. **[11-Geospatial_Commands](./11-Geospatial_Commands/)**
    - 🎯 Objetivo: Queries geoespaciales
    - 📋 [README](./11-Geospatial_Commands/README.md)
    - 📝 Comandos: GEOADD, GEOPOS, GEODIST, GEORADIUS

---

## 🔗 Rutas de Aprendizaje Recomendadas

### 🚀 Ruta Rápida (4-6 semanas)

```
01-Core_Commands → 02-Lists → 09-Pub_Sub → FIN
```

**Resultado:** Sistema de mensajería en tiempo real

### 🎓 Ruta Estándar (8-12 semanas)

```
01-Core_Commands
  → 02-Lists
  → 03-Streams
  → 04-Transactions
  → 07-RDB_Persistence
  → 08-AOF_Persistence
  → 09-Pub_Sub
  → FIN
```

**Resultado:** Redis funcional con persistencia

### 🏆 Ruta Completa (4-6 meses)

```
01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12
```

**Resultado:** Redis production-ready

---

## 📚 Documentación Principal

| Documento                                            | Propósito                         |
| ---------------------------------------------------- | --------------------------------- |
| [README.md](./README.md)                             | Visión general de los Stages      |
| [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md) | Guía completa con tips y recursos |
| [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)           | Referencia rápida de estructura   |
| **Este archivo**                                     | Índice de navegación              |

---

## 🎯 Cómo Navegar

### Opción 1: Por Dificultad

👆 Comienza en la sección **⭐ Principiante** arriba

### Opción 2: Por Interés

```
Quiero:                    → Ve a:
- Básicos                  → 01-Core_Commands
- Estructuras de datos     → 02-Lists, 10-Sorted_Sets
- Real-time               → 03-Streams, 09-Pub_Sub
- Durabilidad             → 07-RDB_Persistence, 08-AOF_Persistence
- Escalabilidad           → 06-Replication
- Seguridad               → 12-Authentication
- Geo/Maps                → 11-Geospatial_Commands
```

### Opción 3: Orden Recomendado

Sigue la numeración: 01 → 02 → 03 → ... → 12

---

## 📂 Estructura de Cada Stage

```
XX-StageName/
├── README.md              ← Lee primero
├── CHECKLIST.md          ← Sigue esto
├── implementation/       ← Tu código aquí
├── tests/                ← Tus tests aquí
└── docs/                 ← Notas adicionales
```

---

## ✅ Checklist para Empezar

- [ ] Leer el README.md del stage elegido
- [ ] Revisar el CHECKLIST.md
- [ ] Configurar el entorno (compilador, herramientas)
- [ ] Crear estructura inicial en `implementation/`
- [ ] Escribir primeros tests en `tests/`
- [ ] Implementar funcionalidades
- [ ] Validar con `redis-cli`
- [ ] Commit a Git

---

## 🤔 Preguntas Frecuentes

**¿Por dónde empiezo?**
→ Comienza con [01-Core_Commands](./01-Core_Commands/)

**¿Puedo saltar stages?**
→ No, cada uno se basa en el anterior. Sigue el orden.

**¿Cuánto tiempo toma?**
→ Depende de tu experiencia:

- Principiante: 4-6 meses (completo)
- Intermedio: 2-3 meses (completo)
- Avanzado: 4-6 semanas (completo)

**¿Qué lenguaje uso?**
→ Elige cualquiera: Rust, Python, Go, C, Java...

**¿Hay soluciones?**
→ No, es un desafío de aprendizaje. Experimenta y aprende.

---

## 🚀 ¡Comienza Ahora!

👉 **[Abre 01-Core_Commands](./01-Core_Commands/README.md)** y comienza tu viaje construyendo Redis.

---

**Última actualización:** 2025  
**Status:** ✅ Estructura lista  
**Próximo paso:** Selecciona un stage e implementa 🎉
