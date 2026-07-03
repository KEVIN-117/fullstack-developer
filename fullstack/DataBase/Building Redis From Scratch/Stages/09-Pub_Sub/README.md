# Stage 9: Pub/Sub

## 📌 Objetivo

Implementar Publish/Subscribe para mensajería en tiempo real entre clientes.

## 🎯 Tareas

1. **Subscribe to a channel** - SUBSCRIBE a canal
2. **Subscribe to multiple channels** - SUBSCRIBE múltiples
3. **Enter subscribed mode** - Modo suscripción
4. **PING in subscribed mode** - PING en modo suscrito
5. **Publish a message** - PUBLISH mensaje
6. **Deliver messages** - Entregar a suscriptores
7. **Unsubscribe** - UNSUBSCRIBE

## 📋 Requisitos

- [ ] SUBSCRIBE: Suscribirse a canales
- [ ] PUBLISH: Publicar en canales
- [ ] UNSUBSCRIBE: Cancelar suscripción
- [ ] Modo suscripción del cliente
- [ ] Entrega de mensajes en tiempo real
- [ ] Patrón matching (PSUBSCRIBE)

## 📚 Conceptos Clave

- **Pub/Sub Model**: Publicador/Suscriptor
- **Message Delivery**: Entrega en tiempo real
- **Channel Subscriptions**: Suscripciones por canal
- **Pattern Matching**: Coincidencia de patrones

## 🔗 Referencias

- [Pub/Sub Commands](https://redis.io/commands/?group=pubsub)
- [Pub/Sub Documentation](https://redis.io/docs/latest/develop/interact/pubsub/)
