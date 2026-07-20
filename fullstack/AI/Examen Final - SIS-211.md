# Examen final de Programación II


### Pregunta 1

3 / 3 pts
¿Cuál de las siguientes clases pertenece al paquete java.lang y puede utilizarse sin importarla explícitamente?

- `ArrayList`
- `HashMap`
- → String(correcta)
- Scanner

### Pregunta 2
¿Qué modificador de acceso permite que un atributo sea accesible solamente dentro de la misma clase?

- → public
- `protected`
- `private(correcta)`
- `static`

### Pregunta 3

0 / 3 pts
Un atributo declarado con el modificador protected puede ser accedido principalmente desde:

- Cualquier clase de cualquier paquete
- La misma clase, clases del mismo paquete y clases hijas(correcta)
- → Solamente la clase donde fue declarado
- Únicamente métodos estáticos

### Pregunta 4

0 / 3 pts
¿Cuál es la característica principal de un atributo declarado como static?

- Existe una copia distinta para cada objeto
- Pertenece a la clase y es compartido por todos sus objetos(correcta)
- → No puede cambiar su valor
- Solo puede ser usado dentro del constructor

### Pregunta 5

0 / 3 pts
Respecto a las clases static en Java, ¿cuál afirmación es correcta?

- Toda clase principal debe declararse static
- Una clase de nivel superior puede declararse static
- Una clase interna puede declararse static(correcta)
- Una clase static siempre debe ser abstracta

### Pregunta 6

3 / 3 pts
¿Cuál es la principal ventaja de `ArrayList` frente a un arreglo tradicional?

- → Su tamaño puede crecer o reducirse dinámicamente(correcta)
- Solo almacena números enteros
- No permite elementos repetidos
- Siempre ordena sus elementos automáticamente
### Pregunta 7

3 / 3 pts
¿Qué método de `ArrayList` se utiliza para añadir un elemento al final de la lista?

- `put()`
- → `add()`(correcta)
- `insert()`
- `append()`

### Pregunta 8

0 / 3 pts
¿Cuál es la función principal de `HashMap` en Java?

- → Guardar elementos únicamente en orden ascendente
- Relacionar claves únicas con valores(correcta)
- Evitar completamente valores nulos
- Almacenar objetos únicamente de tipo String
### Pregunta 9

0 / 3 pts
¿Qué ocurre si se inserta en un HashMap un nuevo valor utilizando una clave que ya existe?

- Se genera obligatoriamente una excepción
- El nuevo valor reemplaza al valor asociado a esa clave(correcta)
- Se crea una segunda clave idéntica
- El `HashMap` elimina todos sus elementos

### Pregunta 10

0 / 3 pts
En programación orientada a objetos, la abstracción consiste en:

- → Ocultar datos privados mediante `getters` y `setters`
- Representar las características esenciales de un objeto, ignorando detalles innecesarios(correcta)
- Crear varias clases hijas a partir de una clase padre
- Repetir un método con diferentes parámetros

### Pregunta 11

0 / 3 pts
¿Qué principio de programación orientada a objetos busca proteger los atributos de una clase y controlar su acceso?

- Herencia
- Polimorfismo
- Encapsulamiento(correcta)
- Sobrecarga

### Pregunta 12

3 / 3 pts
La herencia permite principalmente:

- → Que una clase reutilice y extienda los atributos y métodos de otra clase(correcta)
- Que todos los atributos sean públicos
- Que una clase tenga varios constructores idénticos
- Que un objeto no pueda tener métodos

### Pregunta 13

3 / 3 pts
El polimorfismo permite que:

- → Una referencia de tipo padre invoque el comportamiento redefinido de un objeto hijo(correcta)
- Una clase herede de varias clases al mismo tiempo
- Los atributos privados sean modificados directamente
- Los métodos estáticos puedan ser sobrescritos

### Pregunta 14

0 / 3 pts
¿Cuándo ocurre la sobrecarga de métodos?

- → Cuando una clase hija redefine un método heredado con la misma firma
- Cuando existen métodos con el mismo nombre, pero diferente cantidad o tipo de parámetros(correcta)
- Cuando un atributo cambia de `public` a `private`
- Cuando una interfaz implementa otra interfaz

