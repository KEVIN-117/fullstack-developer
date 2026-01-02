---
sticker: lucide//ghost
banner: assets/ether-bg.jpeg
---
# 1. Introducción
`Go` también conocido como `Golang` es un lenguaje compilado podríamos verlo como un lenguaje tan versátil como la de `C/C++` pero con la simplicidad de `Python`. Su sintaxis base es la siguiente
```go
package main

import "fmt"

func main(){
    fmt.Println("Hello Gophers...!")
}
```
---
Una de las características de `go` es su simplicidad a la hora de copilar
## Go Build 
La compilación de un archivo `.go` es realmente muy sencillo, solo basta con ejecutar `go build file.go -o dest`, pero esto no es todo ya que podemos indicarle a `go` que optimicé el archivo para que al final no pese demasiado, esto lo podemos lograr con `go build -ldflags "-w -s"` con esto el archivo final con pesara tanto
## Compilación Cruzada (Cross-Compiling)
La compilación cruzada es una de las ventajas mas grandes que se tiene al momento de trabajar con `go`, ya que no permite compilar todo nuestro código para diferentes sistemas y arquitecturas sin la necesidad de configurar nada adicional esto realmente muy bueno `（￣︶￣）↗`.
Por decir supongamos que tenemos `hello.go` con el código de ejemplo que tenemos en la introducción, ahora por la terminal nosotros usamos el `build` acompañados de `GOOS` y `GOARCH` son variables de entorno que definen el sistema operativo (OS) y la arquitectura de CPU para los cuales se quiere compilar un programa, esto generar binarios que funcionen en plataformas distintas a la máquina donde se desarrolla 

---
### ¿Qué es GOOS?
- **GOOS** significa *Go Operating System*.  
- Indica el **sistema operativo destino** del binario.  
- Ejemplos comunes:
  - `linux`
  - `windows`
  - `darwin` (macOS)
  - `freebsd`
  - `android`
---
### ¿Qué es GOARCH?
- **GOARCH** significa *Go Architecture*.  
- Define la **arquitectura de CPU** para la que se compila.  
- Ejemplos comunes:
  - `amd64` → 64 bits (x86_64)
  - `386` → 32 bits (x86)
  - `arm` → ARM de 32 bits
  - `arm64` → ARM de 64 bits
  - `ppc64`, `mips`, etc.

---

**Ejemplo práctico**
Si estás en Linux pero quieres compilar para Windows de 64 bits:

```bash
GOOS=windows GOARCH=amd64 go build -o app.exe main.go
```

Esto genera un ejecutable `app.exe` que corre en Windows, aunque lo hayas compilado desde Linux.

---
Puntos clave
- **Compilación cruzada**: Permite crear binarios para otros sistemas sin necesidad de usar máquinas virtuales o contenedores.  
- **CGO_ENABLED=0**: A menudo se desactiva cuando se hace compilación cruzada, porque el uso de C puede complicar la portabilidad.  
- **Ventaja de Go**: Su compilador soporta compilación cruzada de forma nativa, lo que lo hace muy útil para distribuir software multiplataforma.
---

| Variable   | Significado                 | Ejemplo                      | Uso                                |
| ---------- | --------------------------- | ---------------------------- | ---------------------------------- |
| **GOOS**   | Sistema operativo destino   | `linux`, `windows`, `darwin` | Define el OS del binario           |
| **GOARCH** | Arquitectura de CPU destino | `amd64`, `arm64`, `386`      | Define la arquitectura del binario |

---
```bash
# Compilar para Linux 64 bits
GOOS=linux GOARCH=amd64 go build -o app-linux main.go

# Compilar para Linux 32 bits
GOOS=linux GOARCH=386 go build -o app-linux-386 main.go

# Compilar para ARM 32 bits (ej. Raspberry Pi)
GOOS=linux GOARCH=arm go build -o app-arm main.go

# Compilar para ARM 64 bits
GOOS=linux GOARCH=arm64 go build -o app-arm64 main.go

# Compilar para Windows 64 bits
GOOS=windows GOARCH=amd64 go build -o app.exe main.go

# Compilar para Windows 32 bits
GOOS=windows GOARCH=386 go build -o app-386.exe main.go

# Compilar para macOS (Darwin) 64 bits Intel
GOOS=darwin GOARCH=amd64 go build -o app-darwin main.go

# Compilar para macOS (Darwin) ARM64 (Apple Silicon M1/M2)
GOOS=darwin GOARCH=arm64 go build -o app-darwin-arm64 main.go

# Compilar para FreeBSD 64 bits
GOOS=freebsd GOARCH=amd64 go build -o app-freebsd main.go

# Compilar para Android ARM64
GOOS=android GOARCH=arm64 go build -o app-android main.go
```

