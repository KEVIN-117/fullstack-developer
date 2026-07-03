# 📚 Apuntes y Conceptos Clave - Módulo 2: Software Dev & CI/CD

Notas de estudio sobre compilación eficiente, concurrencia, modularidad de interfaces y automatización.

---

## 🏎️ Concurrencia y Paralelismo en Go
*   **Goroutines:** Son hilos virtuales ligeros gestionados por el propio runtime de Go (no por el kernel del sistema operativo). Ocupan muy poca memoria RAM (apenas unos KB) y permiten crear miles de ellos simultáneamente. Se invocan usando la palabra clave `go` antes de una función.
*   **Channels:** Mecanismos seguros de comunicación y sincronización de datos entre Goroutines sin necesidad de usar bloqueos manuales de memoria (Mutex).
*   **sync.WaitGroup:** Estructura que permite bloquear la ejecución de un proceso principal hasta que un grupo de Goroutines termine su trabajo.

---

## 🏗️ Component Driven Development (CDD)
Es una metodología de desarrollo de software enfocada en construir interfaces de usuario "de abajo hacia arriba" (Bottom-Up), empezando por los componentes más pequeños y simples (botones, inputs) y combinándolos para formar estructuras más complejas (formularios, vistas, páginas).
*   **Aislamiento:** Los componentes no deben acoplarse directamente a bases de datos ni a clientes de APIs globales. Deben depender puramente de parámetros recibidos (`Props`) y manejar estados internos mínimos.
*   **Mocks:** Permite probar el comportamiento visual y de interacción inyectando datos estáticos de prueba (Mock Data) antes de conectar el frontend al backend real en producción.

---

## 📦 Docker Multi-stage Builds
Es una técnica de optimización de imágenes que permite utilizar múltiples instrucciones `FROM` en un solo archivo `Dockerfile`.
1.  **Fase de Compilación (Builder Stage):** Utiliza una imagen base pesada que incluye el SDK completo (ej. Golang SDK o Node.js con `npm`), compiladores y herramientas de desarrollo para generar el binario de ejecución o empaquetar los archivos de producción.
2.  **Fase de Ejecución (Runtime Stage):** Copia únicamente el binario compilado o los archivos HTML/JS minificados a una imagen extremadamente ligera (ej. `alpine` o `distroless`), descartando todo el SDK de desarrollo.
*   **Beneficios:** Reduce drásticamente el tamaño de la imagen final (de ~1 GB a ~20 MB) y disminuye el número de paquetes vulnerables.

---

## 🤖 Arquitectura del GitHub Actions Self-Hosted Runner
A diferencia de los servicios que requieren abrir puertos en tu firewall local para que GitHub envíe alertas (Webhooks), el Runner Autohospedado utiliza un modelo de **extracción (Pulling)**.
*   El agente del runner realiza una conexión constante de larga duración (Websocket/Long polling) saliente hacia los servidores de GitHub.
*   Cuando hay un trabajo disponible, el runner lo descarga a través de esa conexión abierta y lo ejecuta localmente.
*   **Ventaja:** Permite automatizar despliegues dentro de tu Home Lab sin abrir ningún puerto entrante en tu router hogareño hacia el exterior (el firewall local UFW se mantiene blindado).