### Pregunta 15

3 / 3 pts
¿Cuál condición es necesaria para sobrescribir correctamente un método heredado?

- Cambiar el nombre del método
- → Usar exactamente los mismos parámetros y una firma compatible(correcta)
- Declarar el método siempre como `static`
- Eliminar el método de la clase padre

### Pregunta 16

0 / 3 pts
Seleccione las afirmaciones correctas sobre las clases abstractas.

- No pueden instanciarse directamente(correcta)
- → Pueden contener métodos abstractos y métodos concretos(correcta)
- → No pueden tener constructores
- Pueden ser utilizadas como clase base para otras clases(correcta)

### Pregunta 17

0 / 3 pts
Seleccione las afirmaciones correctas sobre las interfaces en Java.

- → Una clase puede implementar varias interfaces(correcta)
- Una interfaz puede extender otra interfaz(correcta)
- Una clase puede extender varias clases
- → Las interfaces ayudan a definir contratos de comportamiento(correcta)

### Pregunta 18

0 / 3 pts
¿Qué caracteriza a una interfaz funcional?

- Debe tener exactamente un método abstracto(correcta)
- No puede contener métodos estáticos
- Debe ser implementada por varias clases
- → No puede utilizar expresiones lambda

### Pregunta 19

3 / 3 pts
¿Cuál de las siguientes expresiones puede utilizarse para representar una implementación de una interfaz funcional?

- → Una expresión lambda(correcta)
- Un `import` estático
- Un constructor privado
- Un bloque `finally`

### Pregunta 20

0 / 3 pts
Seleccione las afirmaciones correctas sobre la relación entre herencia e interfaces.

- → Una clase puede extender una clase e implementar una o más interfaces(correcta)
- Una interfaz puede extender varias interfaces(correcta)
- → Una clase hija debe implementar los métodos abstractos heredados, salvo que también sea abstracta(correcta)
- Implementar una interfaz impide heredar de una clase

### Pregunta 21

5 / 15 pts
Implemente una clase `CuentaBancaria` aplicando encapsulamiento. La clase debe tener los atributos privados titular y saldo. Incluya un `constructor`, `getters`, un método `depositar(double monto)` que solo acepte montos positivos y un método `retirar(double monto)` que solo permita retirar dinero si el monto es positivo y no supera el saldo disponible. Finalmente, cree un método `mostrarResumen()` que devuelva los datos principales de la cuenta.

Tu respuesta

```java
public class CuentaBancaria{
  string titular;
  double saldo;

  public void(string titular, double saldo)
    this.titular = titular;
    this.saldo = saldo;

  
}
```
Comentario del docente

Faltan atributos privados y validaciones. El constructor no está correctamente definido. Revisa la sintaxis y completa la implementación.


### Pregunta 22

0 / 15 pts
Diseñe una solución usando abstracción, herencia, `sobrescritura` y polimorfismo. Cree una clase abstracta Empleado con los atributos nombre y `salarioBase`, además de un método abstracto `calcularSalario()`. Cree las clases Desarrollador y Gerente que hereden de Empleado. El desarrollador debe recibir un bono fijo y el gerente una comisión porcentual sobre su salario base. En una clase principal, almacene distintos empleados en un `ArrayList<Empleado>` y recorra la lista mostrando el nombre y el salario calculado de cada uno.

Tu respuesta

```java

```

### Pregunta 23

0 / 10 pts
Implemente una interfaz funcional llamada `OperacionMatematica` con un único método `operar(double a, double b)`. En una clase principal, cree mediante expresiones lambda las operaciones de suma, resta y multiplicación. Guarde las operaciones en un `HashMap<String, OperacionMatematica>`, utilizando como claves `suma`, `resta` y `multiplicacion`. Luego solicite dos números, ejecute las tres operaciones y muestre los resultados.

Tu respuesta

```java
public interface OperacionesMatematicas¨{
  
  
  
}
```

> [!NOTE]
> # Explicación