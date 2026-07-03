# Redis Implementation - Stages

Esta carpeta contiene la estructura incremental para construir Redis desde cero. Cada carpeta representa una fase del desarrollo, progresando desde funcionalidades básicas hasta características avanzadas.

## 📋 Estructura de Stages

### 1. **Core Commands** (Fundamentos)

- [Bind to a port](https://app.codecrafters.io/courses/redis/introduction)
- [Respond to PING](https://app.codecrafters.io/courses/redis/stages/rg2)
- [Respond to multiple PINGs](https://app.codecrafters.io/courses/redis/stages/wy1)
- [Handle concurrent clients](https://app.codecrafters.io/courses/redis/stages/zu2)
- [Implement the ECHO command](https://app.codecrafters.io/courses/redis/stages/qq0)
- [Implement the SET & GET commands](https://app.codecrafters.io/courses/redis/stages/la7)
- [Expiry](https://app.codecrafters.io/courses/redis/stages/yz1)

### 2. **Lists** (Estructuras de Datos)

Implementación de comandos para trabajar con listas en Redis.

### 3. **Streams** (Procesamiento en Tiempo Real)

Soporte para streams, un tipo de dato para logs y análisis.

### 4. **Transactions** (Operaciones Atómicas)

Implementación de MULTI, EXEC, DISCARD y manejo de transacciones.

### 5. **Optimistic Locking** (Control de Concurrencia)

WATCH, UNWATCH y mecanismos de bloqueo optimista.

### 6. **Replication** (Replicación Master-Replica)

Sincronización de datos entre servidores Redis.

### 7. **RDB Persistence** (Persistencia Snapshot)

Almacenamiento y recuperación de datos mediante RDB.

### 8. **AOF Persistence** (Persistencia Log)

Append-Only File para persistencia basada en logs.

### 9. **Pub/Sub** (Publicador/Suscriptor)

Sistema de mensajería pub/sub para comunicación en tiempo real.

### 10. **Sorted Sets** (Conjuntos Ordenados)

Estructuras de datos ordenadas por score.

### 11. **Geospatial Commands** (Comandos Geoespaciales)

Soporte para datos geoespaciales y búsquedas por radio.

### 12. **Authentication** (Autenticación y ACL)

Sistema de autenticación y control de acceso.

## 🚀 Cómo Usar Esta Estructura

1. **Comienza con Core Commands**: Los fundamentos básicos para que Redis sea funcional
2. **Construye incrementalmente**: Cada stage se basa en el anterior
3. **Dentro de cada carpeta**:
   - `README.md`: Descripción y objetivos del stage
   - `requirements.md`: Requisitos técnicos y cambios necesarios
   - `tests/`: Casos de prueba para validar implementación
   - `implementation/`: Código de implementación
   - `checklist.md`: Lista de verificación de tareas

## ✅ Progreso

| Stage                  | Estado         | Completitud |
| ---------------------- | -------------- | ----------- |
| 01-Core_Commands       | ⏳ No iniciado | 0%          |
| 02-Lists               | ⏳ No iniciado | 0%          |
| 03-Streams             | ⏳ No iniciado | 0%          |
| 04-Transactions        | ⏳ No iniciado | 0%          |
| 05-Optimistic_Locking  | ⏳ No iniciado | 0%          |
| 06-Replication         | ⏳ No iniciado | 0%          |
| 07-RDB_Persistence     | ⏳ No iniciado | 0%          |
| 08-AOF_Persistence     | ⏳ No iniciado | 0%          |
| 09-Pub_Sub             | ⏳ No iniciado | 0%          |
| 10-Sorted_Sets         | ⏳ No iniciado | 0%          |
| 11-Geospatial_Commands | ⏳ No iniciado | 0%          |
| 12-Authentication      | ⏳ No iniciado | 0%          |

## 📚 Referencias

- [Redis Protocol (RESP)](https://redis.io/docs/latest/develop/reference/protocol-spec/)
- [Redis Commands](https://redis.io/commands/)
- [CodeCrafters Redis Challenge](https://app.codecrafters.io/courses/redis)
