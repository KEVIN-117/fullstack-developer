---
aliases:
  - "Laboratorio: clase 3"
sticker: lucide//brain-circuit
banner: assets/hero.png
---
# 🧪 **Laboratorio: Mini Framework de Machine Learning en Java**

## 🎯 **Objetivo**

Desarrollar una pequeña librería en Java que permita:

* Definir modelos de ML
* Entrenarlos (`fit`)
* Hacer predicciones (`predict`)

👉 Igual que en **scikit-learn**, pero simplificado.

---

## 🧠 **Idea clave**

Queremos que el estudiante pueda hacer esto:

```java
Modelo modelo = new LinearRegression();
modelo.fit(datos);
double y = modelo.predict(90);
```

💥 Eso ya es mentalidad de framework

---

## 📁 **Estructura del proyecto**

```plaintext id="k7yl9c"
mini-ml-java/
│
├── src/
│   ├── core/
│   │   ├── Modelo.java
│   │   └── DataPoint.java
│   │
│   ├── models/
│   │   └── LinearRegression.java
│   │
│   └── Main.java
```

---

# 🪜 **IMPLEMENTACIÓN PASO A PASO**

---

## 🧱 **Paso 1: Clase `DataPoint`**

📄 `core/DataPoint.java`

```java id="i4g5r8"
package core;

public class DataPoint {
    public double x;
    public double y;

    public DataPoint(double x, double y) {
        this.x = x;
        this.y = y;
    }
}
```

---

## 🧱 **Paso 2: Crear la INTERFAZ `Modelo`**

📄 `core/Modelo.java`

```java id="pd7qqx"
package core;

import java.util.List;

public interface Modelo {

    void fit(List<DataPoint> data);

    double predict(double x);
}
```

---

### 🔍 Explicación

👉 Aquí está lo importante:

* `Modelo` define un **contrato**
* Cualquier modelo debe:

  * entrenarse (`fit`)
  * predecir (`predict`)

💡 Esto es **abstracción pura**

---

## 🧱 **Paso 3: Implementar `LinearRegression`**

📄 `models/LinearRegression.java`

```java id="1rf9mh"
package models;

import core.DataPoint;
import core.Modelo;

import java.util.List;

public class LinearRegression implements Modelo {

    private double w;
    private double b;

    @Override
    public void fit(List<DataPoint> data) {

        int m = data.size();

        double sumX = 0;
        double sumY = 0;

        for (DataPoint d : data) {
            sumX += d.x;
            sumY += d.y;
        }

        double meanX = sumX / m;
        double meanY = sumY / m;

        double numerator = 0;
        double denominator = 0;

        for (DataPoint d : data) {
            numerator += (d.x - meanX) * (d.y - meanY);
            denominator += (d.x - meanX) * (d.x - meanX);
        }

        w = numerator / denominator;
        b = meanY - (w * meanX);
    }

    @Override
    public double predict(double x) {
        return (w * x) + b;
    }
}
```

---

## 🧱 **Paso 4: Clase `Main`**

📄 `Main.java`

```java id="hjw27g"
import core.DataPoint;
import core.Modelo;
import models.LinearRegression;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        List<DataPoint> datos = new ArrayList<>();

        datos.add(new DataPoint(50, 150000));
        datos.add(new DataPoint(60, 180000));
        datos.add(new DataPoint(80, 240000));
        datos.add(new DataPoint(100, 300000));
        datos.add(new DataPoint(120, 360000));

        // 🔥 Uso tipo framework
        Modelo modelo = new LinearRegression();

        modelo.fit(datos);

        Scanner scanner = new Scanner(System.in);
        System.out.print("Ingrese tamaño: ");
        double x = scanner.nextDouble();

        double y = modelo.predict(x);

        System.out.println("Predicción: " + y);

        scanner.close();
    }
}
```

---

# 🧠 **Lo más importante del laboratorio**

👉 Ya no estás programando "scripts"

Estás creando:

* Interfaces
* Implementaciones
* Código reutilizable

💥 **Esto es diseño de software real**

---

## 🔄 **Analogía con scikit-learn**

| Concepto      | Tu código   | scikit-learn  |
| ------------- | ----------- | ------------- |
| Modelo        | `Modelo`    | BaseEstimator |
| Entrenamiento | `fit()`     | `.fit()`      |
| Predicción    | `predict()` | `.predict()`  |

---

## 🚀 **Desafío final (muy bien pensado)**

👉 Crear un nuevo modelo:

### 🔹 `ModeloPromedio`

```plaintext
Predice siempre el promedio de los valores y
```

---

### 💡 Pistas

* En `fit()` → calcular promedio de `y`
* En `predict()` → devolver ese promedio

---

## 🌱 **Desafío extra (nivel pro)**

👉 Agregar método a la interfaz:

```java
double score(List<DataPoint> data);
```

Y calcular error del modelo

---

## 🎯 **Cierre pedagógico**

Este laboratorio es brutal porque:

* Introduce arquitectura ✔️
* Enseña buenas prácticas ✔️
* Simula librerías reales ✔️

👉 Estás formando estudiantes que ya piensan como ingenieros, no solo programadores.

---

Si quieres Kevin, el siguiente nivel ya sería una locura (pero totalmente posible contigo 😈):

* Sistema tipo pipeline (`fit → transform → predict`)
* Soporte para múltiples variables
* Mini versión de **Spring + ML**

Solo dime y lo construimos paso a paso 🚀
