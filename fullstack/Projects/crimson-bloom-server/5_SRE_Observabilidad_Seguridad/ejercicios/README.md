# 📝 Ejercicios Prácticos - Módulo 5: SRE, Observabilidad & Seguridad

Pon a prueba tu infraestructura de monitoreo y endurece la seguridad del sistema resolviendo los siguientes retos prácticos.

---

## 🏃‍♂️ Ejercicio 1: Métricas Personalizadas en la API (Business Metrics)
No te limites a monitorear métricas del sistema (CPU/RAM). Aprende a exponer métricas de negocio para entender qué está pasando a nivel aplicativo.
*   **Instrucciones:**
    1. Agrega una métrica de tipo **Counter** (Contador) en tu API de producción del Módulo 2 utilizando el SDK de Prometheus. Llama a la métrica `facturas_procesadas_total`.
    2. Incrementa este contador cada vez que el endpoint `/api/data` o `/predict` procese una transacción con éxito.
    3. Añade etiquetas (labels) al contador para diferenciar la categoría (ej: `categoria="Equipos"`, `categoria="Servicios"`).
    4. Consulta tu endpoint `/metrics` en el navegador y verifica que la métrica aparezca listada.
*   **Criterio de Aceptación:** Ver en Prometheus y Grafana un gráfico de barras que desglose la cantidad total de facturas procesadas acumuladas por categoría.

---

## 🔄 Ejercicio 2: Alertas de Contenedor Caído
La observabilidad no consiste en sentarse a ver dashboards, sino en dejar que el sistema te avise cuando ocurre un desastre.
*   **Instrucciones:**
    1. Levanta el servicio **Alertmanager** junto a Prometheus en tu Compose.
    2. Crea un archivo `alert.rules.yml` en la carpeta de Prometheus y define una regla de alerta llamada `InstanceDown` que se dispare si un contenedor (como `api-backend`) está caído por más de 1 minuto.
    3. Conecta Alertmanager con un canal de webhook gratuito (como Discord, Slack o Telegram) para recibir la notificación en tu teléfono o PC cliente.
    4. Prueba la alerta deteniendo tu backend (`docker compose stop api-backend`) y esperando la notificación.
*   **Pistas:** Usa la expresión PromQL `up == 0` para verificar la disponibilidad de los servicios scrapeados.

---

## 💾 Ejercicio 3: Hardening del Servidor según Auditoría de Lynis
Aprende a interpretar reportes de seguridad reales y a corregir debilidades en Debian.
*   **Instrucciones:**
    1. Corre una auditoría de sistema completa con Lynis: `sudo lynis audit system`.
    2. Revisa el reporte generado en `/var/log/lynis-report.dat` o la sección "Suggestions" de la consola.
    3. Selecciona al menos 3 sugerencias de seguridad clasificadas de prioridad alta o media (ej: deshabilitar USB storage si no se usa, configurar políticas de expiración de contraseñas de usuarios en `/etc/login.defs`, o asegurar los permisos del cargador de arranque GRUB).
    4. Aplica las correcciones en el servidor Debian y vuelve a ejecutar Lynis para comprobar que el puntaje general de seguridad (Hardening Index) ha aumentado.

---

## 🔒 Ejercicio 4: Control de Calidad de Seguridad en CI/CD (Trivy Gate)
Asegura que tu pipeline bloquee automáticamente cualquier software que contenga brechas de seguridad críticas.
*   **Instrucciones:**
    1. Modifica el flujo de trabajo de GitHub Actions en tu runner.
    2. Agrega una tarea posterior a la construcción de las imágenes de Docker.
    3. Configura **Trivy** en modo bloqueo (`--exit-code 1`) para que analice la imagen recién creada.
    4. Ajusta Trivy para ignorar vulnerabilidades que aún no tienen parche del desarrollador (`--ignore-unpatched`), de modo que solo falle con vulnerabilidades críticas que sí podrías solucionar actualizando las librerías.
*   **Criterio de Aceptación:** Simula un fallo de seguridad agregando una dependencia desactualizada y vulnerable en tu backend. Haz push y verifica que el pipeline de GitHub Actions se detiene e impide el despliegue automático del contenedor roto.
