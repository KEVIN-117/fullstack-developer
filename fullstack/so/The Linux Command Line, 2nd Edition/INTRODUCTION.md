![Imagen](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492071235/files/images/common01.jpg)

Quiero contarte una historia. No, no la historia de cómo, en 1991, Linus Torvalds escribió la primera versión del núcleo de Linux. Puedes leer esa historia en muchos libros de Linux. Tampoco voy a contaros la historia de cómo, años antes, Richard Stallman inició el Proyecto GNU para crear un sistema operativo libre tipo Unix. Esa también es una historia importante, pero la mayoría de los otros libros de Linux también tienen esa historia.

No, quiero contarte la historia de cómo recuperas el control de tu ordenador.

Cuando empecé a trabajar con ordenadores como estudiante universitario a finales de los años 70, había una revolución en marcha. La invención del microprocesador hizo posible que personas corrientes como tú y yo tuviéramos realmente un ordenador. Hoy en día a mucha gente les cuesta imaginar cómo era el mundo cuando solo las grandes empresas y el gran gobierno controlaban todos los ordenadores. Digamos que no pudiste hacer mucho.

Hoy, el mundo es muy diferente. Los ordenadores están por todas partes, desde pequeños relojes de pulsera hasta enormes centros de datos y todo lo que hay entre medias. Además de los ordenadores ubicuos, también contamos con una red ubicua que los conecta. Esto ha creado una nueva era maravillosa de empoderamiento personal y libertad creativa, pero en las últimas dos décadas ha estado ocurriendo algo más. Unas pocas grandes corporaciones han estado imponiendo su control sobre la mayoría de los ordenadores del mundo y decidiendo qué puedes o no puedes hacer con ellos. Por suerte, gente de todo el mundo está haciendo algo al respecto. Están luchando por mantener el control de sus ordenadores escribiendo su propio software. Están construyendo Linux.

Mucha gente habla de "libertad" en relación con Linux, pero no creo que la mayoría sepa lo que realmente significa esa libertad. La libertad es el poder de decidir qué hace tu ordenador, y la única forma de tener esa libertad es saber qué está haciendo tu ordenador. La libertad es un ordenador sin secretos, uno donde todo puede saberse si te importa lo suficiente como para descubrirlo.

### **¿Por qué usar la línea de comandos?**

¿Alguna vez te has fijado en las películas cuando el "superhacker"—ya sabes, el tipo que puede acceder al ordenador militar ultra-seguro en menos de 30 segundos—se sienta frente al ordenador y nunca toca un ratón? Es porque los cineastas se dan cuenta de que, como seres humanos, sabemos instintivamente que la única forma de hacer algo en un ordenador es escribiendo en un teclado.

La mayoría de los usuarios de ordenadores hoy en día solo conocen la _interfaz gráfica (__GUI_) y han sido enseñados por proveedores y expertos que la _interfaz de línea de comandos_ (_CLI_) es algo aterrador del pasado. Esto es lamentable porque una buena interfaz de línea de comandos es una forma maravillosamente expresiva de comunicarse con un ordenador, de forma muy similar a como lo es la palabra escrita para los seres humanos. Se ha dicho que "las interfaces gráficas hacen que las tareas fáciles sean fáciles, mientras que las interfaces de línea de comandos hacen posibles tareas difíciles", y esto sigue siendo muy cierto hoy en día.

Dado que Linux está modelado según la familia de sistemas operativos Unix, comparte la misma rica herencia de herramientas de línea de comandos que Unix. Unix ganó notoriedad a principios de los años 80 (aunque se desarrolló por primera vez una década antes), antes de la adopción generalizada de la interfaz gráfica de usuario y, como resultado, desarrolló una extensa interfaz de línea de comandos. De hecho, una de las razones más fuertes por las que los primeros adoptantes de Linux lo eligieron en lugar de, por ejemplo, Windows NT fue la potente interfaz de línea de comandos que hacía posibles las "tareas difíciles".

### **De qué trata este libro**

Este libro es una visión general amplia de "vivir" en la línea de comandos de Linux. A diferencia de algunos libros que se concentran en un solo programa, como el programa shell bash, este libro tratará de transmitir cómo llevarse bien con la interfaz de línea de comandos en un sentido más amplio. ¿Cómo funciona todo? ¿Qué puede hacer? ¿Cuál es la mejor manera de usarlo?

**Este no es un libro sobre administración de sistemas Linux.** Aunque cualquier discusión seria sobre la línea de comandos conducirá invariablemente a temas de administración de sistemas, este libro solo toca algunos temas de administración. Sin embargo, preparará al lector para estudios adicionales al proporcionar una base sólida en el uso de la línea de comandos, una herramienta esencial para cualquier tarea seria de administración de sistemas.

