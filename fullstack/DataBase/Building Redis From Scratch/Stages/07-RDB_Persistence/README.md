# Stage 7: RDB Persistence

## 📌 Objetivo

Implementar persistencia mediante RDB (Redis Database) - snapshots del estado completo de Redis en disco.

## 🎯 Tareas

1. **RDB file config** - Configuración de archivos RDB
2. **Read a key** - Leer una clave del RDB
3. **Read a string value** - Leer valores string
4. **Read multiple keys** - Leer múltiples claves
5. **Read multiple string values** - Múltiples valores string
6. **Read value with expiry** - Leer con TTL

## 📋 Requisitos

- [ ] Formato RDB completo
- [ ] Lectura de archivos RDB
- [ ] Recuperación de datos
- [ ] Soporte de TTL en RDB
- [ ] Verificación de integridad

## 📚 Conceptos Clave

- **RDB Format**: Formato binario de Redis
- **Snapshots**: Captura de estado
- **Serialization**: Serialización de datos
- **Recovery**: Recuperación de datos

## 🔗 Referencias

- [RDB Format Documentation](https://github.com/antirez/redis/blob/unstable/docs/rdb_format.md)
- [RDB Config](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/rdb/)
