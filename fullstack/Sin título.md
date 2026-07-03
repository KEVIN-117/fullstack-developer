# Roadmap del Proyecto: App de Sincronización Unidireccional

| **Sprint**   | **Nombre de la Fase**       | **Objetivo Principal del Sprint**                                                                             | **Entregable Clave**                                                                                                                           |
| ------------ | --------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Sprint 1** | **Cimientos y Nube**        | Configurar el proyecto, integrar el SDK de Google y lograr la autenticación del usuario.                      | La app permite al usuario iniciar sesión con Google y muestra en la consola un listado crudo de los archivos de su Drive.                      |
| **Sprint 2** | **Puentes Locales (SAF)**   | Implementar la interfaz básica de configuración y dominar la escritura en el almacenamiento local de Android. | El usuario puede seleccionar la carpeta destino local. La app puede crear un archivo `.md` de prueba dentro de esa carpeta usando SAF.         |
| **Sprint 3** | **Clonación Inicial**       | Construir la lógica central para descargar la jerarquía de archivos y carpetas desde Drive al móvil.          | Al presionar "Sincronizar", la app descarga todo el Vault (archivos y subcarpetas) de Drive a la carpeta local seleccionada.                   |
| **Sprint 4** | **Sincronización Delta**    | Implementar la base de datos local (Room) y los tokens de la API para optimizar las descargas.                | La app ya no descarga todo de nuevo; detecta qué cambió en Drive (modificaciones, creaciones, eliminaciones) y actualiza solo eso en el móvil. |
| **Sprint 5** | **Automatización y Pulido** | Hacer que la sincronización sea invisible y robusta ante fallos de red.                                       | La app se sincroniza sola en segundo plano (WorkManager) cada cierto tiempo, maneja errores sin cerrarse y muestra logs claros al usuario.     |
## Sprint 1: Cimientos y Nube

**Objetivo:** El usuario puede iniciar sesión con su cuenta de Google y la app es capaz de imprimir en la consola de Android Studio la lista de archivos de su Google Drive.

| **ID**  | **Tarea**                                 | **Descripción Técnica**                                                                                                                                                                                                                                       | **Estimación** |
| ------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| **1.1** | **Setup del Proyecto y Arquitectura**     | Crear el proyecto en Android Studio (Kotlin + Jetpack Compose). Configurar los `build.gradle` (dependencias de Hilt/Koin para inyección, Coroutines, Google Play Services). Crear la estructura de carpetas para las capas: `presentation`, `domain`, `data`. | 2 horas        |
| **1.2** | **Configuración en Google Cloud Console** | Crear un nuevo proyecto en la consola de Google Cloud. Habilitar la "Google Drive API". Configurar la pantalla de consentimiento de OAuth 2.0 y generar los credenciales (Client ID de Android usando la huella SHA-1 de tu entorno de debug).                | 1.5 horas      |
| **1.3** | **UI de Autenticación (CDD)**             | Crear la pantalla inicial usando Component Driven Development (CDD) en Jetpack Compose. Construir componentes aislados: `LoginScreen`, `GoogleSignInButton` y un estado básico de carga (`LoadingSpinner`).                                                   | 2 horas        |
| **1.4** | **Implementar Flujo de Google Sign-In**   | Integrar Google Identity Services (Credential Manager o la API clásica de Sign-In). Manejar el intent de login, capturar el resultado y extraer la cuenta de Google autenticada junto con sus scopes (permisos para Drive).                                   | 3 horas        |
| **1.5** | **Cliente Base de Drive API v3**          | Crear el servicio en la capa `data` que inicializa el cliente `Drive` usando la cuenta autenticada. Configurar el transporte HTTP y el parseador JSON de Google.                                                                                              | 2 horas        |
| **1.6** | **Prueba de Humo (Listar Archivos)**      | Escribir un método simple en el repositorio que consulte el endpoint `files.list` de Drive. Imprimir en el Logcat (consola) los nombres y IDs de los primeros 10-20 archivos encontrados para verificar que el token y la conexión funcionan.                 | 1.5 horas      |