**Este libro se centra en Linux.** Muchos otros libros intentan ampliar su atractivo incluyendo otras plataformas como Unix genérico y macOS. Al hacerlo, "diluyen" su contenido para incluir solo temas generales. Este libro, por otro lado, cubre solo las distribuciones de Linux contemporáneas. El noventa y cinco por ciento del contenido es útil para usuarios de otros sistemas tipo Unix, pero este libro está altamente dirigido al usuario moderno de la línea de comandos de Linux.

### **¿Quién debería leer este libro?**

Este libro es para nuevos usuarios de Linux que han migrado de otras plataformas. Lo más probable es que seas un "usuario avanzado" de alguna versión de Microsoft Windows. Quizás tu jefe te haya dicho que administres un servidor Linux, o estás entrando en el emocionante nuevo mundo de los ordenadores de placa única (SBC) como el Raspberry Pi. Puede que seas simplemente un usuario de escritorio que está cansado de todos los problemas de seguridad y quiere darle una oportunidad a Linux. Eso está bien. Todos son bienvenidos aquí.

Dicho esto, no hay atajos para la iluminación de Linux. Aprender la línea de comandos es un desafío y requiere un esfuerzo real. No es que sea tan difícil, sino que es muy *vasto*. El sistema Linux promedio tiene literalmente *miles* de programas que puedes emplear en la línea de comandos. Considérate advertido; aprender la línea de comandos no es un esfuerzo casual.

Por otro lado, aprender la línea de comandos de Linux es extremadamente gratificante. Si crees que eres un "usuario avanzado" ahora, solo espera. No sabes lo que es el poder real, todavía. Y, a diferencia de muchas otras habilidades informáticas, el conocimiento de la línea de comandos es duradero. Las habilidades aprendidas hoy seguirán siendo útiles dentro de 10 años. La línea de comandos ha sobrevivido a la prueba del tiempo.

También se asume que no tienes experiencia en programación, pero no te preocupes, también te iniciaremos en ese camino.

### **¿Qué hay en este libro?**

Este material se presenta en una secuencia cuidadosamente elegida, muy parecida a la de un tutor sentado a tu lado guiándote. Muchos autores tratan este material de manera "sistemática", cubriendo exhaustivamente cada tema en orden. Esto tiene sentido desde la perspectiva de un escritor, pero puede ser muy confuso para los nuevos usuarios.

Otro objetivo es familiarizarte con la forma de pensar de Unix, que es diferente de la forma de pensar de Windows. En el camino, haremos algunos viajes laterales para ayudarte a comprender por qué ciertas cosas funcionan de la manera en que lo hacen y cómo llegaron a ser así. Linux no es solo una pieza de software; también es una pequeña parte de la cultura Unix más amplia, que tiene su propio lenguaje e historia. Puede que también lance una que otra queja.

Este libro se divide en cuatro partes, cada una cubriendo algún aspecto de la experiencia de la línea de comandos.

