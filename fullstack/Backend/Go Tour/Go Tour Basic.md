---
sticker: lucide//ghost
banner: assets/ether-bg.jpeg
---
# Introducción
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
# Understanding Go Syntax

## Tipos de datos

### Primitivos
`Go` tiene tipos básicos muy directos:

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

---

### `Slices` y `Maps`
- **Slices**: listas dinámicas.

```go
numeros := []int{1, 2, 3}
numeros = append(numeros, 4)
```

- **Maps**: diccionarios clave-valor.

```go
edades := map[string]int{
    "Ana": 25,
    "Luis": 30,
}
fmt.Println(edades["Ana"])
```

---

## Apuntadores, `structs` e interfaces

- **Apuntadores**: permiten referenciar direcciones de memoria.

```go
var x int = 10
var p *int = &x // con & permite referencia a la direccion de memoria
fmt.Println(*p) // con * permite obtener el valor -> 10
```

- **Structs**: definen tipos compuestos.

```go
type Persona struct {
    Nombre string
    Edad   int
}

p := Persona{"Alguien", 28}
```

- **Interfaces**: definen comportamientos.

```go
type Animal interface {
    Hablar() string
}

type Perro struct{}
func (Perro) Hablar() string { return "Guau" }
```

---

## Estructuras de control
Go usa sintaxis clara y sin paréntesis extra:

```go
if x > 0 {
    fmt.Println("Positivo")
} else {
    fmt.Println("No positivo")
}

for i := 0; i < 5; i++ {
    fmt.Println(i)
}

switch dia {
case "lunes":
    fmt.Println("Inicio de semana")
default:
    fmt.Println("Otro día")
}
```

---

## Concurrencia
`Go` destaca por su **concurrencia con `goroutines` y canales**:

```go
go func() {
    fmt.Println("Ejecutando en paralelo")
}()

mensajes := make(chan string)
go func() { mensajes <- "Hola desde goroutine" }()
fmt.Println(<-mensajes)
```

---

## Manejo de Errores
Go usa valores de error explícitos:

```go
import "errors"

func dividir(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("división por cero")
    }
    return a / b, nil
}

resultado, err := dividir(10, 0)
if err != nil {
    fmt.Println("Error:", err)
}
```

---

## Manejo de estructura de datos
Go provee librerías estándar (`container/list`, `container/heap`, etc.):

```go
import "container/list"

l := list.New()
l.PushBack(1)
l.PushBack(2)
for e := l.Front(); e != nil; e = e.Next() {
    fmt.Println(e.Value)
}
```


