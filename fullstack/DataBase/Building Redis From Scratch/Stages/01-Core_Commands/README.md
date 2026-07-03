# Stage 1: Core Commands

## 📌 Objetivo

Implementar los fundamentos básicos de un servidor Redis: conectarse a un puerto TCP, responder a comandos básicos (PING, ECHO) y implementar los comandos GET/SET para almacenamiento clave-valor.

## 🎯 Tareas

1. **Bind to a port** - Conectar el servidor a un puerto TCP y escuchar conexiones
2. **Respond to PING** - Implementar respuesta a comando PING
3. **Respond to multiple PINGs** - Manejar múltiples comandos PING en la misma conexión
4. **Handle concurrent clients** - Soportar múltiples clientes simultáneamente
5. **Implement ECHO command** - Eco de mensajes del cliente
6. **Implement SET & GET commands** - Almacenamiento y recuperación clave-valor
7. **Expiry** - Soporte para claves con tiempo de expiración

## 📋 Requisitos

- [ ] Servidor TCP escuchando en puerto configurable (default: 6379)
- [ ] Protocolo RESP (Redis Serialization Protocol) implementado
- [ ] Manejo de conexiones múltiples concurrentes
- [ ] Almacén clave-valor en memoria
- [ ] Soporte para TTL (Time To Live) en claves
- [ ] Respuestas correctas según especificación RESP

## 🔧 Implementación

### Estructura de Carpetas

```
01-Core_Commands/
├── README.md
├── requirements.md
├── checklist.md
├── implementation/
│   ├── server.rs (o tu lenguaje)
│   ├── protocol.rs
│   ├── storage.rs
│   └── main.rs
└── tests/
    ├── test_ping.rs
    ├── test_echo.rs
    ├── test_get_set.rs
    └── test_expiry.rs
```

## 🧪 Criterios de Aceptación

- [x] El servidor se inicia y escucha en el puerto 6379
- [x] Responde correctamente a PING
- [x] Maneja múltiples comandos PING
- [x] Soporta múltiples clientes concurrentes
- [x] ECHO retorna el mensaje recibido
- [x] SET almacena valores y GET los recupera
- [x] Las claves con TTL se eliminan automáticamente

## 📚 Conceptos Clave

- **TCP Sockets**: Programación de redes de bajo nivel
- **Protocolo RESP**: Formato de serialización de Redis
- **Concurrencia**: Manejo de múltiples clientes
- **Almacenamiento en Memoria**: Data structures básicas

## 🔗 Referencias

- [Redis Protocol Specification](https://redis.io/docs/latest/develop/reference/protocol-spec/)
- [Redis Commands: PING, ECHO, SET, GET](https://redis.io/commands/)
- [CodeCrafters Stage](https://app.codecrafters.io/courses/redis/introduction)

## 📝 Notas

Después de completar este stage, tendrás un servidor Redis funcional capaz de servir comandos básicos. Este es el fundamento sobre el cual se construirán todas las demás características.
