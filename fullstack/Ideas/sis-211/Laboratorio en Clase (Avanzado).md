---
sticker: lucide//brain
banner: assets/ether-bg.jpeg
---
# 🧪 **Regresión Lineal en Java con Entrenamiento**

## 🎯 **Objetivo del laboratorio**

El estudiante será capaz de:

* Implementar un modelo de regresión lineal desde cero
* Calcular automáticamente los parámetros del modelo (**w** y **b**)
* Aplicar lógica matemática en código Java
* Entender cómo un modelo “aprende” a partir de datos

---

## 🧠 **Concepto clave**

Antes, usábamos valores fijos.
Ahora el programa **aprende los valores de w y b a partir de los datos**.

---

## 🧮 **Modelo matemático**

Seguimos usando:

f_{w,b}(x)=wx+b

Pero ahora:

👉 **w y b se calculan automáticamente**

---

## 📐 **Fórmulas a implementar**

### 🔹 Pendiente (w)

w = \frac{\sum_{i=1}^{m}(x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^{m}(x_i - \bar{x})^2}

---

### 🔹 Intercepto (b)

b = \bar{y} - w \bar{x}

---

### 🔍 ¿Qué significa esto?

* `x̄` → promedio de x
* `ȳ` → promedio de y
* `m` → número de datos

👉 Básicamente estamos encontrando la **mejor línea que se ajusta a los datos**

---

## 📁 **Estructura del proyecto (igual que antes)**

```plaintext
src/
├── Main.java
├── Casa.java
└── ModeloLineal.java
```

---

# 🪜 **IMPLEMENTACIÓN PASO A PASO**

---

## 🧱 **Paso 1: Clase `Casa` (sin cambios)**

```java
public class Casa {
    double tamano;
    double precio;

    public Casa(double tamano, double precio) {
        this.tamano = tamano;
        this.precio = precio;
    }
}
```

---

## 🧱 **Paso 2: Clase `ModeloLineal` (versión avanzada)**

Aquí está la parte importante 👇

```java
import java.util.List;

public class ModeloLineal {

    double w;
    double b;

    // Método para entrenar el modelo
    public void entrenar(List<Casa> datos) {

        int m = datos.size();

        double sumaX = 0;
        double sumaY = 0;

        // 1. Calcular sumatorias
        for (Casa c : datos) {
            sumaX += c.tamano;
            sumaY += c.precio;
        }

        double promedioX = sumaX / m;
        double promedioY = sumaY / m;

        double numerador = 0;
        double denominador = 0;

        // 2. Calcular numerador y denominador
        for (Casa c : datos) {
            double x = c.tamano;
            double y = c.precio;

            numerador += (x - promedioX) * (y - promedioY);
            denominador += (x - promedioX) * (x - promedioX);
        }

        // 3. Calcular w y b
        w = numerador / denominador;
        b = promedioY - (w * promedioX);
    }

    // Método de predicción
    public double predecir(double x) {
        return (w * x) + b;
    }
}
```

---

## 🧱 **Paso 3: Clase `Main`**

```java
import java.util.ArrayList;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        ArrayList<Casa> casas = new ArrayList<>();

        casas.add(new Casa(50, 150000));
        casas.add(new Casa(60, 180000));
        casas.add(new Casa(80, 240000));
        casas.add(new Casa(100, 300000));
        casas.add(new Casa(120, 360000));

        ModeloLineal modelo = new ModeloLineal();

        // 🔥 ENTRENAMIENTO
        modelo.entrenar(casas);

        System.out.println("Modelo entrenado:");
        System.out.println("w (pendiente): " + modelo.w);
        System.out.println("b (intercepto): " + modelo.b);

        Scanner scanner = new Scanner(System.in);
        System.out.print("\nIngrese el tamaño de la casa: ");
        double x = scanner.nextDouble();

        double resultado = modelo.predecir(x);

        System.out.println("Precio estimado: " + resultado);

        scanner.close();
    }
}
```

---

## ▶️ **Ejecución esperada**

```plaintext
Modelo entrenado:
w: 3000.0
b: 0.0

Ingrese el tamaño:
90

Precio estimado: 270000.0
```

---

## 🧠 **Qué acaba de pasar (MUY IMPORTANTE)**

👉 Tu programa ahora:

1. Recibe datos
2. Calcula estadísticas
3. Ajusta un modelo
4. Hace predicciones

💥 **Esto es Machine Learning real (nivel base)**

---

## ⚠️ **Errores comunes**

* División por cero (si todos los x son iguales)
* No usar `double`
* Lista vacía
* Olvidar llamar a `entrenar()`

---

## 🚀 **Desafío final (bien pensado para estudiantes)**

👉 Agrega un método:

```java
double calcularError(List<Casa> datos)
```

Que calcule el **error promedio del modelo**:

💡 Pista:

```plaintext
error = (y_real - y_predicho)^2
```

---

## 🌱 **Mini desafío extra**

* Mostrar cuál dato tiene mayor error
* Mostrar todos los errores

---

## 🎯 **Cierre pedagógico**

Este laboratorio es oro porque:

* Enseña Java con propósito ✔️
* Introduce estadística sin miedo ✔️
* Conecta con IA real ✔️

---

Si quieres Kevin, el siguiente nivel sería brutal 🚀:

* implementar **gradiente descendente (como en cursos pro de ML)**
* o hacer una versión tipo **mini framework en Java estilo scikit-learn**

Solo dime y lo armamos 😈
