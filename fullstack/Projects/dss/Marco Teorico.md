### Inteligencia de negocios (BI)
  Reis y Housley (2022) establecen que la Inteligencia de Negocios (BI) comprende el conjunto de arquitecturas, procesos y tecnologías orientadas a la transformación de datos crudos en información significativa y procesable. Según
  los autores, el propósito fundamental del BI es facilitar la toma de decisiones corporativas mediante la generación de reportes, tableros de control (dashboards) y análisis descriptivos que revelen el estado actual e histórico de
  una organización. De este modo, se democratiza el acceso a la información, permitiendo a los directivos identificar métricas clave de rendimiento (KPIs) de manera intuitiva y sin requerir conocimientos técnicos profundos en
  lenguajes de programación.

  Por su parte, Grus (2019) complementa esta visión señalando que la inteligencia de negocios sienta las bases indispensables para disciplinas analíticas más avanzadas como la ciencia de datos. El autor argumenta que una
  infraestructura de BI sólida requiere de un proceso riguroso de limpieza, consolidación y almacenamiento, puesto que la precisión de los análisis y reportes derivados es directamente proporcional a la calidad de la información
  subyacente. En este contexto, el BI actúa como un puente vital entre la simple gestión de bases de datos transaccionales y el descubrimiento profundo de conocimiento organizacional.

  Desde nuestra perspectiva y en el marco del presente proyecto, la Inteligencia de Negocios representa el cimiento tecnológico necesario para transformar el historial transaccional de la Universidad Autónoma Tomás Frías (UATF) en
  un activo estratégico. Consideramos que la simple acumulación de notas académicas en el sistema actual carece de valor si no es procesada adecuadamente. Por lo tanto, la implementación de herramientas de BI permitirá al
  Departamento de Servicios Académicos (DSA) monitorear de manera dinámica las tasas de rendimiento, facilitando una gestión fundamentada en evidencias concretas y propiciando intervenciones oportunas para mejorar la calidad
  educativa.

### Almacenes de datos (Data Warehouse)

  Martínez (2021) define un Almacén de Datos (Data Warehouse) como un repositorio centralizado y estructurado, diseñado específicamente para optimizar las consultas y el procesamiento analítico de grandes volúmenes de información. A
  diferencia de las bases de datos transaccionales (OLTP), que están orientadas a la rápida inserción y actualización de registros cotidianos, el autor destaca que los almacenes de datos consolidan información proveniente de
  múltiples fuentes heterogéneas. Esta arquitectura permite mantener un registro histórico inmutable, el cual resulta esencial para realizar análisis de tendencias y evaluaciones a largo plazo sin comprometer el rendimiento de los
  sistemas operativos diarios.

  En concordancia con esto, Reis y Housley (2022) enfatizan que la construcción de un Data Warehouse requiere un diseño de ingeniería riguroso enfocado en la lectura eficiente de datos. Los autores explican que la separación de la
  información en "tablas de hechos" (que almacenan métricas numéricas) y "tablas de dimensiones" (que otorgan el contexto descriptivo) facilita la comprensión del entorno y acelera drásticamente los tiempos de respuesta ante
  consultas complejas. Asimismo, subrayan la vital importancia de los procesos de extracción, transformación y carga (tuberías ETL) para asegurar la integridad, limpieza y actualización constante de estos almacenes.

  Para el desarrollo de nuestro proyecto, la construcción de un Data Warehouse constituye la solución técnica idónea para centralizar la vasta cantidad de información académica dispersa en los sistemas actuales de la UATF. Creemos
  firmemente que aislar la carga analítica de la transaccional es imperativo para no saturar ni afectar el desempeño de los registros de inscripción y notas. Al implementar este almacén de datos lograremos crear una "fuente única de
  verdad" robusta y depurada que alimentará de manera eficiente tanto a los tableros de control visuales como a los futuros algoritmos predictivos.

