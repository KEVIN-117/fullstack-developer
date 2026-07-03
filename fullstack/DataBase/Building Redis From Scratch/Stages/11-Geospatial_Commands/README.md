# Stage 11: Geospatial Commands

## 📌 Objetivo

Implementar comandos geoespaciales para trabajar con coordenadas y búsquedas por radio.

## 🎯 Tareas

1. **Respond to GEOADD** - Agregar ubicaciones
2. **Validate coordinates** - Validar latitud/longitud
3. **Store a location** - Almacenar ubicaciones
4. **Calculate location score** - Calcular score geohash
5. **Respond to GEOPOS** - Obtener posiciones
6. **Decode coordinates** - Decodificar geohash
7. **Calculate distance** - GEODIST entre puntos
8. **Search within radius** - GEORADIUS búsqueda

## 📋 Requisitos

- [ ] GEOADD: Agregar coordinadas
- [ ] GEOPOS: Obtener coordenadas
- [ ] GEODIST: Calcular distancia
- [ ] GEORADIUS: Búsqueda por radio
- [ ] Geohashing: Codificación espacial
- [ ] Validación de coordenadas
- [ ] Cálculo de distancias (haversine)

## 📚 Conceptos Clave

- **Geohashing**: Codificación de coordenadas
- **Haversine Formula**: Cálculo de distancias
- **Spatial Indexing**: Indexación espacial
- **Radius Search**: Búsquedas por proximidad

## 🔗 Referencias

- [Geo Commands](https://redis.io/commands/?group=geo)
- [Geospatial Indexes](https://redis.io/docs/latest/develop/data-types/geospatial/)
