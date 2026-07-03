# Stage 12: Authentication

## 📌 Objetivo

Implementar sistema de autenticación y control de acceso con ACL (Access Control Lists).

## 🎯 Tareas

1. **Respond to ACL WHOAMI** - Identificar usuario actual
2. **Respond to ACL GETUSER** - Obtener información de usuario
3. **The nopass flag** - Flag sin contraseña
4. **The passwords property** - Propiedad de contraseñas
5. **Setting default user password** - Contraseña del usuario default
6. **The AUTH command** - Autenticación
7. **Enforce authentication** - Requerir autenticación
8. **Authenticate using AUTH** - Usar AUTH

## 📋 Requisitos

- [ ] ACL WHOAMI: Obtener usuario actual
- [ ] ACL GETUSER: Información de usuario
- [ ] AUTH: Autenticación con contraseña
- [ ] ACL management: Crear/modificar usuarios
- [ ] Passwords: Hashing y validación
- [ ] Permissions: Control de acceso
- [ ] Default user: Usuario por defecto

## 📚 Conceptos Clave

- **ACL Model**: Control de acceso basado en listas
- **Password Hashing**: Seguridad de contraseñas
- **User Permissions**: Permisos granulares
- **Authentication Flow**: Flujo de autenticación

## 🔗 Referencias

- [ACL Documentation](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/)
- [AUTH Command](https://redis.io/commands/auth/)
- [ACL Commands](https://redis.io/commands/?group=server&subgroup=acl)
