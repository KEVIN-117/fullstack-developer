# Resumen: Concurrency in Go

**Autora:** Katherine Cox-Buday

## ¿Por qué este libro?

*Concurrency in Go* nace de la necesidad de proporcionar a la comunidad de Go una guía exhaustiva y de alta calidad sobre la concurrencia. Aunque Go fue diseñado con la concurrencia como una de sus características principales y hace que trabajar con ella sea intuitivo (gracias a las goroutines y canales), Katherine Cox-Buday identificó que faltaban recursos que explicaran no solo la sintaxis, sino también las mejores prácticas, los patrones de diseño y el funcionamiento interno del runtime.

El objetivo del libro es equilibrar tres aspectos fundamentales:
1. **Cómo usar la concurrencia:** Sintaxis básica y primitivas de Go.
2. **Patrones y mejores prácticas:** Cómo estructurar sistemas concurrentes de manera efectiva y evitar errores comunes.
3. **Funcionamiento interno:** Qué sucede "bajo el capó" (runtime y programación de goroutines).

Este libro está dirigido a desarrolladores que ya tienen cierta experiencia con Go y desean dominar el arte de escribir programas concurrentes seguros y escalables.

## Índice

1. [**Preface**](Preface.md)
2. [**Capítulo 1: An Introduction to Concurrency**](Chapter%201.%20An%20Introduction%20to%20Concurrency.md)
   - Perspectiva histórica y problemas fundamentales de la concurrencia (condiciones de carrera, interbloqueos, etc.).
3. [**Capítulo 2: Modeling Your Code - Communicating Sequential Processes**](Chapter%202.%20Modeling%20Your%20Code%20-%20Communicating%20Sequential%20Processes.md)
   - Motivación detrás del diseño de Go y el modelo CSP.
4. [**Capítulo 3: Go’s Concurrency Building Blocks**](Chapter%203.%20Go’s%20Concurrency%20Building%20Blocks.md)
   - Sintaxis de goroutines, canales y el paquete `sync`.
5. [**Capítulo 4: Concurrency Patterns in Go**](Chapter%204.%20Concurrency%20Patterns%20in%20Go.md)
   - Composición de primitivas para formar patrones útiles y evitar errores.
6. [**Capítulo 5: Concurrency at Scale**](Chapter%205.%20Concurrency%20at%20Scale.md)
   - Aplicación de patrones en sistemas grandes y distribuidos.
7. [**Capítulo 6: Goroutines and the Go Runtime**](Chapter%206.%20Goroutines%20and%20the%20Go%20Runtime.md)
   - Detalles sobre cómo el runtime de Go gestiona y programa las goroutines.