---

### Tips rápidos
- Usa `CGO_ENABLED=0` si quieres evitar dependencias de C en compilación cruzada:
  ```bash
  CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o app main.go
  ```
- Puedes listar todas las combinaciones soportadas con:
  ```bash
  go tool dist list
  ```

---
## Comandos de go

### 📦 `go get`
- **Función:** Descarga e instala paquetes y dependencias desde repositorios (generalmente GitHub u otros VCS).  
- **Uso típico:**
  ```bash
  go get github.com/user/proyecto
  ```
- **Notas:**
  - En versiones modernas de Go (>=1.17), `go get` ya no se usa para instalar binarios globales; se recomienda `go install paquete@versión`.
  - Sigue siendo útil para traer dependencias dentro de un módulo.

---

### 📖 `go doc`
- **Función:** Muestra documentación de paquetes, funciones, tipos y métodos directamente en la terminal.  
- **Uso típico:**
  ```bash
  go doc fmt
  go doc fmt.Println
  ```
- **Notas:**
  - Es como tener la documentación oficial sin abrir el navegador.
  - Muy útil para aprender la API estándar rápidamente.

---

### 🧹 `golint`
- **Función:** Herramienta externa que revisa el estilo del código Go y sugiere mejoras de acuerdo a las convenciones.  
- **Instalación:**
  ```bash
  go install golang.org/x/lint/golint@latest
  ```
- **Uso típico:**
  ```bash
  golint ./...
  ```
- **Notas:**
  - No es parte del core de Go, pero es ampliamente usado en proyectos educativos y de QA.
  - Se centra en estilo y convenciones, no en errores de compilación.

---

### 🔍 `go vet`
- **Función:** Analiza el código en busca de **errores sutiles** que compilan pero son sospechosos.  
- **Ejemplo:**
  ```bash
  go vet ./...
  ```
- **Detecta cosas como:**
  - Formatos incorrectos en `fmt.Printf`.
  - Uso de variables no inicializadas.
  - Problemas comunes de concurrencia.
- **Notas:**
  - Es más estricto que el compilador, pero no reemplaza pruebas unitarias.

---

