---
aliases:
  - "Informe Integral de Investigación: Arquitectura Backend Moderna y Evolutiva con Java 21"
  - Spring Boot 3.x y Spring AI
sticker: lucide//coffee
banner: assets/ether-bg.jpeg
---
# **Módulo 0: Introducción a la Programación Moderna y la Evolución de la JVM**

La base de cualquier sistema backend robusto reside en una comprensión profunda de su entorno de ejecución. Java ha evolucionado de ser un lenguaje puramente orientado a objetos a un ecosistema multiparadigma que equilibra la legibilidad, el rendimiento y la seguridad de tipos.

### **Fundamentos Computacionales y la Máquina Virtual**

Un lenguaje de programación, en su definición formal, actúa como un sistema de notación para escribir algoritmos informáticos. Sin embargo, en el contexto de Java, esta definición se expande mediante la **Java Virtual Machine (JVM)**. La JVM no es simplemente un intérprete; es una máquina de computación abstracta que proporciona aislamiento del hardware y gestión automática de memoria.

La arquitectura moderna de la JVM ha evolucionado significativamente. La gestión de memoria, históricamente un punto de fricción, ha visto mejoras masivas con recolectores de basura generacionales y de baja latencia como ZGC y Shenandoah, disponibles en las distribuciones modernas del JDK.1 La premisa "Write Once, Run Anywhere" se mantiene, pero ahora con un enfoque en la optimización dinámica (JIT Compilation) que permite a las aplicaciones de larga duración superar en rendimiento a binarios compilados estáticamente en ciertos escenarios de carga.

### **Sintaxis Moderna: Expresividad y Reducción de Ruido**

La evolución de Java hacia la versión 21 ha estado marcada por la reducción del "boilerplate" (código repetitivo) sin sacrificar la seguridad estática.

#### **Variables e Inferencia de Tipos**

El sistema de tipos de Java ha adoptado la inferencia de tipos local mediante la palabra clave var. Esto no convierte a Java en un lenguaje de tipado dinámico; el tipo se infiere y fija en tiempo de compilación.

- **Impacto en la Legibilidad:** Permite que el desarrollador se centre en el _nombre_ de la variable (la intención) más que en el _tipo_ (la implementación mecanística).
- **Restricciones:** Solo aplicable a variables locales con inicializadores. No se puede usar en campos de clase o parámetros de métodos para mantener contratos de API explícitos.1

#### **Estructuras de Control Evolucionadas**

Las estructuras condicionales y cíclicas han madurado para prevenir errores comunes y mejorar la expresividad.

Switch Expressions:  
A diferencia del switch tradicional, las expresiones switch modernas eliminan la necesidad de la sentencia break, previniendo el error de "fall-through" accidental. Además, al ser expresiones, retornan un valor, facilitando la inmutabilidad al permitir la asignación directa a variables final o registros.

```Java

// Ejemplo de Switch Expression exhaustivo con sintaxis de flecha  
var tipoDia = switch (dia) {  
 case LUNES, VIERNES -> "Inicio/Fin de semana laboral";  
 case SABADO, DOMINGO -> "Fin de semana";  
 default -> throw new IllegalArgumentException("Día inválido: " + dia);  
};
```

Esta estructura no solo es más compacta, sino que el compilador verifica la exhaustividad, especialmente útil cuando se trabaja con Enums o Sealed Classes.1

#### **Text Blocks**

