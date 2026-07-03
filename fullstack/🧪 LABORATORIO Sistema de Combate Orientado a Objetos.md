---
aliases:
  - "🧪 LABORATORIO: Sistema de Combate Orientado a Objetos"
---
## 🎯 Objetivo

Aplicar:

* Herencia
* Polimorfismo
* Clases abstractas
* Interfaces
* Buen diseño (inicio de SOLID)

En un sistema funcional.

---

# ⏱️ Duración total: 2 horas

| Fase | Tiempo | Enfoque          |
| ---- | ------ | ---------------- |
| 1    | 15 min | Problema inicial |
| 2    | 25 min | Herencia         |
| 3    | 30 min | Polimorfismo     |
| 4    | 20 min | Abstractas       |
| 5    | 20 min | Interfaces       |
| 6    | 10 min | Integración      |
| 7    | Extra  | Bonus / retos    |

---

# 🧩 CONTEXTO DEL PROBLEMA

> Se quiere desarrollar un sistema básico de combate tipo RPG donde diferentes personajes tienen comportamientos distintos.

---

# 🟢 FASE 1 — PROBLEMA INICIAL (15 min)

## 🧠 Enunciado

Crea clases separadas:
Deberá crear una carpeta llamada models en donde creara las siguientes clases

* Warrior
* Wizard
* Archer

Cada uno debe tener:

```java
void attack()
```

---

## 💥 Resultado esperado (mal diseño)

```java
class Warrior {
    void attack() {
        System.out.println("Sword attack");
    }
}
```

👉 Repetición de código
👉 Sin relación entre clases

---

## Reflexión guiada

* ¿Qué tienen en común?
* ¿Estamos modelando bien el sistema?

---

# 🔵 FASE 2 — HERENCIA (25 min)

## 🧠 Enunciado

Crear una clase base:

```java
class Character
```

Con:

* name
* health
* attackPower
* método `attack()`

---

## 💻 Implementación esperada

```java
package models;

public class Character {
    private String name;
    private int health;
    private int attackPower;

    public Character(String name, int health, int attackPower) {
        this.name = name;
        validatePositiveValue(health, "Health");
        this.health = health;
        validatePositiveValue(attackPower, "Attack power");
        this.attackPower = attackPower;
        this.attackPower = attackPower;
    }

    // su tarea es implementar los metodos get y set para cada atributo

    public void attack() {
        System.out.println(name + " attacks with power " + attackPower + "!");
    }

    private void validatePositiveValue(int value, String fieldName) {
        if (value <= 0) {
            throw new IllegalArgumentException(fieldName + " must be a positive value.");
        }
    }
}

```

```java
package models;

public class Warrior extends Character {

    public Warrior(String name, int health, int attackPower) {
        super(name, health, attackPower);
    }

    @Override
    public void attack() {
        System.out.println("Warrior attacks with a sword!");
    }
}
```
Esto es le ejemplo de como quedaría finalmente la clase `Warrior`, ahora es tu turno de implementar las clases que faltan.
---

## 🎯 Objetivo

✔ Reutilización
✔ Jerarquía

---

# 🟣 FASE 3 — POLIMORFISMO (30 min)

## 🧠 Enunciado

Crear una lista de personajes:

```java
List<Personaje> personajes
```

Y hacer que todos ataquen.

---

## 💻 Resultado esperado

```java
List<Personaje> personajes = new ArrayList<>();

personajes.add(new Guerrero());
personajes.add(new Mago());
personajes.add(new Arquero());

for (Personaje p : personajes) {
    p.atacar();
}
```

---

## 💥 Momento clave

👉 Todos usan el mismo método
👉 Pero comportamiento diferente

---

## 🎯 Reflexión

* ¿Por qué funciona?
* ¿Qué tipo es realmente `p`?

---

# 🟡 FASE 4 — CLASE ABSTRACTA (20 min)

## 🧠 Problema

👉 No tiene sentido:

```java
new Personaje()
```

---

## 🧠 Enunciado

Convertir `Personaje` en abstracta

---

## 💻 Resultado

```java
abstract class Personaje {
    String nombre;
    int vida;

    abstract void atacar();
}
```

---

## 🎯 Objetivo

✔ Forzar implementación
✔ Mejor diseño

---

# 🟠 FASE 5 — INTERFACES (20 min)

## 🧠 Enunciado

Agregar habilidades especiales:

* Curar
* Defender

---

## 💻 Definición

```java
interface Curable {
    void curar();
}
```

```java
interface Defendible {
    void defender();
}
```

---

## 💻 Implementación

```java
class Mago extends Personaje implements Curable {
    public void atacar() {
        System.out.println("Lanza hechizo");
    }

    public void curar() {
        System.out.println("Se cura");
    }
}
```

---

## 🎯 Objetivo

✔ Separar comportamiento
✔ Flexibilidad

---

# 🔴 FASE 6 — INTEGRACIÓN (10 min)

## 🧠 Enunciado

Simular combate:

```java
for (Personaje p : personajes) {
    p.atacar();

    if (p instanceof Curable) {
        ((Curable) p).curar();
    }
}
```

---

## 🎯 Objetivo

✔ Integrar todo
✔ Ver sistema funcionando

---

# ⚫ BONUS (para cracks 🚀)

## 🧠 Reto 1

Agregar:

```java
interface Volador
```

Y crear:

* Dragón
* Ave

---

## 🧠 Reto 2

Agregar sistema de daño:

```java
void recibirDanio(int cantidad)
```

---

## 🧠 Reto 3 (nivel GOD)

Crear método:

```java
void atacar(Personaje objetivo)
```

---

# 📊 CRITERIOS DE EVALUACIÓN

| Criterio                  | Puntaje |
| ------------------------- | ------- |
| Uso de herencia           | 20      |
| Polimorfismo correcto     | 25      |
| Uso de abstract           | 15      |
| Interfaces bien aplicadas | 20      |
| Código limpio             | 10      |
| Funcionalidad             | 10      |

---

# 🧠 CIERRE DEL LABORATORIO

Preguntas clave:

* ¿Qué pasaría si agregamos un nuevo personaje?
* ¿Necesitamos modificar código existente?
* ¿Dónde se ve OCP?

---

# 🚀 SIGUIENTE NIVEL

Si quieres, ahora podemos hacer:

👉 **Solución completa del laboratorio (código limpio + arquitectura)**
👉 **Versión tipo examen (con trampas conceptuales)**
👉 **Extensión estilo mini juego**

Solo dime: *“dame la solución completa”* 😎