### 🌐 Go Playground
- **Qué es:**  
  Es un entorno online oficial de Go (https://play.golang.org/) donde puedes escribir, ejecutar y compartir código Go sin instalar nada.
- **Características:**
  - Corre en un sandbox seguro con restricciones (tiempo de ejecución, acceso a red, etc.).
  - Ideal para ejemplos rápidos, compartir snippets y probar ideas.
  - Genera un enlace único para compartir tu código con otros.
- **Limitaciones:**
  - No permite acceso a archivos, red ni dependencias externas.
  - Tiempo de ejecución limitado (unos segundos).
- **Ejemplo de uso:**  
  Perfecto para enseñar un algoritmo, probar una función o mostrar un bug reproducible.

---

Resumen:  
- `go get` → dependencias.  
- `go doc` → documentación rápida.  
- `golint` → estilo y convenciones.  
- `go vet` → análisis estático de errores.  
- **Go Playground** → laboratorio online para probar y compartir código.
---
Perfecto, Kevin ⚡. Aquí tienes los apuntes completos siguiendo tu estructura, con definiciones cortas y ejemplos prácticos en cada sección:

---

# 2. Fundamentos (Basics)
---
## 2.1 Fundamentos (Basics)

---

### Paquetes y Exportación
- Todo programa en Go comienza en el **paquete `main`**.  
- Los paquetes permiten organizar el código en módulos reutilizables.

```go
package main

import "fmt"

func main() {
    fmt.Println("Hola desde main")
}
```

---

### Importaciones (`import`)
- Se usan para traer librerías estándar o externas.  
- Se pueden importar múltiples paquetes en un bloque o también la importación en una sola linea pero solo para un paquete

```go
import (
    "fmt"
    "math"
)
// import "fmt"

func main() {
    fmt.Println(math.Sqrt(16))
}
```

---

### Nombres exportados (Mayúscula vs Minúscula)
- En Go, **los identificadores que empiezan con mayúscula son exportados** (públicos).  
- Los que empiezan con minúscula son privados al paquete.

```go
// Exportado
func Sumar(a, b int) int { return a + b }

// No exportado
func restar(a, b int) int { return a - b }
```

---

### Variables y Funciones

#### Declaración de variables (`var` vs `:=`)
- `var` → declaración explícita.  
- `:=` → declaración corta con inferencia de tipo.

```go
var x int = 10
y := 20
```

#### Inicializadores
- Se pueden inicializar múltiples variables en una sola línea.

```go
var a, b, c = 1, 2, 3
```

#### Funciones: Retornos múltiples y valores de retorno con nombre
- Go permite retornar múltiples valores.  
- También se pueden nombrar los valores de retorno.

```go
func dividir(a, b int) (int, error) {
    if b == 0 {
        return 0, fmt.Errorf("división por cero")
    }
    return a / b, nil
}
```

---
### Enteros, Flotantes, Booleanos, Strings
- Tipos básicos ya vistos, con operaciones estándar.
- Primitivos: Go tiene tipos básicos muy directos:

```go
var entero int = 42
var flotante float64 = 3.14
var booleano bool = true
var texto string = "Hola Go"
```
- `int`, `int32`, `int64` → enteros  
- `float32`, `float64` → decimales  
- `bool` → verdadero/falso  
- `string` → texto  

*Estructura básica del lenguaje, variables y tipos primitivos.

```go
i := 5
f := 3.2
b := true
s := "Go es genial"
```

---
### Zero Values (Valores por defecto)
- En Go, las variables no inicializadas tienen un valor por defecto:
  - `int` → `0`
  - `float` → `0.0`
  - `bool` → `false`
  - `string` → `""`

```go
var x int    // 0
var y string // ""
```

---
### Conversión de tipos (`T(v)`)
- Se hace con la sintaxis `T(v)`.

```go
var x int = 10
var y float64 = float64(x)
```

---
### Inferencia de tipos
- Go infiere el tipo automáticamente con `:=`.

```go
mensaje := "Hola"
numero := 42
```

---
### Constantes
- Se definen con `const`.  
- No pueden cambiar durante la ejecución.

```go
const Pi = 3.14159
```

---
### Constantes numéricas de precisión arbitraria
- Las constantes numéricas en Go tienen **precisión arbitraria** hasta que se usan.  
- Esto permite cálculos seguros sin pérdida de precisión.

```go
const Big = 1 << 62
const Small = Big >> 61
```

---
## 2.2. Control de Flujo (Flow Control)

*Cómo se mueve la ejecución. Go unifica muchas estructuras.*

---

### La única estructura de bucle en Go
En Go **solo existe `for`**, pero es muy flexible y cubre los casos de `for`, `while` y bucles infinitos.

#### `for` clásico (con inicialización, condición y post-expresión)
```go
for i := 0; i < 5; i++ {
    fmt.Println(i)
}
```
*Equivalente al `for` de C/Java.*

#### `for` como `while`
```go
i := 0
for i < 5 {
    fmt.Println(i)
    i++
}
```
*Se omite la inicialización y el post-expresión, quedando como un `while`.*

#### Bucles infinitos
```go
for {
    fmt.Println("Loop infinito")
}
```
*Se usa en servidores, goroutines o listeners.*

#### Iteración sobre colecciones (`range`)
```go
numeros := []int{10, 20, 30}
for idx, val := range numeros {
    fmt.Println("Índice:", idx, "Valor:", val)
}
```
- `range` devuelve índice y valor.
- Se puede ignorar uno de ellos con `_`.

#### Iteración sobre mapas
```go
edades := map[string]int{"Ana": 25, "Luis": 30}
for nombre, edad := range edades {
    fmt.Println(nombre, edad)
}
```

#### Iteración sobre strings (runes)
```go
for i, r := range "Go!" {
    fmt.Printf("Posición %d: %c\n", i, r)
}
```

---

### Condicionales (If/Else)

#### `if` con sentencia corta de inicialización
```go
if x := obtenerValor(); x > 10 {
    fmt.Println("Mayor que 10")
} else {
    fmt.Println("Menor o igual a 10")
}
```
*La variable `x` solo existe dentro del bloque `if`.*

---

### Switch
El `switch` en Go es más poderoso y flexible que en otros lenguajes.

#### Switch con expresión
```go
switch dia {
case "lunes":
    fmt.Println("Inicio de semana")
case "viernes":
    fmt.Println("Casi fin de semana")
default:
    fmt.Println("Otro día")
}
```

#### Switch sin condición (como múltiples `if`)
```go
switch {
case x < 0:
    fmt.Println("Negativo")
case x == 0:
    fmt.Println("Cero")
default:
    fmt.Println("Positivo")
}
```

#### Múltiples valores en un mismo `case`
```go
switch letra {
case "a", "e", "i", "o", "u":
    fmt.Println("Es vocal")
default:
    fmt.Println("Es consonante")
}
```

#### Fallthrough
Permite continuar al siguiente `case` aunque ya se haya cumplido uno.
```go
switch numero := 2; numero {
case 1:
    fmt.Println("Uno")
case 2:
    fmt.Println("Dos")
    fallthrough
case 3:
    fmt.Println("Tres")
}
```
*Salida: "Dos" y "Tres".*

#### Orden de evaluación
- Los `case` se evalúan **de arriba hacia abajo**.
- Se ejecuta el **primer caso que cumpla la condición**.
- No hay necesidad de `break` (se hace automáticamente).

---

### Ejecución diferida (LIFO) con `defer`

#### Concepto
- `defer` pospone la ejecución de una función hasta que la función envolvente termine.  
- Se ejecuta en **orden inverso (Last In, First Out)**.  
- Muy útil para liberar recursos (cerrar archivos, conexiones, etc.).

#### Ejemplo básico
```go
func ejemplo() {
    defer fmt.Println("Último")
    defer fmt.Println("Segundo")
    fmt.Println("Primero")
}
```
**Salida:**
```
Primero
Segundo
Último
```

#### Uso típico: cerrar recursos
```go
func leerArchivo() {
    f, err := os.Open("data.txt")
    if err != nil {
        log.Fatal(err)
    }
    defer f.Close() // se asegura de cerrar el archivo al final

    // procesar archivo...
}
```

#### Stacking defers (apilamiento)
Se pueden apilar múltiples `defer`.  
Esto asegura que los recursos se liberen en orden inverso al que se adquirieron.

```go
func manejarArchivos() {
    f1, _ := os.Open("archivo1.txt")
    defer f1.Close()

    f2, _ := os.Open("archivo2.txt")
    defer f2.Close()

    fmt.Println("Procesando archivos...")
}
```

#### Evaluación inmediata de argumentos
Los **argumentos de la función diferida se evalúan inmediatamente**, aunque la función se ejecute después.
```go
func ejemplo() {
    x := 10
    defer fmt.Println(x) // imprime 10, aunque luego cambie
    x = 20
}
```

---

## 2.3. Estructuras y Tipos Complejos (More Types)

*Gestión de memoria y colecciones de datos.*

---

### Structs
Definen tipos compuestos que agrupan datos relacionados.
```go
type Persona struct {
    Nombre string
    Edad   int
}

p := Persona{"Alguien", 28}
fmt.Println(p.Nombre, p.Edad)
```

---

### Interfaces
Definen comportamientos que los tipos deben implementar.
```go
type Animal interface {
    Hablar() string
}

type Perro struct{}
func (Perro) Hablar() string { return "Guau" }

var a Animal = Perro{}
fmt.Println(a.Hablar())
```

---

### Punteros
Permiten referenciar direcciones de memoria.
```go
var x int = 10
var p *int = &x
fmt.Println(*p) // 10
```

---

### Referencias a memoria (`&`, `*`)
- `&` → obtiene la dirección de memoria.  
- `*` → desreferencia, accede al valor.

```go
y := 20
ptr := &y
fmt.Println(*ptr) // 20
```

---

### `nil`
Valor especial que indica ausencia de datos en punteros, slices, maps, interfaces, etc.
```go
var p *int = nil
if p == nil {
    fmt.Println("Puntero vacío")
}
```

---

### Definición de campos
Los campos de un `struct` pueden ser nombrados o anónimos.
```go
type Punto struct {
    X, Y int
}
```

---

### Literales de struct
Se pueden inicializar con valores directos.
```go
p := Punto{X: 10, Y: 20}
```

---

### Arrays (tamaño fijo) vs Slices (dinámicos)
- **Array**: tamaño fijo.
```go
var arr [3]int = [3]int{1, 2, 3}
```
- **Slice**: tamaño dinámico.
```go
slice := []int{1, 2, 3, 4}
```

---

### Longitud (`len`) y Capacidad (`cap`)
```go
s := make([]int, 3, 5)
fmt.Println(len(s)) // 3
fmt.Println(cap(s)) // 5
```

---

### Creación con `make`
`make` se usa para crear slices, maps y canales.
```go
s := make([]int, 0, 10)
m := make(map[string]int)
c := make(chan int)
```

---

### `append` y `copy`
- `append` agrega elementos.
```go
s := []int{1, 2}
s = append(s, 3, 4)
```
- `copy` copia elementos entre slices.
```go
a := []int{1, 2, 3}
b := make([]int, len(a))
copy(b, a)
```

---

### Slices de slices (Multidimensionales)
```go
matriz := [][]int{
    {1, 2},
    {3, 4},
}
fmt.Println(matriz[1][0]) // 3
```

---

### Iteración con `range`
```go
for i, v := range []string{"Go", "Rust", "C++"} {
    fmt.Println(i, v)
}
```

---

### Maps
#### Diccionarios clave-valor
```go
m := map[string]int{"Ana": 25, "Luis": 30}
```

#### Mutación de mapas (insertar, actualizar, borrar)
```go
m["Carlos"] = 40   // insertar
m["Ana"] = 26      // actualizar
delete(m, "Luis")  // borrar
```

#### Verificación de existencia (`elem, ok := m[key]`)
```go
edad, ok := m["Ana"]
if ok {
    fmt.Println("Edad de Ana:", edad)
}
```

---

### Funciones Avanzadas
#### Funciones como valores (First-class citizens)
Las funciones se pueden asignar a variables y pasar como argumentos.
```go
f := func(x int) int { return x * 2 }
fmt.Println(f(5)) // 10
```

#### Closures (Funciones anónimas y captura de estado)
Las funciones pueden capturar variables externas.
```go
func contador() func() int {
    x := 0
    return func() int {
        x++
        return x
    }
}

c := contador()
fmt.Println(c()) // 1
fmt.Println(c()) // 2
```

---

## 2.4. Métodos e Interfaces

*El enfoque de Go para la Orientación a Objetos.*  
Go no tiene clases como en Java o C++, pero permite asociar **métodos** a tipos y definir **interfaces** para comportamientos.

---

### Métodos
Los métodos se definen sobre tipos (structs o alias).  
```go
type Rectangulo struct {
    Ancho, Alto float64
}

// Método asociado al tipo Rectangulo
func (r Rectangulo) Area() float64 {
    return r.Ancho * r.Alto
}

r := Rectangulo{10, 5}
fmt.Println(r.Area()) // 50
```

---

### Receptores de valor vs. Receptores de puntero (`(v T)` vs `(v *T)`)
- **Receptor de valor (`(v T)`)**: recibe una copia del objeto. No modifica el original.
- **Receptor de puntero (`(v *T)`)**: recibe una referencia. Puede modificar el objeto.

```go
type Contador struct{ Valor int }

func (c Contador) IncrementarValor() { c.Valor++ }   // copia
func (c *Contador) IncrementarPuntero() { c.Valor++ } // referencia

c := Contador{}
c.IncrementarValor()
fmt.Println(c.Valor) // 0 (no cambia)

c.IncrementarPuntero()
fmt.Println(c.Valor) // 1 (sí cambia)
```

---

### Interfaces
Definen **comportamientos** que los tipos deben implementar.

#### Definición de comportamientos
```go
type Animal interface {
    Hablar() string
}
```

#### Implementación implícita (Duck typing)
No se declara explícitamente que un tipo implementa una interfaz; basta con que cumpla sus métodos.
```go
type Perro struct{}
func (Perro) Hablar() string { return "Guau" }

var a Animal = Perro{}
fmt.Println(a.Hablar())
```

#### Valores de interfaz y `nil`
Una interfaz puede contener un valor y su tipo.  
Si no contiene nada, es `nil`.
```go
var a Animal
if a == nil {
    fmt.Println("Interfaz vacía")
}
```

#### Interfaz vacía (`interface{}`)
Representa cualquier tipo.  
```go
func imprimir(v interface{}) {
    fmt.Println(v)
}

imprimir(42)
imprimir("texto")
```

#### Type Assertions
Permiten convertir una interfaz a su tipo concreto.
```go
var i interface{} = "hola"
s, ok := i.(string)
if ok {
    fmt.Println("Es string:", s)
}
```

#### Type Switches
Permiten evaluar el tipo dinámico de una interfaz.
```go
var i interface{} = 10
switch v := i.(type) {
case int:
    fmt.Println("Entero:", v)
case string:
    fmt.Println("Texto:", v)
default:
    fmt.Println("Otro tipo")
}
```

---

### Interfaces Comunes

#### `Stringers` (personalizar impresión)
La interfaz `fmt.Stringer` define el método `String() string`.
```go
type Persona struct{ Nombre string }
func (p Persona) String() string { return "Persona: " + p.Nombre }

fmt.Println(Persona{"Kevin"}) // Persona: Kevin
```

#### `Errors` (Interfaz `error` nativa)
La interfaz `error` define el método `Error() string`.
```go
type MiError struct{}
func (MiError) Error() string { return "Ocurrió un error" }

var err error = MiError{}
fmt.Println(err.Error())
```

#### `Readers` (Interfaz `io.Reader` para streams)
Define el método `Read(p []byte) (n int, err error)`.  
Ejemplo con `strings.NewReader`:
```go
r := strings.NewReader("Hola Go")
buf := make([]byte, 4)
n, _ := r.Read(buf)
fmt.Println(string(buf[:n])) // Hola
```

#### `Images` (Paquete `image`)
El paquete `image` define interfaces para manipular imágenes (`image.Image`).
```go
import "image"

var img image.Image // puede ser cualquier implementación
```


---
## 2.5. Genéricos (Go 1.18+)

*Polimorfismo paramétrico.*
### Funciones genéricas.
#### Tipos genéricos.
---
### Constraints
#### Restricciones (`comparable`, `any`).



## 2.6. Concurrencia

`Go` destaca por su **concurrencia con `goroutines` y canales**:

```go
go func() {
    fmt.Println("Ejecutando en paralelo")
}()

mensajes := make(chan string)
go func() { mensajes <- "Hola desde goroutine" }()
fmt.Println(<-mensajes)
```

*El "Killer Feature" de Go.*

* Goroutines
* Hilos ligeros gestionados por el runtime.
---
* Canales (Channels)
* Comunicación entre goroutines.
* Canales con buffer (Buffered Channels).
* `range` y `close`.
* Multiplexación de canales (esperar en múltiples canales).
* `default` en select.
---
* Exclusión Mutua
* `sync.Mutex` (para cuando no se necesitan canales).

# 3. Ejercicios Prácticos (Laboratorio)

*Espacio para la resolución de los ejercicios del Tour.*

* [[08.01 Ejercicio: Loops and Functions]] (Newton's Method)
-] (Pic generator)
* [[08.03 Ejercicio: Maps]] (Word Count)
* [[08.04 Ejercicio: Fibonacci Closure]]
-] (IP Addr)
* [[08.06 Ejercicio: Errors]] (Sqrt Error)
-] (ASCII Stream)
-] (Cipher Stream)
* [[08.09 Ejercicio: Images]] (Generator)
-] (Concurrency)
-] (Concurrency + Mutex)