# ⚙️ Módulo 2: Desarrollo e Integración Continua (Software & DevOps)

Este módulo conecta tus habilidades de programador con las de DevOps, estructurando tus proyectos de código fuente y automatizando su despliegue seguro.

---

## 🗺️ Roadmaps de Referencia Integrados
Para profundizar en la teoría de este módulo, abre y estudia las siguientes rutas de especialización:
*   📄 **[golang.pdf](../roadmaps/Skill%20Based%20Roadmaps/golang.pdf)** & **[nodejs.pdf](../roadmaps/Skill%20Based%20Roadmaps/nodejs.pdf)**: Sintaxis de Go, concurrencia de goroutines, y modularidad TS en Node.
*   📄 **[api-design.pdf](../roadmaps/Skill%20Based%20Roadmaps/api-design.pdf)** & **[backend.pdf](../roadmaps/Role%20Based%20Roadmaps/backend.pdf)**: Diseño de APIs RESTful y códigos HTTP.
*   📄 **[design-system.pdf](../roadmaps/Skill%20Based%20Roadmaps/design-system.pdf)** & **[frontend.pdf](../roadmaps/Role%20Based%20Roadmaps/frontend.pdf)**: CDD, componentes modulares e interfaces reutilizables.
*   📄 **[git-github.pdf](../roadmaps/Skill%20Based%20Roadmaps/git-github.pdf)** & **[devsecops.pdf](../roadmaps/Role%20Based%20Roadmaps/devsecops.pdf)** (Sección CI/CD): Automatizaciones locales de Git y hardening de Dockerfiles.

---

## 📋 Checklist General del Módulo
- [ ] Desarrollar una API RESTful en Go o NestJS que exponga endpoints `/health` y `/api/data`.
- [ ] Crear un frontend interactivo en Vite + React aplicando Component Driven Development (CDD).
- [ ] Escribir archivos `Dockerfile` optimizados mediante Multi-stage Builds para ambos servicios.
- [ ] Asegurar que las imágenes finales corran bajo usuarios sin privilegios root.
- [ ] Desplegar un GitHub Actions Runner local contenerizado y enlazado al repositorio.
- [ ] Crear un workflow de integración continua (`deploy.yml`) que ejecute pruebas unitarias y redespliegue automáticamente al hacer `git push`.
- [ ] Validar que un push en caliente actualice la web en producción sin intervención manual.

---

## 📚 Tópicos y Submódulos de Aprendizaje

### ⚡ Submódulo 2.1: Desarrollo de APIs REST (Go o NestJS)
*   **Objetivo:** Desarrollar un servicio backend modular con buenas prácticas estructurales y manejo de peticiones concurrentes.
*   **Tópicos Relacionados:** [2.1_Desarrollo_APIs.md](./topicos/2.1_Desarrollo_APIs.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Cómo funciona la concurrencia a nivel de sistema operativo vs. goroutines ligeras (en Go)?
    - [ ] Importancia del desacoplamiento de capas (Controladores, Servicios, Repositorios).
    - [ ] Uso correcto de códigos de estado HTTP y serialización de datos JSON.

---

### 🎨 Submódulo 2.2: Frontend Modular con CDD (React + Vite)
*   **Objetivo:** Diseñar interfaces de usuario modulares, mantenibles y fáciles de testear.
*   **Tópicos Relacionados:** [2.2_Frontend_CDD.md](./topicos/2.2_Frontend_CDD.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Qué es Component Driven Development (CDD) y por qué previene acoplamientos visuales?
    - [ ] Diferencia entre componentes puros de presentación y componentes contenedores de lógica.
    - [ ] Aislamiento de estilos mediante CSS Modules para evitar colisiones de clases CSS.

---

### 📦 Submódulo 2.3: Compilaciones Docker Multi-stage
*   **Objetivo:** Generar imágenes de producción extremadamente ligeras y seguras eliminando herramientas de desarrollo.
*   **Tópicos Relacionados:** [2.3_Docker_MultiStage.md](./topicos/2.3_Docker_MultiStage.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] ¿Por qué un compilador o gestor de paquetes (npm/gcc) no debe estar en la imagen final?
    - [ ] Ventajas de seguridad de usar bases minimalistas como Alpine o Distroless.
    - [ ] ¿Cómo impacta la ejecución del comando `USER` en la seguridad de Docker ante exploits de escalada de privilegios?

---

### 🤖 Submódulo 2.4: Servidores de Automatización Autohospedados (Runner CI/CD)
*   **Objetivo:** Automatizar el ciclo de vida del software de forma local y privada.
*   **Tópicos Relacionados:** [2.4_Agente_Runner_CICD.md](./topicos/2.4_Agente_Runner_CICD.md)
*   **Checklist de Conceptos a Aprender:**
    - [ ] Diferencia de arquitectura entre el envío de webhooks (push) y el polling de runners (pull).
    - [ ] ¿Por qué montar `/var/run/docker.sock` en el runner le permite crear contenedores hermanos (Docker-out-of-Docker)?
    - [ ] Estructura de pipelines declarativos y manejo seguro de variables de entorno (Secrets).

---

## 🔍 Guía de Diagnóstico (Troubleshooting)

| Error Común | Causa Probable | Comando de Diagnóstico / Solución |
| :--- | :--- | :--- |
| **`Permission denied` al montar `docker.sock`** | El usuario del runner no tiene permisos para leer el socket de Docker en Debian. | En el Host Debian: Asegura permisos con `sudo chmod 666 /var/run/docker.sock`. |
| **El Runner de GitHub aparece offline** | El contenedor del runner no puede conectar a GitHub debido a un Token inválido. | Obtén un token nuevo desde la configuración del repositorio en GitHub Actions. |
| **`CORS Policy` en el navegador** | Peticiones a dominios cruzados directas al puerto del backend. | Asegúrate de que las consultas pasen por el proxy Nginx en `homelab.local/api/`. |
| **Imagen Docker de gran tamaño (> 1 GB)** | No utilizaste multi-stage builds y quedaron dependencias de compilación. | Asegúrate de copiar solo los binarios o la carpeta `/dist` a una base final `alpine`. |
