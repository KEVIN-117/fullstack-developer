---
sticker: lucide//brain-circuit
banner: assets/hero.png
---
# 🧪 **Clasificador Simple (Spam vs No Spam)**

👉 Este laboratorio introduce **clasificación (otro tipo de ML)**, pero sin matemáticas pesadas.

---

## 🎯 **Idea principal**

Crear un sistema que determine si un mensaje es:

* 📩 **SPAM**
* ✅ **NO SPAM**

Basado en palabras clave.

---

## 🧠 **Conceptos que enseña**

* Clasificación (vs regresión)
* Lógica condicional
* Uso de `HashMap`
* Conteo de frecuencia
* Diseño de clases

💥 Esto es una versión simplificada de lo que hacen modelos reales

---

# 📘 **Enunciado de la práctica**

Se desea construir un sistema que clasifique mensajes como **SPAM o NO SPAM**, utilizando un conjunto de palabras asociadas a spam.

El sistema debe:

1. Analizar un mensaje
2. Contar palabras sospechosas
3. Decidir si es spam según una regla simple

---

## 📁 **Estructura sugerida**

```plaintext
spam-classifier/
│
├── src/
│   ├── Message.java
│   ├── SpamClassifier.java
│   └── Main.java
```

---

# 🪜 **Implementación paso a paso**

---

## 🧱 **Paso 1: Clase `Message`**

```java
public class Message {
    String content;

    public Message(String content) {
        this.content = content;
    }
}
```

---

## 🧱 **Paso 2: Clase `SpamClassifier`**

```java
import java.util.HashMap;

public class SpamClassifier {

    HashMap<String, Integer> spamWords;

    public SpamClassifier() {
        spamWords = new HashMap<>();

        // palabras típicas de spam
        spamWords.put("gratis", 1);
        spamWords.put("oferta", 1);
        spamWords.put("dinero", 1);
        spamWords.put("gana", 1);
        spamWords.put("click", 1);
    }

    public boolean esSpam(String mensaje) {

        String[] palabras = mensaje.toLowerCase().split(" ");
        int contador = 0;

        for (String palabra : palabras) {
            if (spamWords.containsKey(palabra)) {
                contador++;
            }
        }

        return contador >= 2; // regla simple
    }
}
```

---

## 🧱 **Paso 3: `Main`**

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        SpamClassifier classifier = new SpamClassifier();
        Scanner scanner = new Scanner(System.in);

        System.out.print("Ingrese un mensaje: ");
        String mensaje = scanner.nextLine();

        boolean resultado = classifier.esSpam(mensaje);

        if (resultado) {
            System.out.println("SPAM detectado 🚫");
        } else {
            System.out.println("Mensaje válido ✅");
        }

        scanner.close();
    }
}
```

---

# 🧠 **Explicación simple (para estudiantes)**

👉 El programa hace esto:

1. Divide el mensaje en palabras
2. Busca palabras sospechosas
3. Cuenta cuántas hay
4. Decide si es spam

---

# 💥 **Conexión con Machine Learning real**

Esto es una versión simplificada de:

* Naive Bayes
* NLP básico
* Clasificadores de texto

👉 Estás enseñando la idea SIN complicar matemáticas

---

# 🚀 **Desafíos (muy bien pensados)**

## 🔹 Nivel 1

Agregar más palabras al diccionario

---

## 🔹 Nivel 2

Cambiar la regla:

```plaintext
>= 3 palabras → spam
```

---

## 🔹 Nivel 3

Usar `HashMap<String, Integer>` con pesos:

```java
"gratis" → 3
"oferta" → 2
```

👉 sumar puntos en vez de contar

---

## 🔹 Nivel 4 (🔥 recomendado)

Mostrar cuántas palabras sospechosas se encontraron

---

# 🌱 **Otra idea (rápida para futuro laboratorio)**

Si quieres seguir esta línea, te dejo otras prácticas potentes:

---

## 1. 🎯 Sistema de recomendación básico

* recomendar películas según gustos
* usa listas y coincidencias

---

## 2. 📊 Clasificador de estudiantes

* aprobado / reprobado según notas
* introduce lógica de decisión

---

## 3. 🎮 KNN simplificado (MUY BUENO)

* comparar distancias entre puntos
* introduce geometría + ML

