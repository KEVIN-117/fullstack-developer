# Checklist - Core Commands

## ✅ Requisitos Previos

- [ ] Entorno de desarrollo configurado
- [ ] Compilador/Intérprete listo
- [ ] Git inicializado
- [ ] Redis CLI instalado (para testing)

## 🔧 Tareas de Implementación

### Socket & Networking

- [ ] Crear socket TCP
- [ ] Bindear a puerto 6379
- [ ] Escuchar conexiones entrantes
- [ ] Aceptar múltiples conexiones concurrentes
- [ ] Manejo de conexiones cerradas

### Protocolo RESP

- [ ] Parsear comandos RESP
- [ ] Construir respuestas RESP
- [ ] Manejar diferentes tipos de datos (strings, arrays, integers)
- [ ] Error handling en protocolo

### Almacenamiento

- [ ] HashMap/Dictionary para almacenar datos
- [ ] Estructura para guardar TTL
- [ ] Timer/scheduler para expiración

### Comandos Básicos

- [ ] **PING** → PONG
- [ ] **ECHO** → retornar mensaje
- [ ] **SET key value** → OK
- [ ] **GET key** → value
- [ ] **EXISTS key** → 0/1
- [ ] **DEL key** → número eliminado
- [ ] **EXPIRE key seconds** → 1/0
- [ ] **TTL key** → segundos restantes

## 🧪 Testing

- [ ] Test para cada comando
- [ ] Test de concurrencia (múltiples clientes)
- [ ] Test de expiración
- [ ] Test de protocolo RESP

## 📊 Criterios de Aceptación

- [ ] `redis-cli` se conecta sin errores
- [ ] `redis-cli ping` retorna PONG
- [ ] SET/GET funcionan correctamente
- [ ] Múltiples clientes pueden conectarse
- [ ] Las claves expiran en el tiempo especificado
- [ ] El servidor maneja desconexiones correctamente

## 🚀 Hito

Después de esto, tendrás un servidor Redis básico pero funcional.