La manipulación de cadenas multilínea (JSON, SQL, HTML) en Java pre-15 era propensa a errores y difícil de leer debido a la necesidad de caracteres de escape (n, "). Los **Text Blocks** introducen un literal de cadena bidimensional delimitado por triples comillas """.

**Implicaciones:**

- **Seguridad:** Facilita la incrustación de JSON o XML para pruebas y payloads de API sin errores de formato.
- **Incidental Whitespace:** El compilador es inteligente al eliminar la indentación incidental, preservando el formato relativo del texto.1

```Java

// Ejemplo de Text Block para un JSON de Prompt de IA  
String promptJson = """  
 {  
 "role": "user",  
 "content": "Explica la teoría de la relatividad"  
 }  
 """;
```

---

# **Módulo 1: Fundamentos de Programación Orientada a Objetos (POO) en la Era Moderna**

Aunque Java incorpora características funcionales, la POO sigue siendo el paradigma dominante para la estructuración de sistemas complejos. La comprensión matizada de sus pilares es crucial para evitar diseños anémicos o excesivamente acoplados.

### **Clases, Objetos y el Ciclo de Vida**

Una clase actúa como el plano arquitectónico (blueprint), mientras que los objetos son las instancias concretas que ocupan memoria en el heap. La distinción moderna radica en cómo modelamos estos objetos: ¿son portadores de datos puros o entidades con comportamiento?

### **Los Cuatro Pilares: Revisitados**

1. **Encapsulamiento:** Más allá de private y public, el encapsulamiento moderno incluye el concepto de módulos (Java 9 JPMS) y la restricción de herencia mediante sealed classes. El objetivo es minimizar la superficie de API expuesta y proteger las invariantes del estado interno.1
2. **Herencia:** El mecanismo extends permite la reutilización, pero se prefiere la composición sobre la herencia en diseños modernos para evitar la fragilidad de la clase base.
3. **Polimorfismo:** La capacidad de intercambiar implementaciones en tiempo de ejecución es la base de la Inyección de Dependencias en Spring.
4. **Abstracción:** El uso de interfaces y clases abstractas para definir contratos permite desacoplar la definición del servicio de su implementación.1

### **Interfaces vs. Clases Abstractas: Un Análisis Comparativo**

La línea entre interfaces y clases abstractas se ha difuminado desde Java 8, pero sus roles arquitectónicos permanecen distintos.

| Característica    | Clase Abstracta                                                    | Interfaz                                                                   |
| :---------------- | :----------------------------------------------------------------- | :------------------------------------------------------------------------- |
| **Herencia**      | Herencia simple (extends). Define "qué es" el objeto.              | Implementación múltiple (implements). Define "qué puede hacer".            |
| **Estado**        | Puede mantener estado mutable (campos no estáticos).               | Sin estado de instancia (solo constantes static final).                    |
| **Constructores** | Posee constructores para inicializar estado base.                  | Sin constructores.                                                         |
| **Métodos**       | Abstractos y concretos con cualquier visibilidad.                  | Abstractos, default, static y private (desde Java 9).                      |
| **Uso Ideal**     | Compartir código y estado entre clases estrechamente relacionadas. | Definir contratos de comportamiento (Capabilities) entre clases disjuntas. |

**Insight:** Los métodos default en interfaces permiten la evolución de APIs sin romper la compatibilidad binaria con implementaciones existentes, un factor crítico en el diseño de librerías.1

### **Asociaciones y Modelado UML en Código**

La traducción precisa de relaciones UML a Java es vital para la integridad referencial y el ciclo de vida de los objetos.1

1. **Asociación:** Relación "usa un". El objeto A tiene una referencia al objeto B, pero sus ciclos de vida son independientes.  
   ```Java  
   public class Profesor { private Curso curso; } // Referencia débil
   ```

2. **Composición:** Relación "parte de" fuerte. Si el padre muere, el hijo también.  
   ```Java  
   public class Casa {  
    private final List<Habitacion> habitaciones = new ArrayList<>();  
    // Las habitaciones no existen sin la casa  
   }
   ```

3. **Agregación:** Relación "parte de" débil. El hijo puede sobrevivir al padre.  
  ``` Java  
   public class Departamento {  
    private List<Profesor> profesores; // Profesores pueden cambiar de depto  
   }
  ```

### **Pruebas Unitarias con JUnit 5: El Patrón AAA**

La calidad del software moderno depende de pruebas automatizadas. JUnit 5 (Jupiter) es el estándar actual. El patrón **AAA (Arrange, Act, Assert)** proporciona una estructura clara:

- **Arrange:** Preparar el entorno y los mocks.
- **Act:** Ejecutar el método bajo prueba.
- **Assert:** Verificar los resultados y efectos colaterales.1

```Java

@Test  
void testCalculadoraSuma() {  
 // Arrange  
 Calculadora calc = new Calculadora();  
 // Act  
 int resultado = calc.sumar(2, 3);  
 // Assert  
 assertEquals(5, resultado, "La suma debe ser 5");  
}
```

---

# **Módulo 2: Ecosistema de Java, Gestión de Dependencias y Lombok**

El desarrollo profesional no ocurre en el vacío; depende de un ecosistema de herramientas de construcción y librerías de productividad.

### **Maven: Ingeniería de Construcción y Ciclo de Vida**

Maven gestiona la complejidad de las dependencias transitivas y estandariza el ciclo de vida del proyecto.

- **Gestión de Dependencias:** El archivo pom.xml declara dependencias directas. Maven resuelve el grafo de dependencias, descargando artefactos de Maven Central.
- **Ciclo de Vida:** Comandos como mvn clean, mvn compile, mvn test, mvn package, mvn install ejecutan fases secuenciales predefinidas. mvn dependency:tree es esencial para diagnosticar conflictos de versiones ("Jar Hell").1

### **Project Lombok: Reducción de Boilerplate**

Lombok actúa como un procesador de anotaciones en tiempo de compilación, inyectando código (getters, setters, constructores) en el AST (Abstract Syntax Tree).

**Anotaciones Clave:**

- `@Data`: Genera `getters`, `setters`, `toString`, `equals`, `hashCode`. Útil para entidades mutables.
- `@Builder`: Implementa el patrón `Builder` para la creación fluida de objetos complejos.
- `@Slf4j`: Inyecta un `logger` estático (`SLF4J`), eliminando la declaración manual del logger.1

**Contradicción Emergente:** Con la llegada de los **Java `Records`**, el uso de `@Data` para `DTOs` inmutables está siendo reemplazado por la sintaxis nativa de `record`, que ofrece inmutabilidad garantizada por el lenguaje sin dependencias externas.5

---

# **Módulo 3: Colecciones, Genéricos y Programación Funcional**

La manipulación eficiente de datos en memoria es crítica para el rendimiento del backend.

### **Colecciones: Estructuras de Datos**

La elección de la implementación correcta de la interfaz `Collection` impacta la complejidad algorítmica (Big O).

- **`List`:** `ArrayList` (acceso O(1), inserción O(n)) vs `LinkedList` (acceso O(n), inserción O(1) en extremos).
- **`Set`:** `HashSet` (búsqueda O(1)) garantiza unicidad. `TreeSet` mantiene orden natural (O(log n)).
- **`Map`:** `HashMap` es el estándar para pares clave-valor. Java 9 introdujo factorías inmutables (`List.of`, `Map.of`) que lanzan `UnsupportedOperationException` si se intentan modificar, promoviendo la seguridad.1

### **Genéricos: Seguridad de Tipos y PECS**

Los genéricos permiten la abstracción sobre tipos.

- **`Bounded Type Parameters`:** `<T extends Animal>` restringe `T` a subtipos de Animal.
- **`Wildcards` y `PECS` (Producer `Extends`, `Consumer` Super):**
  - Si solo _lees_ de una estructura (Productor), usa `<? extends T>`.
  - Si solo _escribes_ en una estructura (Consumidor), usa `<? super T>`.
  - Esto maximiza la flexibilidad de las `APIs` de colecciones.1
### **Programación Funcional y `Streams` API**

Desde Java 8, el paradigma funcional permite un procesamiento de datos declarativo y paralelizable.

- **Interfaces Funcionales:** `Predicate<T>` (booleano), `Function<T,R>` (transformación), `Consumer<T>` (efecto secundario), `Supplier<T>` (generación).
- **`Streams`:** Pipeline de operaciones (`filter`, `map`, reduce).
  - _`Lazy Evaluation`:_ Las operaciones intermedias no se ejecutan hasta que se invoca una operación terminal (ej. `collect`, `forEach`).
  - _Inmutabilidad:_ Los `streams` no modifican la fuente original.1

```Java

// Ejemplo de Pipeline Funcional  
List<String> nombresMayusculas = usuarios.stream()  
 .filter(u -> u.getEdad() > 18) // Predicate  
 .map(Usuario::getNombre) // Function (Reference Method)  
 .map(String::toUpperCase) // Transformación  
 .collect(Collectors.toList()); // Terminal

```
---

# **Módulo 4: Java 21 y Características Modernas Avanzadas**

Java 21 representa un hito LTS que consolida características transformadoras para la concurrencia y la expresividad.

### **Virtual Threads (Project Loom): La Revolución de la Escalabilidad**

Tradicionalmente, Java utilizaba un modelo "uno a uno" entre hilos de Java (java.lang.Thread) e hilos del sistema operativo (Platform Threads). Esto limitaba la escalabilidad en aplicaciones I/O bound (como servidores web) debido al alto costo de memoria y contexto de los hilos del SO.

**Hilos Virtuales:** Son hilos ligeros gestionados por la JVM, no por el SO. Mapean M hilos virtuales a N hilos de plataforma (Carrier Threads). Cuando un hilo virtual realiza una operación bloqueante (I/O), la JVM lo "desmonta" del hilo portador, permitiendo que este último ejecute otro hilo virtual.

**Implicación Arquitectónica:**

- Permite el estilo de programación "Thread-per-request" a escala de millones de hilos.
- Elimina la necesidad de código reactivo complejo (WebFlux) para la mayoría de los casos de uso de alta concurrencia.
- **Limitación - Pinning:** Bloques synchronized o métodos nativos pueden "clavar" (pin) el hilo virtual al portador, impidiendo el desmontaje. Se recomienda usar ReentrantLock en su lugar.1

### **Concurrencia Estructurada (StructuredTaskScope)**

Actualmente en _preview_, esta API trata múltiples tareas concurrentes relacionadas como una sola unidad de trabajo, mejorando el manejo de errores y la cancelación. Evita los "hilos huérfanos" y simplifica la coordinación.

```Java

try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {  
 Supplier<String> user = scope.fork(() -> findUser(id));  
 Supplier<Order> order = scope.fork(() -> fetchOrder(id));

    scope.join().throwIfFailed(); // Espera a ambos, falla si uno falla

    return new Response(user.get(), order.get());

}
```

Esto reemplaza la complejidad de CompletableFuture para la coordinación de tareas paralelas.4

### **Records y Pattern Matching**

Los **Records** (Java 14+) son clases inmutables transparentes. Java 21 mejora su uso con **Record Patterns**, permitiendo la desestructuración directa en instanceof y switch.

```Java

// Pattern Matching con Records  
if (obj instanceof Point(int x, int y)) {  
 System.out.println("X: " + x + ", Y: " + y);  
}
```

Esto reduce la necesidad de casting manual y accesores, haciendo el código más declarativo y seguro.1

### **Sequenced Collections**

Java 21 introduce interfaces unificadas (SequencedCollection, SequencedMap) que garantizan un orden de encuentro. Métodos como addFirst, addLast, getFirst, getLast y reversed ahora son estándar en List, Deque, y LinkedHashSet, eliminando inconsistencias históricas en las APIs.1

---

# **Módulo 5: APIs sin Spring (Fundamentos Web en Java)**

Es esencial comprender las capacidades nativas de Java para HTTP antes de usar abstracciones de alto nivel.

### **Cliente HTTP Nativo (java.net.http.HttpClient)**

Introducido en Java 11, reemplaza a la antigua HttpURLConnection. Soporta HTTP/1.1 y HTTP/2, WebSocket, y ofrece APIs sincrónicas y asincrónicas.

**Ejemplo de Petición Asíncrona (GET):**

```Java

HttpClient client = HttpClient.newHttpClient();  
HttpRequest request = HttpRequest.newBuilder()  
 .uri(URI.create("https://api.ejemplo.com/data"))  
 .GET()  
 .build();

// Retorna CompletableFuture  
client.sendAsync(request, BodyHandlers.ofString())  
 .thenApply(HttpResponse::body)  
 .thenAccept(System.out::println)  
 .join(); // Esperar finalización (solo para demo)
```

Este cliente es la base moderna para la comunicación entre microservicios cuando no se utilizan clientes declarativos como Feign o RestClient.12

### **Servidor HTTP Simple (com.sun.net.httpserver)**

Java incluye un servidor HTTP ligero ideal para pruebas, prototipos o microservicios mínimos sin dependencias.

```Java

HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);  
server.createContext("/api/hello", exchange -> {  
 String resp = "Hola Mundo Java";  
 exchange.sendResponseHeaders(200, resp.getBytes().length);  
 try (OutputStream os = exchange.getResponseBody()) {  
 os.write(resp.getBytes());  
 }  
});  
server.start();
```

Aunque funcional, carece de características avanzadas como enrutamiento complejo o manejo automático de JSON que proveen frameworks como Spring Boot.15

---

# **Módulo 6: Spring Boot 3.x y Arquitectura REST**

Spring Boot 3 se basa en Spring Framework 6, requiriendo Java 17+. Introduce cambios significativos en la observabilidad, compilación nativa (GraalVM) y manejo de errores.

### **Estructura del Proyecto: Layer vs. Feature**

La organización del código afecta la mantenibilidad a largo plazo.

1. **Layer-based (Por Capas):** Agrupa por tipo técnico (controllers, services, repositories). Fácil de entender al inicio, pero escala mal; las características están dispersas.
2. **Feature-based (Por Funcionalidad):** Agrupa por dominio (usuario, pedido, pago). Cada paquete contiene su controlador, servicio y repositorio. Favorece la modularidad, el encapsulamiento (usando visibilidad de paquete) y se alinea con **Spring Modulith** para arquitecturas evolutivas.17

### **ProblemDetail: Estandarización de Errores (RFC 7807)**

Spring Boot 3 adopta el estándar **RFC 7807** para respuestas de error. En lugar de crear DTOs de error personalizados, se utiliza la clase ProblemDetail.

**Configuración Global con @RestControllerAdvice:**

```Java

@RestControllerAdvice  
public class GlobalExceptionHandler {  
 @ExceptionHandler(RecursoNoEncontradoException.class)  
 public ProblemDetail handleNotFound(RecursoNoEncontradoException ex) {  
 ProblemDetail pd = ProblemDetail.forStatusAndDetail(  
 HttpStatus.NOT_FOUND, ex.getMessage());  
 pd.setTitle("Recurso No Encontrado");  
 pd.setType(URI.create("https://api.miap.com/errors/not-found"));  
 pd.setProperty("timestamp", Instant.now()); // Metadatos extra  
 return pd;  
 }  
}
```

Esto asegura que todos los clientes (Frontend, otros microservicios) reciban una estructura de error predecible y estándar.2

### **DTOs Modernos con Records y Validación**

Los Java Records son ideales para DTOs (Data Transfer Objects) debido a su inmutabilidad y semántica de datos. Se integran perfectamente con **Jakarta Validation** (@Valid).

```Java

public record UsuarioRegistroDto(  
 @NotBlank(message = "El nombre es obligatorio") String nombre,  
 @Email(message = "Email inválido") String email,  
 @Size(min = 8) String password  
) {}
```

En el controlador, @Valid @RequestBody UsuarioRegistroDto dto activará la validación automática antes de entrar al método, lanzando MethodArgumentNotValidException si falla, la cual puede ser manejada globalmente para retornar un ProblemDetail.5

### **ModelMapper y Records**

Aunque librerías como ModelMapper existen para transformar Entidad <-> DTO, tienen limitaciones con Records debido a la falta de setters. Se requiere configuración específica o el uso de patrones de construcción. La tendencia moderna favorece mappers en tiempo de compilación como **MapStruct** o métodos de mapeo manuales dentro de los Records para mayor rendimiento y claridad.21

---

# **Módulo 7: Persistencia de Datos con Spring Data JPA**

### **Configuración Docker Compose**

Spring Boot 3.1 introdujo el soporte nativo para **Docker Compose** en desarrollo. Al incluir spring-boot-docker-compose, la aplicación detecta el compose.yaml, levanta los contenedores (ej. PostgreSQL) al inicio y apaga al finalizar.

**Ventaja Crítica:** Inyecta automáticamente las propiedades de conexión (spring.datasource.url, etc.) en el contexto de Spring, eliminando la necesidad de hardcodear credenciales en application.properties para entornos locales.24

### **Proyecciones y Rendimiento**

Para evitar el problema de "fetching" excesivo (traer columnas innecesarias), Spring Data JPA soporta **Proyecciones** basadas en Interfaces o Records.

```Java

// Record Proyección: Solo trae lo necesario  
public record InfoBasicaUsuario(String nombre, String email) {}

public interface UsuarioRepository extends JpaRepository<Usuario, Long> {  
 // Spring Data optimiza la query SELECT nombre, email FROM...  
 List<InfoBasicaUsuario> findByActivoTrue();  
}
```

Esto mejora drásticamente el rendimiento en consultas de lectura masiva.27

### **Stored Procedures con @Procedure**

Para lógica compleja en base de datos, JPA permite mapear procedimientos almacenados directamente a métodos de repositorio, manejando parámetros IN y OUT.

```Java

@Procedure(procedureName = "calcular_impuestos")  
BigDecimal calcularImpuestos(Long usuarioId);
```

Esto encapsula la llamada nativa y mantiene la abstracción del repositorio.29

### **Inyección de Dependencias: Constructor vs. Field**

La inyección por constructor es el estándar de facto en Spring Boot 3.

- **`Inmutabilidad`:** Permite campos final.
- **`Testing`:** Facilita la instanciación manual en `tests` unitarios sin necesidad de levantar el contexto de Spring.
- `Claridad`: Hace explícitas las dependencias obligatorias.  
  La inyección por campo (@Autowired en atributos) se considera mala práctica excepto en tests.30

---

# **Módulo 8: Seguridad con Spring Security 6**

Spring Security 6 elimina WebSecurityConfigurerAdapter y adopta una configuración basada en componentes (SecurityFilterChain) usando una DSL Lambda funcional.

### **Autenticación Stateless con JWT**

En arquitecturas REST modernas, se prefiere la autenticación sin estado (Stateless) usando JSON Web Tokens (JWT).

**Arquitectura de Implementación:**

1. **Filtro JWT (OncePerRequestFilter):** Intercepta cada petición, extrae el token del header Authorization, lo valida (firma, expiración) y extrae el usuario.
2. **Contexto de Seguridad:** Si el token es válido, se crea un objeto Authentication y se inyecta en el SecurityContextHolder. Esto autentica al usuario para el resto de la ejecución de la petición.
3. **Configuración:** Se define SessionCreationPolicy.STATELESS para evitar que Spring cree cookies de sesión JSESSIONID.

**Ejemplo de Configuración (Lambda DSL):**

```Java

@Bean  
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {  
 http  
 .csrf(AbstractHttpConfigurer::disable)  
 .authorizeHttpRequests(auth -> auth  
 .requestMatchers("/auth/**").permitAll()  
 .anyRequest().authenticated()  
 )  
 .sessionManagement(sess -> sess.sessionCreationPolicy(SessionCreationPolicy.STATELESS))  
 .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);  
 return http.build();  
}
```

Este enfoque desacopla el servidor del estado del cliente, facilitando el escalado horizontal.32

### **Perfiles de Configuración**

Spring Profiles (dev, prod) permiten segregar configuraciones de seguridad. Por ejemplo, en dev se puede usar una base de datos H2 y logs detallados, mientras que en prod se usa PostgreSQL y seguridad estricta. Se activan vía spring.profiles.active.35

---

# **Módulo 9: Pruebas Automatizadas: La Pirámide Moderna**

### **Unit Testing: JUnit 5 y Mockito**

Pruebas aisladas de la lógica de negocio. Se usa @ExtendWith(MockitoExtension.class) para inyectar mocks en servicios. Los Records y la inyección por constructor facilitan enormemente estas pruebas al no requerir contenedores Spring.3

### **Integration Testing: Testcontainers**

Para pruebas que requieren infraestructura real (BD, Broker de Mensajes), **Testcontainers** es el estándar. Levanta contenedores Docker efímeros durante la ejecución de los tests.

```Java

@Testcontainers
class UsuarioRepoTest {
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        //... credenciales dinámicas
    }
}
```

Esto garantiza que las pruebas de repositorio se ejecuten contra una base de datos PostgreSQL real, idéntica a producción, evitando falsos positivos de H2.38

### **Slice Testing: @WebMvcTest**

Pruebas enfocadas solo en la capa web (Controladores). Utilizan **MockMvc** para simular peticiones HTTP sin levantar el servidor completo. Spring Boot 3.4 introduce MockMvcTester con una API fluida basada en AssertJ para aserciones más legibles.40

---

# **Módulo 10: Integración Frontend (Consumo de API)**

### **React y Fetch API / Axios**

React utiliza hooks (useEffect) para disparar efectos secundarios como llamadas a API.

- **Fetch API:** Nativo del navegador. Requiere dos await (uno para la red, otro para parsear JSON).
- Axios: Librería popular que simplifica el manejo de errores, interceptores y transformación automática de JSON.  
  La configuración de CORS (@CrossOrigin) en el backend es obligatoria para permitir peticiones desde dominios distintos (ej. localhost:3000 a localhost:8080).42

### **Angular y HttpClient**

Angular ofrece un HttpClient robusto basado en **Observables (RxJS)**. Esto permite características avanzadas como cancelación de peticiones, reintentos automáticos y debouncing de manera declarativa, integrándose profundamente con el ciclo de detección de cambios de Angular.44

### **Next.js App Router**

Next.js 13+ introduce _Server Components_. Estos componentes se renderizan en el servidor (Node.js) y pueden hacer fetch directamente a la API de Spring Boot dentro de la red del servidor, mejorando la seguridad (no exponen tokens al cliente) y el SEO.

```ts
// Server Component en Next.js
async function ListaUsuarios() {
  const res = await fetch("http://api-springboot:8080/usuarios");
  const usuarios = await res.json();
  return (
    <ul>
      {usuarios.map((u) => (
        <li key={u.id}>{u.nombre}</li>
      ))}
    </ul>
  );
}
```

Esto cambia el paradigma de "`Client-side fetching`" a "`Server-side data access`"[46]

---

# **Módulo 11: Concurrencia Avanzada: `@Async` y Virtual Threads**

### **Modelo Asíncrono (@Async)**

La anotación `@Async` en Spring permite ejecutar métodos en un hilo separado. Tradicionalmente, esto usaba un `ThreadPoolTaskExecutor` limitado.

### **Impacto de los Hilos Virtuales**

Con Java 21 y Spring Boot 3.2+, al habilitar spring.threads.virtual.enabled=true, el ejecutor asíncrono por defecto (SimpleAsyncTaskExecutor) comienza a usar hilos virtuales. Esto permite lanzar miles de tareas asíncronas concurrentes (ej. envío de emails, llamadas a APIs externas) sin saturar el pool de hilos del sistema, haciendo que la asincronía sea casi "gratuita" en términos de recursos.48

---

# **Módulo 12: Spring AI y la Nueva Frontera del Desarrollo**

Spring AI es la adición más transformadora, proporcionando una abstracción unificada para integrar Modelos de Lenguaje Grande (LLMs) y bases de datos vectoriales.

### **ChatClient y Prompt Engineering**

ChatClient ofrece una API fluida para interactuar con modelos (OpenAI, Ollama, Azure). Permite parametrizar prompts ("Prompt Templating") para inyectar datos dinámicos de manera segura.

```Java

String respuesta = chatClient.prompt()  
 .system("Eres un asistente experto en Java.")  
 .user(u -> u.text("Explica el concepto de {concepto}").param("concepto", "Virtual Threads"))  
 .call()  
 .content();
```

Esta abstracción permite cambiar el proveedor de IA (ej. de GPT-4 a Llama 3) solo cambiando la configuración, sin tocar el código.50

### **Salida Estructurada (Structured Output)**

Un desafío de los LLMs es que generan texto no estructurado. Spring AI soluciona esto con Structured Output Converters (ej. BeanOutputConverter).  
El framework inyecta automáticamente instrucciones de formato en el prompt (ej. "Responde en JSON conforme a este esquema...") y luego deserializa la respuesta JSON del modelo a objetos Java (POJOs o Records). Esto permite integrar la IA en flujos de lógica de negocio tipados.53

### **Function Calling (Uso de Herramientas)**

Permite a los LLMs interactuar con el mundo exterior. Se registran métodos Java como @Tool. El modelo, al razonar, puede decidir que necesita ejecutar una herramienta (ej. "Obtener precio de acción"). Spring AI intercepta esta solicitud, ejecuta el código Java y devuelve el resultado al modelo para que genere la respuesta final. Esto es la base de los **Agentes Autónomos**.55

### **RAG (Retrieval Augmented Generation)**

Para superar las alucinaciones y la falta de conocimiento privado, se usa RAG.

1. **Ingesta (ETL):** TikaDocumentReader lee documentos (PDF, Docx), TokenTextSplitter los divide en fragmentos, y un EmbeddingModel los convierte en vectores numéricos.
2. **Almacenamiento:** Los vectores se guardan en una **Vector Database** (Chroma, PGVector, Milvus).58
3. **Recuperación (Advisors):** Al consultar, QuestionAnswerAdvisor intercepta el prompt, busca documentos semánticamente similares en la base vectorial, y los inyecta en el contexto del sistema antes de llamar al LLM. Esto permite "chatear con tus datos".60

### **Multimodalidad**

Spring AI soporta modelos multimodales (GPT-4o, Gemini Vision). Permite enviar texto e imágenes (como recursos Resource) simultáneamente para análisis visual (ej. "Describe qué ves en esta imagen"). Esto abre casos de uso como procesamiento de facturas o análisis de diagramas.63

### **Structured Logging (Spring Boot 3.4)**

Spring Boot 3.4 introduce soporte nativo para **Logging Estructurado** (JSON), compatible con formatos como ECS (Elastic Common Schema) y Logstash. Esto es vital para la observabilidad en sistemas distribuidos y aplicaciones de IA, permitiendo la ingestión directa de logs en plataformas como Kibana o Grafana sin parsers complejos.65

---

# **Conclusión**

La convergencia de **Java 21**, **Spring Boot 3.x** y **Spring AI** define un nuevo estándar para el desarrollo backend. La adopción de **Virtual Threads** resuelve el problema histórico de la escalabilidad I/O sin la complejidad reactiva. Los **Records** y la **Concurrencia Estructurada** modernizan la sintaxis y la gestión de tareas. Finalmente, **Spring AI** democratiza el acceso a la inteligencia artificial generativa, permitiendo a los desarrolladores Java construir sistemas cognitivos complejos (RAG, Agentes) utilizando los patrones de diseño y la seguridad de tipos que han hecho de Java el pilar de la ingeniería de software empresarial. La arquitectura descrita en este informe no es solo una actualización tecnológica, sino una redefinición de las capacidades del backend moderno.

#### **Fuentes citadas**

1. f898cfdc-9874-481a-8114-34cf300468ee_Java_21__Spring_Boot_Backend_Developer.pdf
2. Problem Detail in Spring Boot REST API with Examples | Learn Code With Durgesh, acceso: enero 4, 2026, [https://learncodewithdurgesh.com/tutorials/spring-boot-tutorials/problem-detail-in-spring-boot-rest-api-with-examples](https://learncodewithdurgesh.com/tutorials/spring-boot-tutorials/problem-detail-in-spring-boot-rest-api-with-examples)
3. Unit Testing Rest Services with Spring Boot and JUnit - in28minutes, acceso: enero 4, 2026, [https://www.springboottutorial.com/unit-testing-for-spring-boot-rest-services](https://www.springboottutorial.com/unit-testing-for-spring-boot-rest-services)
4. Unit Testing in Spring Boot Project using Mockito and Junit - GeeksforGeeks, acceso: enero 4, 2026, [https://www.geeksforgeeks.org/advance-java/unit-testing-in-spring-boot-project-using-mockito-and-junit/](https://www.geeksforgeeks.org/advance-java/unit-testing-in-spring-boot-project-using-mockito-and-junit/)
5. Using Java Records with Spring Boot DTOs | Medium, acceso: enero 4, 2026, [https://medium.com/@AlexanderObregon/using-java-records-with-spring-boot-dtos-619ff1484495](https://medium.com/@AlexanderObregon/using-java-records-with-spring-boot-dtos-619ff1484495)
6. Spring Boot 3 + Record-Based DTOs: Cleaner APIs with Better Type Safety, acceso: enero 4, 2026, [https://www.javacodegeeks.com/2025/05/spring-boot-3-record-based-dtos-cleaner-apis-with-better-type-safety.html](https://www.javacodegeeks.com/2025/05/spring-boot-3-record-based-dtos-cleaner-apis-with-better-type-safety.html)
7. Virtual Threads in Springboot 3.2 | by Navod Dilshan | Nerd For Tech | Medium, acceso: enero 4, 2026, [https://medium.com/nerd-for-tech/virtual-threads-in-springboot-3-2-9a7250429809](https://medium.com/nerd-for-tech/virtual-threads-in-springboot-3-2-9a7250429809)
8. What are Virtual Threads? (And How to Use Them in Spring Boot) - Soham Kamani, acceso: enero 4, 2026, [https://www.sohamkamani.com/java/virtual-threads-spring-boot/](https://www.sohamkamani.com/java/virtual-threads-spring-boot/)
9. BACKEND. Virtual Threads and the concurrency model in Spring - EDICOM Careers, acceso: enero 4, 2026, [https://careers.edicomgroup.com/techblog/backend-virtual-threads-and-the-concurrency-model-in-spring/](https://careers.edicomgroup.com/techblog/backend-virtual-threads-and-the-concurrency-model-in-spring/)
10. StructuredTaskScope (Java SE 21 & JDK 21) - Oracle Help Center, acceso: enero 4, 2026, [https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/StructuredTaskScope.html](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/StructuredTaskScope.html)
11. Understanding Structured Concurrency in Java (New preview feature in Java 21), acceso: enero 4, 2026, [https://codefarm0.medium.com/understanding-structured-concurrency-in-java-new-preview-feature-in-java-21-0b3f3943eab8](https://codefarm0.medium.com/understanding-structured-concurrency-in-java-new-preview-feature-in-java-21-0b3f3943eab8)
12. Java HTTP Client - Examples and Recipes - OpenJDK, acceso: enero 4, 2026, [https://openjdk.org/groups/net/httpclient/recipes.html](https://openjdk.org/groups/net/httpclient/recipes.html)
13. HttpClient (Java SE 21 & JDK 21) - Oracle Help Center, acceso: enero 4, 2026, [https://docs.oracle.com/en/java/javase/21/docs/api/java.net.http/java/net/http/HttpClient.html](https://docs.oracle.com/en/java/javase/21/docs/api/java.net.http/java/net/http/HttpClient.html)
14. Http Client API in Java: The basics - DEV Community, acceso: enero 4, 2026, [https://dev.to/noelopez/http-client-api-in-java-26e](https://dev.to/noelopez/http-client-api-in-java-26e)
15. com.sun.net.httpserver (Java HTTP Server ) - Oracle Help Center, acceso: enero 4, 2026, [https://docs.oracle.com/javase/8/docs/jre/api/net/httpserver/spec/com/sun/net/httpserver/package-summary.html](https://docs.oracle.com/javase/8/docs/jre/api/net/httpserver/spec/com/sun/net/httpserver/package-summary.html)
16. Lesson 20: Project — Building a Simple RESTful API with Java | by Souren Stepanyan, acceso: enero 4, 2026, [https://programming.am/lesson-20-project-building-a-simple-restful-api-with-java-30102f29f8a8](https://programming.am/lesson-20-project-building-a-simple-restful-api-with-java-30102f29f8a8)
17. Spring Boot Project Structure Best Practices: Layer-Based vs Feature-Based Explained Simply | by Mohamed Rifai, acceso: enero 4, 2026, [https://rifaiio.medium.com/spring-boot-project-structure-best-practices-layer-based-vs-feature-based-explained-simply-4a9002f3cff0](https://rifaiio.medium.com/spring-boot-project-structure-best-practices-layer-based-vs-feature-based-explained-simply-4a9002f3cff0)
18. What's the cleanest way to structure a Spring Boot project as it grows? - Reddit, acceso: enero 4, 2026, [https://www.reddit.com/r/SpringBoot/comments/1p6m74v/whats_the_cleanest_way_to_structure_a_spring_boot/](https://www.reddit.com/r/SpringBoot/comments/1p6m74v/whats_the_cleanest_way_to_structure_a_spring_boot/)
19. Spring Boot 3 Rest: Error Handling - PandaC, acceso: enero 4, 2026, [https://pandac.in/blogs/springrest-errorhandle/](https://pandac.in/blogs/springrest-errorhandle/)
20. Returning Errors Using ProblemDetail in Spring Boot - GeeksforGeeks, acceso: enero 4, 2026, [https://www.geeksforgeeks.org/advance-java/returning-errors-using-problemdetail-in-spring-boot/](https://www.geeksforgeeks.org/advance-java/returning-errors-using-problemdetail-in-spring-boot/)
21. How to Write Clean DTO & Entity Mappers in Java (with Spring Boot) - DEV Community, acceso: enero 4, 2026, [https://dev.to/gianfcop98/how-to-write-clean-dto-entity-mappers-in-java-with-spring-boot-5ac6](https://dev.to/gianfcop98/how-to-write-clean-dto-entity-mappers-in-java-with-spring-boot-5ac6)
22. Expertise in ModelMapper for Seamless Java Object Mapping - Mindbowser, acceso: enero 4, 2026, [https://www.mindbowser.com/modelmapper-expert-java-mapping/](https://www.mindbowser.com/modelmapper-expert-java-mapping/)
23. Utilizing Java Records as DTOs with ModelMapper in Your Applications - YouTube, acceso: enero 4, 2026, [https://www.youtube.com/watch?v=gihjMm0gcMs](https://www.youtube.com/watch?v=gihjMm0gcMs)
24. Docker Compose Spring Boot and Postgres example - GitHub, acceso: enero 4, 2026, [https://github.com/bezkoder/docker-compose-spring-boot-postgres](https://github.com/bezkoder/docker-compose-spring-boot-postgres)
25. Using Docker Compose with Spring Boot and PostgreSQL | by Gozde Saygili Yalcin, acceso: enero 4, 2026, [https://medium.com/@saygiligozde/using-docker-compose-with-spring-boot-and-postgresql-235031106f9f](https://medium.com/@saygiligozde/using-docker-compose-with-spring-boot-and-postgresql-235031106f9f)
26. Running Spring Boot with PostgreSQL in Docker Compose | Baeldung, acceso: enero 4, 2026, [https://www.baeldung.com/spring-boot-postgresql-docker](https://www.baeldung.com/spring-boot-postgresql-docker)
27. Projections :: Spring Data JPA, acceso: enero 4, 2026, [https://docs.spring.io/spring-data/jpa/reference/repositories/projections.html](https://docs.spring.io/spring-data/jpa/reference/repositories/projections.html)
28. Using Java Records with JPA | Baeldung, acceso: enero 4, 2026, [https://www.baeldung.com/spring-jpa-java-records](https://www.baeldung.com/spring-jpa-java-records)
29. Calling Stored Procedures from Spring Data JPA Repositories | Baeldung, acceso: enero 4, 2026, [https://www.baeldung.com/spring-data-jpa-stored-procedures](https://www.baeldung.com/spring-data-jpa-stored-procedures)
30. Why Constructor Injection is Better Than Field Injection | by Suresh - Medium, acceso: enero 4, 2026, [https://medium.com/@CodeWithTech/why-constructor-injection-is-better-than-field-injection-d6f2375b13c8](https://medium.com/@CodeWithTech/why-constructor-injection-is-better-than-field-injection-d6f2375b13c8)
31. Why Is Field Injection Not Recommended in Spring? - GeeksforGeeks, acceso: enero 4, 2026, [https://www.geeksforgeeks.org/advance-java/why-is-field-injection-not-recommended-in-spring/](https://www.geeksforgeeks.org/advance-java/why-is-field-injection-not-recommended-in-spring/)
32. Mastering JWT Authentication in Spring Security 6: A Developer's Guide - Dev Genius, acceso: enero 4, 2026, [https://blog.devgenius.io/mastering-jwt-authentication-in-spring-security-6-a-developers-guide-737c4586c3fb](https://blog.devgenius.io/mastering-jwt-authentication-in-spring-security-6-a-developers-guide-737c4586c3fb)
33. Configuration Migrations :: Spring Security, acceso: enero 4, 2026, [https://docs.spring.io/spring-security/reference/6.5-SNAPSHOT/migration-7/configuration.html](https://docs.spring.io/spring-security/reference/6.5-SNAPSHOT/migration-7/configuration.html)
34. JWT authentication in Spring Boot 3 with Spring Security 6 - Teco Tutorials, acceso: enero 4, 2026, [https://blog.tericcabrel.com/jwt-authentication-springboot-spring-security/](https://blog.tericcabrel.com/jwt-authentication-springboot-spring-security/)
35. Mastering Spring Profiles: Environment-Specific Configuration Made Easy | by Kunal Bhangale | Medium, acceso: enero 4, 2026, [https://medium.com/@bhangalekunal2631996/spring-profiles-detailed-explanation-fe5ca342fd71](https://medium.com/@bhangalekunal2631996/spring-profiles-detailed-explanation-fe5ca342fd71)
36. Spring Boot Profiles: Managing Multiple Environments Like a Pro - Igor Venturelli, acceso: enero 4, 2026, [https://igventurelli.io/spring-boot-profiles-managing-multiple-environments-like-a-pro/](https://igventurelli.io/spring-boot-profiles-managing-multiple-environments-like-a-pro/)
37. Unit Testing Using Spring Boot, JUnit and Mockito - DEV Community, acceso: enero 4, 2026, [https://dev.to/olymahmud/unit-testing-using-spring-boot-junit-and-mockito-2l0b](https://dev.to/olymahmud/unit-testing-using-spring-boot-junit-and-mockito-2l0b)
38. Getting started with Testcontainers in a Java Spring Boot Project, acceso: enero 4, 2026, [https://testcontainers.com/guides/testing-spring-boot-rest-api-using-testcontainers/](https://testcontainers.com/guides/testing-spring-boot-rest-api-using-testcontainers/)
39. Testcontainers container lifecycle management using JUnit 5, acceso: enero 4, 2026, [https://testcontainers.com/guides/testcontainers-container-lifecycle/](https://testcontainers.com/guides/testcontainers-container-lifecycle/)
40. A Practical Guide to Testing Spring Controllers With MockMvcTester | The IntelliJ IDEA Blog, acceso: enero 4, 2026, [https://blog.jetbrains.com/idea/2025/04/a-practical-guide-to-testing-spring-controllers-with-mockmvctester/](https://blog.jetbrains.com/idea/2025/04/a-practical-guide-to-testing-spring-controllers-with-mockmvctester/)
41. Choosing Between MockMvc and @SpringBootTest for Controller Testing - rieckpil, acceso: enero 4, 2026, [https://rieckpil.de/choosing-between-mockmvc-and-springboottest-for-testing/](https://rieckpil.de/choosing-between-mockmvc-and-springboottest-for-testing/)
42. How to Fetch and Display Data From API in ReactJS? - HCL GUVI, acceso: enero 4, 2026, [https://www.guvi.in/blog/how-to-fetch-and-display-data-from-api-in-react/](https://www.guvi.in/blog/how-to-fetch-and-display-data-from-api-in-react/)
43. Consuming a Rest API with Axios in Vue.js - GeeksforGeeks, acceso: enero 4, 2026, [https://www.geeksforgeeks.org/javascript/consuming-a-rest-api-with-axios-in-vue-js/](https://www.geeksforgeeks.org/javascript/consuming-a-rest-api-with-axios-in-vue-js/)
44. Understanding communicating with backend services using HTTP - Angular, acceso: enero 4, 2026, [https://v17.angular.io/guide/understanding-communicating-with-http](https://v17.angular.io/guide/understanding-communicating-with-http)
45. How to Connect an Angular Frontend with a Spring Boot Backend | by Kalana Heshan, acceso: enero 4, 2026, [https://kalanaheshan.medium.com/how-to-connect-an-angular-frontend-with-a-spring-boot-backend-fb7e52f86c13](https://kalanaheshan.medium.com/how-to-connect-an-angular-frontend-with-a-spring-boot-backend-fb7e52f86c13)
46. Getting Started: Fetching Data - Next.js, acceso: enero 4, 2026, [https://nextjs.org/docs/app/getting-started/fetching-data](https://nextjs.org/docs/app/getting-started/fetching-data)
47. Building APIs with Next.js, acceso: enero 4, 2026, [https://nextjs.org/blog/building-apis-with-nextjs](https://nextjs.org/blog/building-apis-with-nextjs)
48. Task Execution and Scheduling :: Spring Boot, acceso: enero 4, 2026, [https://docs.spring.io/spring-boot/reference/features/task-execution-and-scheduling.html](https://docs.spring.io/spring-boot/reference/features/task-execution-and-scheduling.html)
49. Building Scalable Asynchronous Backends with Spring Boot and Virtual Threads, acceso: enero 4, 2026, [https://dev.to/anarefin/building-scalable-asynchronous-backends-with-spring-boot-and-virtual-threads-1pj8](https://dev.to/anarefin/building-scalable-asynchronous-backends-with-spring-boot-and-virtual-threads-1pj8)
50. Real-Time Streaming with Spring AI ChatClient - Java Code Geeks, acceso: enero 4, 2026, [https://www.javacodegeeks.com/real-time-streaming-with-spring-ai-chatclient.html](https://www.javacodegeeks.com/real-time-streaming-with-spring-ai-chatclient.html)
51. Spring AI In Action with Open AI ( Chat Client ) - Ejyle, acceso: enero 4, 2026, [https://ejyle.com/2025/02/18/spring-ai-in-action-with-open-ai-chat-client/](https://ejyle.com/2025/02/18/spring-ai-in-action-with-open-ai-chat-client/)
52. Chat Client API :: Spring AI Reference, acceso: enero 4, 2026, [https://docs.spring.io/spring-ai/reference/api/chatclient.html](https://docs.spring.io/spring-ai/reference/api/chatclient.html)
53. Spring AI Structured Output Example - Java Code Geeks, acceso: enero 4, 2026, [https://www.javacodegeeks.com/spring-ai-structured-output-example.html](https://www.javacodegeeks.com/spring-ai-structured-output-example.html)
54. Structured Output Converter :: Spring AI Reference, acceso: enero 4, 2026, [https://docs.spring.io/spring-ai/reference/api/structured-output-converter.html](https://docs.spring.io/spring-ai/reference/api/structured-output-converter.html)
55. Tool Calling :: Spring AI Reference, acceso: enero 4, 2026, [https://docs.spring.io/spring-ai/reference/api/tools.html](https://docs.spring.io/spring-ai/reference/api/tools.html)
56. Spring AI Function Calling Example - HowToDoInJava, acceso: enero 4, 2026, [https://howtodoinjava.com/spring-ai/spring-ai-function-calling-example/](https://howtodoinjava.com/spring-ai/spring-ai-function-calling-example/)
57. Mastering Spring AI's New Tool Annotation: A Developer's Guide to Effortless AI Integration, acceso: enero 4, 2026, [https://aymankalaie.medium.com/mastering-spring-ais-tool-annotation-9b14b542b3ca](https://aymankalaie.medium.com/mastering-spring-ais-tool-annotation-9b14b542b3ca)
58. Build a GenAI App With Java Using Spring AI and Docker Model Runner, acceso: enero 4, 2026, [https://www.docker.com/blog/build-genai-app-with-java-spring-ai-docker-model-runner/](https://www.docker.com/blog/build-genai-app-with-java-spring-ai-docker-model-runner/)
59. Chroma :: Spring AI Reference, acceso: enero 4, 2026, [https://docs.spring.io/spring-ai/reference/api/vectordbs/chroma.html](https://docs.spring.io/spring-ai/reference/api/vectordbs/chroma.html)
60. Retrieval Augmented Generation :: Spring AI Reference, acceso: enero 4, 2026, [https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html)
61. Retrieval Augmented Generation (RAG) With Spring AI | by Kuldeep Singh - Medium, acceso: enero 4, 2026, [https://medium.com/manomano-tech/retrieval-augmented-generation-rag-with-spring-ai-89d29d9be9ed](https://medium.com/manomano-tech/retrieval-augmented-generation-rag-with-spring-ai-89d29d9be9ed)
62. Your Simple Guide to RAG in Spring AI: Give Your App a "Memory" | Coding Shuttle, acceso: enero 4, 2026, [https://www.codingshuttle.com/blogs/your-simple-guide-to-rag-in-spring-ai-give-your-app-a-memory/](https://www.codingshuttle.com/blogs/your-simple-guide-to-rag-in-spring-ai-give-your-app-a-memory/)
63. Spring AI with Multimodality and Images - Piotr's TechBlog, acceso: enero 4, 2026, [https://piotrminkowski.com/2025/03/04/spring-ai-with-multimodality-and-images/](https://piotrminkowski.com/2025/03/04/spring-ai-with-multimodality-and-images/)
64. Multimodality API :: Spring AI Reference, acceso: enero 4, 2026, [https://docs.spring.io/spring-ai/reference/api/multimodality.html](https://docs.spring.io/spring-ai/reference/api/multimodality.html)
65. 4 interesting new features in Spring Boot 3.4 : r/SpringBoot - Reddit, acceso: enero 4, 2026, [https://www.reddit.com/r/SpringBoot/comments/1i3cgkq/4_interesting_new_features_in_spring_boot_34/](https://www.reddit.com/r/SpringBoot/comments/1i3cgkq/4_interesting_new_features_in_spring_boot_34/)
66. 5 Tips for Structured Logging in Spring Boot 3.4 - Digma AI, acceso: enero 4, 2026, [https://digma.ai/6-tips-for-structured-logging-in-spring-boot-3-4/](https://digma.ai/6-tips-for-structured-logging-in-spring-boot-3-4/)
67. Structured Logging in Spring Boot | Baeldung, acceso: enero 4, 2026, [https://www.baeldung.com/spring-boot-structured-logging](https://www.baeldung.com/spring-boot-structured-logging)