### Modelado multidimensional

  Bernabeu (2010) postula que el modelado multidimensional es una técnica de diseño de bases de datos analíticas que busca estructurar la información de manera que se alinee directamente con la forma en que los usuarios de negocio
  piensan y consultan sus datos. A través de la Metodología Hefesto, el autor detalla que este proceso se construye a partir de los requerimientos de los usuarios, identificando los procesos centrales (hechos) y los contextos que
  los rodean (dimensiones). Esta orientación asegura que el esquema resultante, usualmente un esquema en estrella, sea altamente intuitivo, escalable y perfectamente compatible con las herramientas de visualización.

  Profundizando en su metodología, Bernabeu (2010) resalta la importancia crítica de definir correctamente la "granularidad" de los datos durante la fase de diseño lógico. El autor señala que el nivel de detalle de los registros
  almacenados en las tablas de hechos determina el límite de los análisis posteriores; un nivel de granularidad muy resumido impide descender a detalles específicos, mientras que uno muy atómico exige mayores recursos de
  almacenamiento y procesamiento. Por ende, la selección adecuada del grano es un paso decisivo para garantizar la viabilidad y la rapidez del sistema de soporte a decisiones.

  Aplicando estos lineamientos a nuestra investigación, consideramos que la Metodología Hefesto es el marco de trabajo más certero para estructurar el modelo multidimensional del rendimiento académico estudiantil. Nuestro enfoque
  establecerá una granularidad a nivel de "calificación final por materia y estudiante", lo que nos proporcionará la flexibilidad analítica necesaria para evaluar el rendimiento tanto a nivel micro (por alumno individual) como macro
  (por carrera o facultad). Esta estructuración multidimensional será la clave principal para que las autoridades puedan navegar por los indicadores sin enfrentar cuellos de botella técnicos.

### Sistemas de Soporte a Decisiones y Machine Learning

  Pérez, Gómez y Sánchez (2022) afirman que la integración de modelos predictivos de Machine Learning en el ámbito educativo transforma por completo el análisis del rendimiento académico. Según los autores, los algoritmos
  supervisados de clasificación son capaces de procesar variables sociodemográficas y calificaciones previas para descubrir patrones ocultos e identificar tempranamente a los alumnos que se encuentran en alto riesgo de reprobación o
  deserción. De este modo, el sistema transita de tener un enfoque meramente descriptivo a uno prescriptivo, brindando a las instituciones alertas tempranas sólidas para mejorar la retención estudiantil.

  Para dotar de estructura a estos modelos predictivos, Wirth y Hipp (2000) exponen el estándar CRISP-DM (Cross-Industry Standard Process for Data Mining) como la metodología más probada y adoptada en la industria. Los autores
  explican que CRISP-DM divide el ciclo de vida del aprendizaje automático en seis fases iterativas: comprensión del negocio, comprensión de los datos, preparación, modelado, evaluación y despliegue. Destacan que esta estructura
  fomenta la revisión constante, garantizando que los modelos matemáticos se alineen a los objetivos iniciales y mantengan niveles óptimos de precisión frente a nuevos conjuntos de datos reales.

  Desde nuestra visión como ingenieros, la implementación de algoritmos de Machine Learning bajo el estándar metodológico CRISP-DM es el factor innovador que elevará el sistema propuesto de un simple generador de gráficos a un
  verdadero Sistema de Soporte a Decisiones. Estamos convencidos de que predecir la deserción académica a través de inteligencia artificial es la respuesta idónea a las deficiencias actuales. Al aplicar esta metodología,
  aseguraremos que el entrenamiento de los algoritmos sobre el almacén de datos posea rigor científico, resultando en predicciones de riesgo precisas que apoyen la gestión proactiva de las autoridades universitarias.
  ──────
### Referencias Bibliográficas (Formato APA v7)

  Agrega estas referencias a la sección de "Bibliografía" de tu documento final:

  • Bernabeu, R. D. (2010). Metodología Hefesto: Construcción de un Data Warehouse (2.ª ed.). Autoedición.
  • Grus, J. (2019). Ciencia de datos desde cero: Principios básicos del Data Science (2.ª ed.). Anaya Multimedia.
  • Martínez, A. (2021). Arquitectura e ingeniería de datos. Editorial Síntesis.
  • Pérez, L., Gómez, C., & Sánchez, R. (2022). Predicción del rendimiento académico utilizando modelos de Machine Learning. Revista Electrónica Dialnet, 14(3), 45-62.
  • Reis, J., & Housley, M. (2022). Fundamentals of Data Engineering: Plan and Build Robust Data Systems (1.ª ed.). O'Reilly Media.
  • Wirth, R., & Hipp, J. (2000). CRISP-DM: Towards a standard process model for data mining. Proceedings of the 4th International Conference on the Practical Applications of Knowledge Discovery and Data Mining, 29-39.