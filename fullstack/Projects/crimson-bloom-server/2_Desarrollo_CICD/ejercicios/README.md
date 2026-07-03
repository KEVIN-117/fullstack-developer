# 📝 Ejercicios Prácticos - Módulo 2: Software Dev & CI/CD

Refuerza tus habilidades de desarrollo y automatización ejecutando las siguientes tareas avanzadas.

---

## 🏃‍♂️ Ejercicio 1: Concurrencia en Go (Procesamiento en Paralelo)
Si elegiste Go para tu backend, aprenderás a usar Goroutines y Channels para acelerar la respuesta de la API consumiendo múltiples recursos concurrentemente.
*   **Instrucciones:**
    1. Crea un endpoint `/api/data` en tu servidor Go.
    2. Simula la consulta a 3 fuentes de datos externas independientes (por ejemplo, 3 funciones diferentes que tardan 1 segundo cada una en responder usando `time.Sleep`).
    3. Implementa Goroutines para ejecutar estas 3 consultas en paralelo en lugar de secuencialmente.
    4. Utiliza un `sync.WaitGroup` o canales (`chan`) para esperar los resultados y unirlos.
*   **Criterio de Aceptación:** El endpoint debe responder en aproximadamente 1 segundo en total (en lugar de 3 segundos) y devolver los datos de las tres fuentes consolidados en la respuesta JSON.

---

## 🎨 Ejercicio 2: Component Driven Development (CDD) con React
Diseña y valida un componente de interfaz reutilizable y aislado utilizando Mock Data antes de conectarlo al backend real.
*   **Instrucciones:**
    1. Diseña un componente de React llamado `TransactionTable` para mostrar una lista de transacciones.
    2. El componente debe aceptar propiedades (`Props`) que definan: la lista de datos a mostrar, el estado de carga (`loading`), y una función de callback para cuando se haga clic en una transacción.
    3. Diseña el componente de manera puramente visual (CSS aislado en un archivo `.module.css`) sin importar llamadas a la red (`fetch` o `axios`) en su interior.
    4. En tu página principal, renderiza este componente pasándole datos ficticios (mock data) simulando el backend.
*   **Pistas:** Mantener la lógica de negocio (llamadas API) en componentes contenedores de nivel superior y la lógica de presentación (UI) en componentes puros en niveles inferiores.

---

## 🔄 Ejercicio 3: Rollback Automático en CI/CD
Añade robustez a tus despliegues automáticos asegurándote de que no se publiquen versiones rotas o defectuosas.
*   **Instrucciones:**
    1. Modifica tu workflow de GitHub Actions.
    2. Añade un paso final después de hacer el despliegue con Docker Compose que realice una petición HTTP al endpoint `/health` del nuevo backend.
    3. Si la API no responde con un código de estado `200 OK` en 30 segundos, el pipeline debe considerarse fallido.
    4. En caso de fallo, el runner debe ejecutar automáticamente un comando de restauración para revertir a la imagen Docker anterior que sí funcionaba.
*   **Pistas:** Puedes etiquetar tus imágenes con el hash del commit (`github.sha`) y mantener una etiqueta `:stable` para realizar la reversión en caso de error.

---

## 🔒 Ejercicio 4: Evitar Ejecución de Contenedores como Root
Por motivos de seguridad informática (hardening de Docker), nunca debes permitir que los procesos dentro del contenedor corran con privilegios de root del Host Debian.
*   **Instrucciones:**
    1. Modifica el `Dockerfile` de tu backend (o frontend).
    2. Crea un usuario del sistema sin privilegios (ej. `node` o `appuser`) en la fase final de ejecución del contenedor.
    3. Usa la directiva `USER appuser` en tu Dockerfile para asegurar que el comando de ejecución inicial (`ENTRYPOINT` o `CMD`) corra bajo este usuario.
    4. Verifica que funciona construyendo y ejecutando el contenedor locally.
