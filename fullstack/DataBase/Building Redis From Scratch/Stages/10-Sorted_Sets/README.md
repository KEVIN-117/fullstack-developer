# Stage 10: Sorted Sets

## 📌 Objetivo

Implementar Sorted Sets - conjuntos ordenados por score con búsquedas eficientes.

## 🎯 Tareas

1. **Create a sorted set** - ZADD para crear
2. **Add members** - ZADD con múltiples miembros
3. **Retrieve member rank** - ZRANK de miembro
4. **List sorted set members** - ZRANGE
5. **ZRANGE with negative indexes** - ZRANGE con índices negativos
6. **Count sorted set members** - ZCARD
7. **Retrieve member score** - ZSCORE
8. **Remove a member** - ZREM

## 📋 Requisitos

- [ ] ZADD: Agregar miembros con score
- [ ] ZRANGE: Obtener rango ordenado
- [ ] ZRANK: Obtener rango de miembro
- [ ] ZSCORE: Obtener score de miembro
- [ ] ZCARD: Contar miembros
- [ ] ZREM: Remover miembro
- [ ] Índices negativos en ZRANGE
- [ ] Estructura eficiente (skip list)

## 📚 Conceptos Clave

- **Skip List**: Estructura de datos ordenada
- **Score-based Ordering**: Ordenamiento por score
- **Range Queries**: Consultas por rango
- **Rank Lookups**: Búsqueda de posición

## 🔗 Referencias

- [Sorted Set Commands](https://redis.io/commands/?group=sorted_set)
- [Sorted Sets Documentation](https://redis.io/docs/latest/develop/data-types/sorted-sets/)
