# Stage 4: Transactions

## 📌 Objetivo

Implementar transacciones ACID que permiten ejecutar múltiples comandos de forma atómica y aislada.

## 🎯 Tareas

1. **The INCR command (1/3)** - Incrementar valores
2. **The INCR command (2/3)** - INCR avanzado
3. **The INCR command (3/3)** - INCR completo
4. **The MULTI command** - Iniciar transacción
5. **The EXEC command** - Ejecutar transacción
6. **Empty transaction** - Transacciones vacías
7. **Queueing commands** - Encolamiento de comandos
8. **Executing a transaction** - Ejecución atómica
9. **The DISCARD command** - Cancelar transacción
10. **Failures within transactions** - Manejo de errores
11. **Multiple transactions** - Soporte de múltiples transacciones

## 📋 Requisitos

- [ ] INCR: Incrementar contador
- [ ] MULTI: Comenzar transacción
- [ ] EXEC: Ejecutar transacción de forma atómica
- [ ] DISCARD: Cancelar transacción encolada
- [ ] Encolamiento de comandos durante MULTI
- [ ] Manejo de errores en transacciones
- [ ] Aislamiento entre transacciones

## 📚 Conceptos Clave

- **ACID Properties**: Atomicidad, Consistencia, Aislamiento, Durabilidad
- **Command Queueing**: Buffering de comandos
- **Atomic Execution**: Ejecución indivisible
- **Error Handling**: Manejo de fallos

## 🔗 Referencias

- [Redis Transactions](https://redis.io/commands/?group=transaction)
- [Transactions Documentation](https://redis.io/docs/latest/develop/interact/transactions/)
