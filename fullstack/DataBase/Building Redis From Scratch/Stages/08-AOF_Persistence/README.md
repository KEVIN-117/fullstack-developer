# Stage 8: AOF Persistence

## 📌 Objetivo

Implementar AOF (Append-Only File) - persistencia basada en logs de comandos.

## 🎯 Tareas

1. **Default AOF options** - Opciones por defecto
2. **AOF options from flags** - Configuración desde flags
3. **Create append-only directory** - Crear directorio
4. **Create append-only file** - Crear archivo AOF
5. **Create manifest file** - Crear manifest
6. **Write a single command** - Escribir comando
7. **Write multiple commands** - Múltiples comandos
8. **Filter write commands** - Filtrar comandos de escritura
9. **Replay a single command** - Replayear comando único
10. **Replay multiple commands** - Replayear múltiples

## 📋 Requisitos

- [ ] Formato AOF
- [ ] Escritura de comandos
- [ ] Lectura y replay de AOF
- [ ] Manifest file para management
- [ ] Rewrite de AOF

## 📚 Conceptos Clave

- **AOF Format**: Log de comandos
- **Write Ahead Logging**: Escribir antes de ejecutar
- **Replay**: Recuperación mediante replay
- **AOF Rewrite**: Compresión del log

## 🔗 Referencias

- [AOF Persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/aof/)
- [AOF Protocol](https://redis.io/docs/latest/develop/reference/protocol-spec/)
