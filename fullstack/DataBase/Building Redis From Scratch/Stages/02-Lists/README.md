# Stage 2: Lists

## 📌 Objetivo

Implementar soporte para el tipo de dato List en Redis. Las listas son colecciones ordenadas de strings que permiten operaciones en ambos extremos.

## 🎯 Tareas

1. **Create a list** - LPUSH, RPUSH para crear listas
2. **Append an element** - RPUSH para agregar elemento al final
3. **Append multiple elements** - Múltiples elementos en RPUSH
4. **List elements (positive indexes)** - LRANGE con índices positivos
5. **List elements (negative indexes)** - LRANGE con índices negativos
6. **Prepend elements** - LPUSH para agregar al inicio
7. **Query list length** - LLEN para obtener longitud
8. **Remove an element** - LPOP, RPOP para eliminar
9. **Remove multiple elements** - Eliminar múltiples elementos
10. **Blocking retrieval** - BLPOP con timeout
11. **Blocking retrieval with timeout** - BRPOP con manejo de timeouts

## 📋 Requisitos

- [ ] Implementar estructura List internamente
- [ ] LPUSH: Agregar elemento al inicio
- [ ] RPUSH: Agregar elemento al final
- [ ] LRANGE: Obtener elementos en rango
- [ ] LPOP: Remover del inicio
- [ ] RPOP: Remover del final
- [ ] LLEN: Obtener longitud
- [ ] BLPOP: Blocking pop con timeout
- [ ] BRPOP: Blocking pop al final con timeout

## 🔧 Implementación

```
02-Lists/
├── README.md
├── requirements.md
├── checklist.md
├── implementation/
│   ├── list.rs
│   ├── commands.rs
│   └── blocking.rs
└── tests/
    ├── test_push_pop.rs
    ├── test_range.rs
    └── test_blocking.rs
```

## 🧪 Criterios de Aceptación

- [ ] LPUSH/RPUSH crean y almacenan listas
- [ ] LRANGE retorna elementos con índices positivos y negativos
- [ ] LPOP/RPOP remueven y retornan elementos
- [ ] LLEN retorna la longitud correcta
- [ ] BLPOP/BRPOP manejan bloqueos con timeout

## 📚 Conceptos Clave

- **Data Structures**: Listas en memoria
- **Queue/Stack Operations**: FIFO/LIFO con PUSH/POP
- **Blocking Operations**: Sincronización entre clientes
- **Índices Negativos**: Acceso desde el final

## 🔗 Referencias

- [Redis List Commands](https://redis.io/commands/?group=list)
- [CodeCrafters Stage](https://app.codecrafters.io/courses/redis/stages/mh6)
