---
aliases:
  - Sistema Inteligente de Recomendación de Cursos (POO + ML ligero)**
sticker: lucide//brain-circuit
banner: assets/ether-bg.jpeg
---
# 🧪 **Laboratorio en Casa

## 🎯 **Objetivo**

El estudiante será capaz de:

* Aplicar **POO (clases, objetos, métodos)**
* Usar **ArrayList y HashMap**
* Implementar una lógica de **recomendación (tipo Machine Learning básico)**
* Diseñar un sistema modular

---

# 🧠 **Idea del sistema**

Vamos a simular un sistema que:

👉 Recomienda cursos a estudiantes según sus intereses

💡 Ejemplo:

* Estudiante: le gusta `programación`, `IA`
* Curso: contiene `programación`, `bases de datos`

👉 Resultado:

* Coincidencia → recomendado

---

# 🧩 **Concepto tipo ML (simplificado)**

Esto es una versión básica de:

* Sistemas de recomendación
* Similaridad entre conjuntos

👉 Regla:

```plaintext
score = cantidad de coincidencias
```

---

# 📁 **Estructura del proyecto**

```plaintext
smart-recommendation/
│
├── src/
│   ├── Estudiante.java
│   ├── Curso.java
│   ├── SistemaRecomendacion.java
│   └── Main.java
```

---

# 🪜 **IMPLEMENTACIÓN PASO A PASO**

---

## 🧱 **Paso 1: Clase `Estudiante`**

```java
import java.util.ArrayList;

public class Estudiante {

    String nombre;
    ArrayList<String> intereses;

    public Estudiante(String nombre) {
        this.nombre = nombre;
        this.intereses = new ArrayList<>();
    }

    public void agregarInteres(String interes) {
        intereses.add(interes.toLowerCase());
    }
}
```

---

## 🧱 **Paso 2: Clase `Curso`**

```java
import java.util.ArrayList;

public class Curso {

    String nombre;
    ArrayList<String> temas;

    public Curso(String nombre) {
        this.nombre = nombre;
        this.temas = new ArrayList<>();
    }

    public void agregarTema(String tema) {
        temas.add(tema.toLowerCase());
    }
}
```

---

## 🧱 **Paso 3: Sistema de Recomendación**

🔥 Aquí está la magia

```java
import java.util.*;

public class SistemaRecomendacion {

    ArrayList<Curso> cursos;
    HashMap<String, ArrayList<Curso>> historial;

    public SistemaRecomendacion() {
        cursos = new ArrayList<>();
        historial = new HashMap<>();
    }

    public void agregarCurso(Curso curso) {
        cursos.add(curso);
    }

    public List<Curso> recomendar(Estudiante estudiante) {

        HashMap<Curso, Integer> puntuacion = new HashMap<>();

        for (Curso curso : cursos) {

            int score = 0;

            for (String interes : estudiante.intereses) {
                if (curso.temas.contains(interes)) {
                    score++;
                }
            }

            puntuacion.put(curso, score);
        }

        // Ordenar cursos por puntuación
        List<Map.Entry<Curso, Integer>> lista = new ArrayList<>(puntuacion.entrySet());

        lista.sort((a, b) -> b.getValue() - a.getValue());

        List<Curso> recomendados = new ArrayList<>();

        for (Map.Entry<Curso, Integer> entry : lista) {
            if (entry.getValue() > 0) {
                recomendados.add(entry.getKey());
            }
        }

        // Guardar historial
        historial.put(estudiante.nombre, new ArrayList<>(recomendados));

        return recomendados;
    }
}
```

---

## 🧱 **Paso 4: `Main`**

```java
import java.util.*;

public class Main {

    public static void main(String[] args) {

        SistemaRecomendacion sistema = new SistemaRecomendacion();

        // Crear cursos
        Curso c1 = new Curso("Programación en Java");
        c1.agregarTema("programacion");

        Curso c2 = new Curso("Introducción a IA");
        c2.agregarTema("ia");

        Curso c3 = new Curso("Bases de Datos");
        c3.agregarTema("datos");

        sistema.agregarCurso(c1);
        sistema.agregarCurso(c2);
        sistema.agregarCurso(c3);

        // Crear estudiante
        Estudiante est = new Estudiante("Kevin");
        est.agregarInteres("programacion");
        est.agregarInteres("ia");

        // Recomendación
        List<Curso> recomendados = sistema.recomendar(est);

        System.out.println("Cursos recomendados:");

        for (Curso c : recomendados) {
            System.out.println("- " + c.nombre);
        }
    }
}
```

---

# 🧠 **Qué aprendieron (nivel GOD)**

👉 Técnicamente hicieron:

* ✔ POO real
* ✔ Uso combinado de `ArrayList` y `HashMap`
* ✔ Sistema de scoring
* ✔ Ordenamiento
* ✔ Lógica tipo ML

💥 Esto es un **recomendador real simplificado**

---

# ⚠️ **Errores comunes**

* No convertir a minúsculas
* No inicializar listas
* No entender `HashMap<Curso, Integer>`

---

# 🚀 **Desafíos (clave para aprendizaje)**

---

## 🔹 Nivel 1

Mostrar el **score de cada curso**

---

## 🔹 Nivel 2

Permitir ingresar intereses desde teclado

---

## 🔹 Nivel 3 (🔥 recomendado)

Guardar múltiples estudiantes en el sistema

---

## 🔹 Nivel 4 (ML real)

Normalizar score:

```plaintext
score = coincidencias / total_intereses
```

---

## 🔹 Nivel 5 (pro)

Evitar recomendar cursos ya vistos
