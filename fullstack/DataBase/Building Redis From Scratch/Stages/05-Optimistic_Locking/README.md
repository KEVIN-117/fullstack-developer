# Stage 5: Optimistic Locking

## 📌 Objetivo

Implementar mecanismos de bloqueo optimista usando WATCH para control de concurrencia sin deadlocks.

## 🎯 Tareas

1. **The WATCH command** - Monitorear claves para cambios
2. **WATCH inside transaction** - WATCH con MULTI/EXEC
3. **Tracking key modifications** - Detectar modificaciones
4. **Watching multiple keys** - Monitorear múltiples claves
5. **Watching missing keys** - WATCH en claves inexistentes
6. **The UNWATCH command** - Dejar de monitorear
7. **Unwatch on EXEC** - UNWATCH automático en EXEC
8. **Unwatch on DISCARD** - UNWATCH automático en DISCARD

## 📋 Requisitos

- [ ] WATCH: Monitorear claves
- [ ] Detección de cambios en claves monitoreadas
- [ ] UNWATCH: Remover monitoreo
- [ ] Cancelación de transacción si hay cambios
- [ ] Soporte de múltiples WATCH
- [ ] Limpieza automática en EXEC/DISCARD

## 📚 Conceptos Clave

- **Optimistic Locking**: Suposición de no conflicto
- **Compare-and-Swap**: Verificación antes de escribir
- **Conflict Detection**: Detección de cambios
- **Retry Logic**: Reintentos en conflictos

## 🔗 Referencias

- [WATCH Command](https://redis.io/commands/watch/)
- [Optimistic Locking Docs](https://redis.io/docs/latest/develop/interact/transactions/)
