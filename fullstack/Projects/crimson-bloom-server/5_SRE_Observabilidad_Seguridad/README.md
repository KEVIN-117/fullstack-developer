# 📈 Módulo 5: SRE, Observabilidad y DevSecOps Avanzado (Monitoreo & Seguridad)

Este módulo final cierra tu formación técnica como profesional de infraestructura, enseñándote a medir la fiabilidad de tus sistemas y a protegerlos de forma proactiva.

---

## 🗺️ Roadmaps de Referencia Integrados
Para profundizar en la teoría de este módulo, abre y estudia las siguientes rutas de especialización:
*   📄 **[devops.pdf](../roadmaps/Role%20Based%20Roadmaps/devops.pdf)** (Sección SRE & Telemetry): Telemetría, recolección de métricas con Prometheus y alertas automatizadas.
*   📄 **[system-design.pdf](../roadmaps/Skill%20Based%20Roadmaps/system-design.pdf)** (Sección Monitoreo): Indicadores clave de rendimiento (KPIs), telemetría distribuida y tolerancia a fallos.
*   📄 **[devsecops.pdf](../roadmaps/Role%20Based%20Roadmaps/devsecops.pdf)** & **[cyber-security.pdf](../roadmaps/Role%20Based%20Roadmaps/cyber-security.pdf)** (Sección Audits): Escaneo estático de imágenes Docker con Trivy y hardening del Host Debian con Lynis.

---

## 📋 Checklist General del Módulo
- [ ] Desplegar Prometheus, Grafana, Node Exporter y cAdvisor usando Docker Compose.
- [ ] Configurar las tareas de scraping de Prometheus para recolectar métricas del host y de los contenedores.
- [ ] Integrar instrumentación en tu API de producción para exponer métricas en el endpoint `/metrics`.
- [ ] Configurar Prometheus como fuente de datos en Grafana de manera segura.
- [ ] Diseñar un panel (dashboard) en Grafana que unifique uso de hardware e indicadores de latencia/solicitudes de tu API.
- [ ] Configurar reglas de alerta en Alertmanager para notificaciones automatizadas.
- [ ] Ejecutar auditorías de seguridad en el host físico (Lynis) y en tus imágenes de Docker (Trivy).
- [ ] Resolver todos los desafíos prácticos de la sección `/ejercicios`.

---

## 📚 Tópicos y Submódulos de Aprendizaje

### 📊 Submódulo 5.1: Recolección y Almacenamiento de Métricas (Prometheus)
*   **Objetivo:** Implementar una base de datos de series temporales capaz de consultar y almacenar telemetría de red y hardware.
*   **Tópicos Relacionados:** [5.1_Metricas_Prometheus.md](./topicos/5.1_Metricas_Prometheus.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Cómo funciona el modelo de scraping (Pull) de Prometheus frente al modelo push?
    - [ ] Uso de exportadores especializados: Node Exporter (hardware físico) y cAdvisor (recursos de contenedores).
    - [ ] Entender el lenguaje de consultas PromQL y la estructura de una serie temporal dimensional.

---

### 🎨 Submódulo 5.2: Visualización con Grafana
*   **Objetivo:** Diseñar interfaces analíticas dinámicas que informen sobre la salud de los servicios en tiempo real.
*   **Tópicos Relacionados:** [5.2_Visualizacion_Grafana.md](./topicos/5.2_Visualizacion_Grafana.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] Las 4 señales doradas de SRE: Latencia, Tráfico, Errores y Saturación.
    - [ ] Estructura de dashboards representados como archivos JSON portables.
    - [ ] ¿Cómo configurar alertas basadas en umbrales tolerables (Alertmanager)?

---

### 🛡️ Submódulo 5.3: DevSecOps y Análisis de Seguridad
*   **Objetivo:** Integrar escaneos de vulnerabilidades en el ciclo de vida del desarrollo y auditar el endurecimiento del servidor.
*   **Tópicos Relacionados:** [5.3_DevSecOps_Auditorias.md](./topicos/5.3_DevSecOps_Auditorias.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Qué es una vulnerabilidad CVE (Common Vulnerabilities and Exposures) y cómo la explota Trivy?
    - [ ] Concepto de escaneo estático de imágenes frente a análisis dinámico de sistemas (auditorías locales).
    - [ ] Prácticas recomendadas de Hardening de Linux (seguridad del Kernel, gestión de pam, permisos de archivos).

---

## 🔍 Guía de Diagnóstico (Troubleshooting)

| Error Común | Causa Probable | Comando de Diagnóstico / Solución |
| :--- | :--- | :--- |
| **`cAdvisor: Permission denied`** | cAdvisor no puede leer directorios del host Debian debido a restricciones. | Asegúrate de montar los volúmenes en modo lectura (`:ro`). |
| **Grafana muestra "No Data"** | Rango de tiempo incorrecto o scraping target caído. | Revisa el panel de Prometheus en `http://localhost:9090/targets` y valida que estén `UP`. |
| **`Trivy: connection refused`** | La máquina del runner no tiene acceso a Internet para descargar la base de datos de CVEs. | Asegura que el DNS del runner permita conexiones salientes. |
| **Alertmanager no envía alertas** | La configuración del webhook contiene URLs incorrectas o formato de regla inválido. | Revisa los logs de alertmanager y valida sintaxis con `amtool`. |
