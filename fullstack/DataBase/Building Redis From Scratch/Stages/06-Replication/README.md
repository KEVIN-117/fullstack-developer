# Stage 6: Replication

## 📌 Objetivo

Implementar replicación master-replica para distribuir datos entre múltiples instancias de Redis.

## 🎯 Tareas

1. **Configure listening port** - Puerto de escucha para replicas
2. **The INFO command** - Información del servidor
3. **The INFO command on a replica** - INFO en réplica
4. **Initial replication ID and offset** - IDs de replicación
5. **Send handshake (1/3)** - Protocolo de handshake
6. **Send handshake (2/3)** - Sincronización inicial
7. **Send handshake (3/3)** - Completar handshake
8. **Receive handshake (1/2)** - Recibir handshake
9. **Receive handshake (2/2)** - Procesar handshake
10. **Empty RDB transfer** - Transferencia RDB
11. **Single-replica propagation** - Propagar a una replica
12. **Multi-replica propagation** - Propagar a múltiples replicas
13. **Command processing** - Procesamiento de comandos
14. **ACKs with no commands** - ACK sin comandos
15. **ACKs with commands** - ACK con comandos
16. **WAIT with no replicas** - WAIT sin replicas
17. **WAIT with no commands** - WAIT sin comandos
18. **WAIT with multiple commands** - WAIT con múltiples comandos

## 📋 Requisitos

- [ ] Protocolo handshake master-replica
- [ ] INFO command con estado de replicación
- [ ] Transferencia RDB inicial
- [ ] Propagación de comandos a replicas
- [ ] ACKs de replicas
- [ ] WAIT command para sincronización
- [ ] Replication ID y offset tracking

## 📚 Conceptos Clave

- **Master-Replica Architecture**: Distribución de datos
- **Replication Handshake**: Protocolo de sincronización
- **RDB Snapshots**: Transferencia de estado
- **Command Propagation**: Sincronización de cambios
- **Write Safety**: Confirmación de replicas

## 🔗 Referencias

- [Replication Documentation](https://redis.io/docs/latest/operate/oss_and_stack/management/replication/)
- [INFO Command](https://redis.io/commands/info/)
- [WAIT Command](https://redis.io/commands/wait/)