---

## Sprint 2: Puentes Locales (Storage Access Framework)

**Objetivo:** La aplicación permite al usuario seleccionar una carpeta del dispositivo mediante la interfaz nativa del sistema, retiene los permisos de escritura sobre esa carpeta de forma persistente y es capaz de crear un archivo `.md` real dentro de ella.

| **ID**  | **Tarea**                                        | **Descripción Técnica**                                                                                                                                                                                                                    | **Estimación** |
| ------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------- |
| **2.1** | **Selector de Directorio Local (SAF Intent)**    | Implementar un contrato `ActivityResultContracts.OpenDocumentTree` en Compose para invocar el selector de carpetas nativo de Android y capturar el `Uri` seleccionado por el usuario.                                                      | 1.5 horas      |
| **2.2** | **Persistencia de Permisos y Metadatos**         | Configurar Room o DataStore para guardar el `Uri` de la carpeta seleccionada en texto plano y, vitalmente, invocar `takePersistableUriPermission` para que la app no pierda el acceso si el dispositivo se reinicia.                       | 2.0 horas      |
| **2.3** | **Wrapper de Almacenamiento Local (Data Layer)** | Crear el `LocalFileSystemRepository` en la capa de datos. Utilizar `DocumentFile.fromTreeUri` y `ContentResolver` para abstraer la complejidad de SAF, exponiendo métodos limpios al dominio como `createFile()`, `folderExists()`.        | 3.0 horas      |
| **2.4** | **UI de Configuración (CDD Puro)**               | Construir la pantalla de ajustes (`SettingsScreen`) ensamblando componentes puramente visuales y aislados (ej. `FolderSelectionCard`, `PathDisplayLabel`). Todo manejado mediante _Unidirectional Data Flow_ desde el ViewModel.           | 2.5 horas      |
| **2.5** | **Prueba de Integración: Escritura Física**      | Crear un Caso de Uso temporal que tome una cadena de texto (ej. `# Hola Obsidian`), utilice el `LocalFileSystemRepository` y genere un archivo real `test_sincronizacion.md` en el directorio seleccionado para validar el flujo completo. | 1.5 horas      |

**Total estimado Sprint 2:** ~10.5 horas.

Este bloque deja todo preparado para que, en el Sprint 3, la app simplemente le entregue los bytes descargados de Google Drive a este sistema de archivos local ya validado.

---

## Sprint 3: Clonación Inicial (Descarga Completa)

**Objetivo:** La aplicación es capaz de escanear la carpeta raíz seleccionada en Google Drive, recrear su árbol de subcarpetas en el dispositivo móvil y descargar todos los archivos Markdown de forma secuencial, reportando el progreso al usuario.

| **ID**  | **Tarea**                                        | **Descripción Técnica**                                                                                                                                                                           | **Estimación** |
| ------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| **3.1** | **Exploración Jerárquica de Drive (Data Layer)** | Implementar consultas paginadas (`q = "'ID_CARPETA' in parents"`) en la API de Drive para obtener recursivamente la lista completa de archivos y subcarpetas del Vault.                           | 3.0 horas      |
| **3.2** | **Motor de Descarga en Streaming (I/O)**         | Conectar el cliente de Drive con el `LocalFileSystemRepository` para descargar los archivos. Utilizar un `InputStream` de red conectado a un `OutputStream` local para no saturar la memoria RAM. | 2.5 horas      |
| **3.3** | **Persistencia del Estado Base (Room)**          | Configurar los DAOs y entidades para registrar cada archivo descargado exitosamente en Room (creando la base de datos `synced_files`) y solicitar el `StartPageToken` inicial de Drive.           | 2.5 horas      |
| **3.4** | **Orquestador de Clonación (Domain Use Case)**   | Construir el caso de uso central que coordine la lista, la creación de carpetas, la descarga y la base de datos. Exponer un `Flow<SyncProgress>` para reportar el avance (ej. "50/200 archivos"). | 3.5 horas      |
| **3.5** | **Dashboard UI (Pantalla Principal)**            | Construir la pantalla principal en Compose bajo CDD. Incluir un botón gigante de "Sincronizar", una barra de progreso lineal y un registro de la última ejecución.                                | 2.5 horas      |