- **[Parte 1](https://learning.oreilly.com/library/view/the-linux-command/9781492071235/xhtml/part01.xhtml#part01), "Aprendiendo el Shell",** comienza nuestra exploración del lenguaje básico de la línea de comandos, incluyendo cosas como la estructura de los comandos, la navegación por el sistema de archivos, la edición de la línea de comandos y la búsqueda de ayuda y documentación para los comandos.
- **[Parte 2](https://learning.oreilly.com/library/view/the-linux-command/9781492071235/xhtml/part02.xhtml#part02), "Configuración y el Entorno",** cubre la edición de archivos de configuración que controlan el funcionamiento del ordenador desde la línea de comandos.
- **[Parte 3](https://learning.oreilly.com/library/view/the-linux-command/9781492071235/xhtml/part03.xhtml#part03), "Tareas Comunes y Herramientas Esenciales",** explora muchas de las tareas ordinarias que se realizan comúnmente desde la línea de comandos. Los sistemas operativos tipo Unix, como Linux, contienen muchos programas de línea de comandos "clásicos" que se utilizan para realizar potentes operaciones sobre los datos.
- **[Parte 4](https://learning.oreilly.com/library/view/the-linux-command/9781492071235/xhtml/part04.xhtml#part04), "Escritura de Shell Scripts",** presenta la programación de shell, una técnica admitidamente rudimentaria pero fácil de aprender para automatizar muchas tareas informáticas comunes. Al aprender la programación de shell, te familiarizarás con conceptos que se pueden aplicar a muchos otros lenguajes de programación.

### **Cómo leer este libro**

Comienza por el principio del libro y síguelo hasta el final. No está escrito como una obra de referencia; es realmente más como una historia con un principio, un nudo y un desenlace.

#### **_Prerrequisitos_**

Para usar este libro, todo lo que necesitarás es una instalación funcional de Linux. Puedes obtenerla de una de estas dos maneras:

**Instala Linux en un ordenador (no tan nuevo).** No importa qué distribución elijas, aunque la mayoría de la gente hoy en día comienza con Ubuntu, Fedora u OpenSUSE. En caso de duda, prueba primero con Ubuntu. Instalar una distribución moderna de Linux puede ser ridículamente fácil o ridículamente difícil dependiendo de tu hardware. Sugiero un ordenador de sobremesa que tenga un par de años y al menos 2 GB de RAM y 6 GB de espacio libre en el disco duro. Evita los portátiles y las redes inalámbricas si es posible, ya que a menudo son más difíciles de poner en marcha.

**Usa un "CD en vivo" o una unidad flash USB.** Una de las cosas geniales que puedes hacer con muchas distribuciones de Linux es ejecutarlas directamente desde un CD-ROM o una unidad flash USB sin instalarlas en absoluto. Simplemente entra en la configuración de la BIOS y configura tu ordenador para que arranque desde una unidad de CD-ROM o un dispositivo USB y reinicia. Usar este método es una excelente manera de probar la compatibilidad de Linux en un ordenador antes de la instalación. La desventaja es que puede ser lento en comparación con tener Linux instalado en tu disco duro. Tanto Ubuntu como Fedora (entre otros) tienen versiones en vivo.

Independientemente de cómo instales Linux, necesitarás tener privilegios ocasionales de superusuario (es decir, administrativos) para llevar a cabo las lecciones de este libro.

Después de tener una instalación funcional, comienza a leer y sigue los pasos con tu propio ordenador. La mayor parte del material de este libro es "práctico", ¡así que siéntate y empieza a escribir!

**POR QUÉ NO LO LLAMO "GNU/LINUX"**

En algunos círculos, es políticamente correcto llamar al sistema operativo Linux el "sistema operativo GNU/Linux". El problema con "Linux" es que no hay una forma completamente correcta de nombrarlo porque fue escrito por muchas personas diferentes en un vasto y distribuido esfuerzo de desarrollo. Técnicamente hablando, Linux es el nombre del núcleo (kernel) del sistema operativo, nada más. El núcleo es muy importante, por supuesto, ya que hace que el sistema operativo funcione, pero no es suficiente para formar un sistema operativo completo.

Entra Richard Stallman, el genio filósofo que fundó el movimiento del Software Libre, inició la Free Software Foundation, formó el Proyecto GNU, escribió la primera versión del compilador GNU C (gcc), creó la Licencia Pública General de GNU (la GPL), etc., etc., etc. Él *insiste* en que lo llames "GNU/Linux" para reflejar adecuadamente las contribuciones del Proyecto GNU. Si bien el Proyecto GNU es anterior al núcleo de Linux y las contribuciones del proyecto son extremadamente merecedoras de reconocimiento, colocarlas en el nombre es injusto para todos los demás que hicieron contribuciones significativas. Además, creo que "Linux/GNU" sería más preciso desde el punto de vista técnico, ya que el núcleo arranca primero y todo lo demás se ejecuta sobre él.

En el uso popular, Linux se refiere al núcleo y a todo el demás software libre y de código abierto que se encuentra en la distribución típica de Linux, es decir, todo el ecosistema de Linux, no solo los componentes GNU. El mercado de sistemas operativos parece preferir nombres de una sola palabra como DOS, Windows, macOS, Solaris, Irix y AIX. He optado por usar el formato popular. Sin embargo, si prefieres usar "GNU/Linux" en su lugar, por favor realiza una búsqueda mental y reemplazo mientras lees este libro. No me importará.

### **Novedades en la segunda edición**

Aunque la estructura básica y el contenido permanecen iguales, esta edición de _The Linux Command_ Line está salpicada de diversas mejoras, aclaraciones y modernizaciones, muchas de las cuales se basan en la opinión de los lectores. Además, destacan dos mejoras en particular. Primero, el libro ahora asume la versión 4 de la bash. _X_, que no estaba ampliamente utilizado en la época del manuscrito original. Esta cuarta versión importante de bash añadió varias características nuevas útiles que ahora se cubren en esta edición. En segundo lugar, [la Parte 4](https://learning.oreilly.com/library/view/the-linux-command/9781492071235/xhtml/part04.xhtml#part04), "[Shell Scripting](https://learning.oreilly.com/library/view/the-linux-command/9781492071235/xhtml/part04.xhtml#part04)", ha sido mejorada para ofrecer mejores ejemplos de buenas prácticas de scripting. Los scripts incluidos en [la Parte 4](https://learning.oreilly.com/library/view/the-linux-command/9781492071235/xhtml/part04.xhtml#part04) han sido revisados para hacerlos más completos, y también he corregido algunos errores ;-).

### **¡Necesitas tu opinión!**

Este libro es un proyecto en curso, como muchos proyectos de software de código abierto. Si encuentras un error técnico, escríbeme en _[bshotts@users.sourceforge.net](mailto:bshotts@users.sourceforge.net)_.

Asegúrate de indicar la edición exacta del libro que estás leyendo. Tus cambios y sugerencias pueden aparecer en futuras versiones.
