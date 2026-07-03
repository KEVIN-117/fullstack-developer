# Stage 3: Streams

## 📌 Objetivo

Implementar Streams, una estructura de datos poderosa para registros de eventos, análisis y logs en tiempo real.

## 🎯 Tareas

1. **The TYPE command** - Identificar tipo de dato
2. **Create a stream** - XADD para crear streams
3. **Validating entry IDs** - Validación de IDs de entrada
4. **Partially auto-generated IDs** - IDs parcialmente autogeneradas
5. **Fully auto-generated IDs** - IDs completamente autogeneradas
6. **Query entries from stream** - XRANGE para consultar
7. **Query with -** - Rango desde inicio
8. **Query with +** - Rango hasta fin
9. **Query single stream using XREAD** - XREAD en stream único
10. **Query multiple streams using XREAD** - XREAD en múltiples streams
11. **Blocking reads** - XREAD con bloqueo
12. **Blocking reads without timeout** - Bloqueo indefinido
13. **Blocking reads using $** - Bloqueo desde nuevas entradas

## 📋 Requisitos

- [ ] XADD: Agregar entrada a stream
- [ ] TYPE: Retornar tipo de dato
- [ ] XRANGE: Obtener rango de entradas
- [ ] XREAD: Leer de uno o múltiples streams
- [ ] XREAD BLOCK: Lectura bloqueante
- [ ] ID autogeneración con timestamp y secuencia
- [ ] Soporte para $ (últimas entradas)

## 🔗 Referencias

- [Redis Streams](https://redis.io/commands/?group=stream)
- [Stream Documentation](https://redis.io/docs/latest/develop/data-types/streams/)