**Total estimado Sprint 3:** ~14.0 horas.

**Nota Técnica Estratégica:** En la Tarea 3.3, aunque estamos haciendo una "clonación completa" (descargando todo), es vital que pidamos el `StartPageToken` de la API de Drive _justo antes_ de empezar a descargar. Esto garantizará que, en el Sprint 4 (Sincronización Delta), sepamos exactamente a partir de qué momento debemos empezar a buscar cambios.

---

## Sprint 4: Sincronización Delta (Eficiencia y Optimización)

**Objetivo:** Consumir el `StartPageToken` para consultar únicamente los cambios recientes en Google Drive, actualizando la base de datos local y el almacenamiento físico (SAF) de forma selectiva, garantizando la limpieza estricta de archivos obsoletos.

| **ID**  | **Tarea**                            | **Descripción Técnica**                                                                                                                              | **Estimación** |
| ------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| **4.1** | **Consulta de Cambios (Drive API)**  | Implementar el endpoint `changes.list` en el repositorio de Drive para obtener la lista diferencial de modificaciones usando el token guardado.      | 2.5 horas      |
| **4.2** | **Lógica de Eliminación y Limpieza** | Extender el `LocalFileSystemRepository` para procesar banderas de eliminación (`trashed = true`) y borrar físicamente archivos y carpetas del móvil. | 2.0 horas      |
| **4.3** | **Orquestador Delta (Domain)**       | Crear el caso de uso `ExecuteDeltaSyncUseCase` que evalúe la lista de cambios, sobrescriba notas modificadas y actualice el token de paginación.     | 3.5 horas      |
| **4.4** | **Actualización de UI (CDD Puro)**   | Integrar los nuevos estados del motor Delta en el Dashboard existente, mostrando notificaciones específicas de los archivos modificados.             | 2.0 horas      |

---

## Sprint 5: Automatización y Pulido (WorkManager)

**Objetivo:** Lograr que la sincronización Delta se ejecute de forma autónoma e invisible en segundo plano, respetando los recursos del dispositivo y puliendo la experiencia final del usuario.

| **ID**  | **Tarea**                           | **Descripción Técnica**                                                                                                                                                    | **Estimación** |
| ------- | ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| **5.1** | **Worker de Sincronización**        | Implementar `CoroutineWorker` de WorkManager. Inyectar `ExecuteDeltaSyncUseCase` para ejecutar la sincronización Delta sin necesidad de abrir la aplicación.               | 2.5 horas      |
| **5.2** | **Restricciones y Planificación**   | Configurar `Constraints` (ej. `NetworkType.UNMETERED` para solo Wi-Fi, `requiresBatteryNotLow`) y encolar el trabajo con `PeriodicWorkRequestBuilder`.                     | 1.5 horas      |
| **5.3** | **UI de Preferencias (Automático)** | Añadir controles en la pantalla de Configuración (`SettingsScreen`) para activar/desactivar la sincronización en segundo plano y definir la frecuencia (ej. cada 4 horas). | 2.0 horas      |
| **5.4** | **Sistema de Notificaciones**       | Integrar notificaciones locales para informar sobre eventos clave: advertencias si falló la autenticación, o un reporte silencioso si hubo cambios masivos.                | 2.5 horas      |
| **5.5** | **QA y Manejo de Casos Extremos**   | Pulido final: gestionar la renovación automática del token OAuth, capturar la revocación de permisos SAF y asegurar la resiliencia ante el modo Doze de Android.           | 3.0 horas      |

**Total estimado Sprint 5:** ~11.5 horas.