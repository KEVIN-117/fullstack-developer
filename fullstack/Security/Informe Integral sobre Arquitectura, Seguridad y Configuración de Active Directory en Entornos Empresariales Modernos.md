---
sticker: lucide//file-text
banner: assets/ether-bg.jpeg
---
## **Introducción: La Columna Vertebral de la Identidad Empresarial**

En el panorama actual de la infraestructura tecnológica, los Servicios de Dominio de Active Directory (AD DS) de Microsoft se han consolidado como el estándar de facto para la gestión de identidades y accesos en entornos corporativos. Según reportes recientes, más del 90% de las empresas del Fortune 1000 dependen de esta tecnología para orquestar la autenticación de usuarios y la autorización de recursos.1 Active Directory no debe conceptualizarse meramente como una base de datos de usuarios o un directorio telefónico digital; en su lugar, funciona como un sistema operativo distribuido y jerárquico que gestiona las políticas de seguridad, la replicación de datos críticos y la interconexión lógica de los activos de una organización.2

La relevancia de Active Directory radica en su capacidad para proporcionar una gestión centralizada. Permite a los administradores de TI organizar elementos de red —usuarios, computadoras, grupos, impresoras y recursos compartidos— en una estructura de contención jerárquica que trasciende la topología física de la red.3 Sin embargo, esta centralización también introduce un riesgo sistémico significativo: el compromiso de Active Directory equivale, en la práctica, al compromiso total de la infraestructura de TI de una organización. La evolución de las amenazas cibernéticas ha transformado a AD en el objetivo principal de los atacantes, quienes explotan configuraciones heredadas, protocolos de autenticación obsoletos como NTLM y permisos delegados incorrectamente para escalar privilegios y exfiltrar datos sensibles.4

Este informe técnico exhaustivo aborda la naturaleza multifacética de Active Directory, diseccionando su arquitectura lógica y física, analizando en profundidad los mecanismos de autenticación —con un enfoque especial en la dicotomía NTLM versus Kerberos— y exponiendo las configuraciones peligrosas que prevalecen en los entornos de producción. Además, se presentan estrategias de mitigación y endurecimiento (hardening) basadas en las mejores prácticas de seguridad para 2025, incluyendo el modelo de niveles administrativos y la transición hacia una arquitectura de confianza cero (Zero Trust).4

---

# **Capítulo 1: Arquitectura y Modelado de Active Directory**

Para asegurar y configurar Active Directory, es imperativo comprender primero su diseño subyacente. AD opera bajo dos modelos distintos pero interconectados: el modelo lógico, que define la organización de los recursos y las políticas de seguridad, y el modelo físico, que gestiona la optimización del tráfico de red y la replicación de datos.3

### **1.1 El Modelo Lógico: Estructura y Jerarquía**

El modelo lógico permite a las organizaciones estructurar sus recursos de manera que reflejen su organigrama o necesidades administrativas, independientemente de la ubicación geográfica de los activos.

#### **El Bosque (Forest)**

En la cúspide de la jerarquía se encuentra el Bosque. Un bosque representa el límite de seguridad definitivo de una instancia de Active Directory. Todos los objetos dentro de un bosque comparten un esquema de directorio común, una configuración global y un Catálogo Global (GC).3

- **Implicaciones de Seguridad:** Es fundamental entender que el bosque, y no el dominio, es el límite de seguridad. Un administrador con privilegios elevados en un dominio secundario dentro de un bosque puede, teóricamente, comprometer la seguridad de todo el bosque si existen relaciones de confianza predeterminadas. Por ello, el aislamiento de seguridad real requiere la implementación de bosques separados.7

#### **El Dominio (Domain)**

El dominio actúa como una partición administrativa y de replicación dentro del bosque. Funciona como un límite para las políticas de gestión, como las políticas de contraseñas, bloqueo de cuentas y tickets Kerberos.

- **Identidad de Red:** Los dominios permiten crear identidades de usuario únicas que pueden ser referenciadas en cualquier máquina unida al bosque. Los Controladores de Dominio (DC) dentro de un dominio almacenan una réplica completa de todos los objetos de ese dominio, pero solo una réplica parcial de objetos de otros dominios (a través del Catálogo Global).3
- **Relaciones de Confianza:** Los dominios dentro de un mismo bosque están conectados automáticamente por relaciones de confianza transitivas y bidireccionales, formando un Árbol de Dominio. Esto permite que un usuario en el dominio ventas.corp.local acceda a recursos en ingenieria.corp.local sin re-autenticación, asumiendo que los permisos lo permitan.2

#### **Unidades Organizativas (OUs)**

Las OUs son contenedores dentro de un dominio que proporcionan granularidad administrativa. Son esenciales para la delegación de control y la aplicación de Objetos de Política de Grupo (GPO).3

- **Estrategia de Delegación:** Las OUs permiten implementar el principio de menor privilegio. En lugar de otorgar derechos de "Admin del Dominio" a todo el personal de TI, se pueden delegar permisos específicos (como restablecer contraseñas o unir computadoras al dominio) sobre una OU específica a un grupo de soporte técnico.7

### **1.2 El Modelo Físico: Topología y Replicación**

Mientras el modelo lógico organiza, el modelo físico optimiza. Active Directory utiliza el concepto de "Sitios" para gestionar el tráfico de replicación y autenticación en redes geográficamente dispersas.8

#### **Sitios y Subredes**

Un Sitio en AD se define como una colección de subredes IP con conectividad rápida y confiable (generalmente LAN).

- **Optimización de Autenticación:** Los sitios aseguran que los clientes localicen y se autentiquen con el Controlador de Dominio más cercano, minimizando la latencia y el tráfico a través de enlaces WAN costosos o lentos.8
- **Control de Replicación:** La replicación dentro de un sitio (intra-site) ocurre casi en tiempo real y sin compresión para maximizar la velocidad. La replicación entre sitios (inter-site) se comprime y se puede programar para ocurrir en horarios de bajo tráfico, optimizando el ancho de banda.6

#### **Controladores de Dominio (Domain Controllers)**

El DC es el servidor que aloja la base de datos NTDS.DIT y el recurso compartido SYSVOL. Es el corazón operativo de AD.

- **Almacén de Datos:** Los DCs almacenan la información de identidad, incluyendo los hashes de contraseñas de los usuarios y las claves criptográficas de los servicios.
- **Catálogo Global (GC):** Un DC designado como GC almacena una copia completa de todos los objetos de su dominio y una copia parcial de solo lectura de todos los objetos de otros dominios en el bosque. Esto es crucial para búsquedas universales y la validación de pertenencia a grupos universales durante el inicio de sesión.3

### **1.3 La Base de Datos y Particiones**

Active Directory utiliza una base de datos basada en el motor Jet (Blue) llamada NTDS.DIT. Esta base de datos se divide lógicamente en particiones o "Naming Contexts" (NC), cada una con diferentes reglas de replicación:

1. **Partición de Esquema:** Define las clases de objetos y atributos que se pueden crear. Se replica a todos los DCs del bosque.
2. **Partición de Configuración:** Contiene la topología de replicación y configuración de sitios. Se replica a todos los DCs del bosque.
3. **Partición de Dominio:** Contiene los objetos reales (usuarios, computadoras). Se replica solo a los DCs dentro del mismo dominio.
4. **Partición de Aplicación:** Utilizada por aplicaciones como DNS integrado en AD para controlar el alcance de la replicación de datos específicos.3

---

# **Capítulo 2: Despliegue y Configuración de Active Directory**

La configuración inicial de Active Directory establece la línea base de seguridad y funcionalidad para toda la vida útil del entorno. Un diseño deficiente en esta etapa puede introducir vulnerabilidades difíciles de remediar posteriormente.

### **2.1 Proceso de Instalación y Promoción**

La instalación de AD DS transforma un servidor miembro en un Controlador de Dominio. En Windows Server 2025 (y versiones anteriores recientes), este proceso implica la instalación de los binarios del rol y la posterior "promoción" del servidor.9

#### **Requisitos Previos Críticos**

- **Direccionamiento IP Estático:** Los DCs son infraestructuras críticas que deben tener direcciones IP fijas para garantizar la resolución DNS confiable.10
- **DNS:** Active Directory y DNS están indisolublemente ligados. AD utiliza registros SRV en DNS para que los clientes localicen servicios como Kerberos (\_kerberos.\_tcp) y LDAP (\_ldap.\_tcp). Una configuración DNS incorrecta es la causa principal de fallos en AD.7

#### **Métodos de Despliegue**

- **Server Manager (GUI):** A través del asistente gráfico, se selecciona el rol AD DS y se configura el nuevo bosque o dominio. Es propenso a errores humanos si no se siguen guías estrictas.10
- **PowerShell:** El uso de cmdlets como Install-ADDSForest permite despliegues automatizados, repetibles y menos propensos a errores. Ejemplo de automatización:  
  PowerShell  
  Install-ADDSForest \-DomainName "corp.empresa.com" \-DomainNetbiosName "CORP" \-DomainMode WinThreshold \-ForestMode WinThreshold \-InstallDns:$true

  Este método es preferible para garantizar la consistencia en entornos grandes o de recuperación ante desastres.10

### **2.2 Niveles Funcionales del Bosque y Dominio**

Los niveles funcionales determinan las capacidades disponibles de AD y los sistemas operativos Windows Server que pueden operar como Controladores de Dominio.

- **Evolución:** Con Windows Server 2025, se introducen nuevos niveles funcionales que soportan características avanzadas de seguridad y tamaños de página de base de datos optimizados (32k páginas). Mantener niveles funcionales antiguos (como 2008 R2) para compatibilidad con servidores legados impide la adopción de mejoras de seguridad modernas como la protección contra la reproducción de Kerberos o el soporte para grupos de seguridad protegidos.5

### **2.3 Diseño del Espacio de Nombres y DNS**

La elección del nombre de dominio raíz es una decisión crítica.

- **Prácticas Recomendadas:** Se aconseja utilizar un subdominio de un dominio público registrado (ej. ad.empresa.com) en lugar de dominios inventados no enrutables como .local o .internal. Esto facilita la gestión de certificados SSL/TLS públicos y evita colisiones de nombres con estándares futuros (como mDNS que usa .local).10
- **Nombre NetBIOS:** Aunque es un remanente heredado, el nombre NetBIOS debe ser único y corto (máximo 15 caracteres) para asegurar compatibilidad con sistemas antiguos que aún dependen de la resolución WINS o broadcasts.10

---

# **Capítulo 3: Mecanismos de Autenticación \- Un Análisis Profundo**

La función primordial de Active Directory es la autenticación: verificar que una entidad es quien dice ser. Históricamente, Microsoft ha soportado dos familias de protocolos: NTLM (NT LAN Manager) y Kerberos. Comprender la mecánica interna de estos protocolos es vital para identificar vulnerabilidades y configurar defensas efectivas.

### **3.1 NTLM: El Legado Persistente e Inseguro**

NTLM es un protocolo de autenticación de desafío-respuesta que no depende de un tercero de confianza en tiempo real para la emisión de tickets, sino que valida las credenciales directamente con el servidor o pasando la solicitud al DC (Pass-through Authentication).12

#### **Flujo de Autenticación NTLM**

1. **Negociación (Negotiate):** El cliente envía una solicitud al servidor indicando las capacidades que soporta (cifrado, versión).
2. **Desafío (Challenge):** El servidor responde con un número aleatorio de 16 bytes llamado "Nonce" o desafío del servidor.
3. **Respuesta (Authenticate):** El cliente cifra este desafío utilizando un hash derivado de su contraseña (hash NTLM) y envía el resultado (la respuesta) al servidor.
4. **Validación:**
   - Si es una cuenta local, el servidor valida la respuesta comparándola con el hash almacenado en su SAM local.
   - Si es una cuenta de dominio, el servidor reenvía el desafío, la respuesta y el nombre de usuario al Controlador de Dominio a través del servicio Netlogon. El DC verifica la respuesta y comunica el resultado al servidor.14

#### **Variantes y Debilidades de NTLM**

- **NTLMv1:** Utiliza el algoritmo de cifrado DES, que es extremadamente débil. Un atacante que capture una respuesta NTLMv1 puede descifrarla en segundos utilizando tablas Rainbow o fuerza bruta moderna, revelando el hash NTLM del usuario.15
- **NTLMv2:** Introduce HMAC-MD5 y desafíos de cliente para mitigar ataques de predicción, pero sigue siendo vulnerable a la captura y retransmisión (Relay) y al craqueo offline si la contraseña es débil.14

**Peligros Inherentes de NTLM:**

- **Falta de Autenticación Mutua:** El cliente no verifica la identidad del servidor. Esto permite que un atacante monte un servidor falso e intercepte las credenciales.12
- **Pass-the-Hash:** Dado que el servidor no requiere la contraseña en texto plano, sino solo la prueba de que el cliente posee el hash, un atacante que robe el hash NTLM (de la memoria LSASS de una máquina comprometida) puede autenticarse como ese usuario sin conocer la contraseña.4

### **3.2 Kerberos: El Estándar de Seguridad Empresarial**

Kerberos es el protocolo predeterminado desde Windows 2000\. Se basa en un modelo de confianza de terceros utilizando criptografía de clave simétrica y un sistema de tickets para evitar la transmisión de contraseñas por la red.12

#### **Componentes Clave de Kerberos**

- **KDC (Key Distribution Center):** Reside en el DC y consta del Servicio de Autenticación (AS) y el Servicio de Concesión de Tickets (TGS).
- **TGT (Ticket Granting Ticket):** Ticket maestro que prueba la identidad del usuario.
- **TGS (Service Ticket):** Ticket específico para acceder a un recurso (ej. CIFS, SQL).
- **PAC (Privilege Attribute Certificate):** Estructura dentro del ticket que contiene los SIDs del usuario y grupos, determinando sus privilegios.17

#### **Análisis Detallado del Flujo Kerberos**

El proceso de autenticación completa implica varios intercambios de mensajes:

1. **KRB_AS_REQ (Autenticación Inicial):**
   - El usuario solicita un TGT al KDC.
   - Para prevenir ataques de reproducción, el usuario cifra una marca de tiempo actual con su hash de contraseña (Pre-autenticación).
   - _Nota de Seguridad:_ Si la pre-autenticación está deshabilitada, un atacante puede solicitar un TGT para cualquier usuario y tratar de romperlo offline (AS-REP Roasting).19
2. **KRB_AS_REP (Emisión del TGT):**
   - El KDC valida la marca de tiempo. Si es correcta, genera un TGT que contiene la identidad del usuario y el PAC.
   - **Punto Crítico:** El TGT se cifra con el hash de la cuenta KRBTGT. Solo el KDC puede descifrar y validar este ticket. Si un atacante roba el hash KRBTGT, puede forjar TGTs válidos para cualquier usuario (Golden Ticket).20
   - El KDC también envía una Clave de Sesión, cifrada con el hash del usuario, para que este pueda comunicarse con el TGS posteriormente.
3. **KRB_TGS_REQ (Solicitud de Servicio):**
   - El usuario presenta su TGT al KDC y solicita acceso a un servicio específico (identificado por su SPN, Service Principal Name).
   - El usuario envía un "Authenticator" cifrado con la Clave de Sesión para probar que es el dueño legítimo del TGT.21
4. **KRB_TGS_REP (Emisión del Ticket de Servicio):**
   - El KDC valida el TGT.
   - Genera un Ticket de Servicio (Service Ticket) que contiene el PAC del usuario.
   - **Punto Crítico:** Este ticket se cifra con el hash de la cuenta de servicio (ej. la cuenta de máquina del servidor de archivos). Si esta cuenta tiene una contraseña débil, un atacante puede solicitar el ticket, llevarlo offline y romperlo (Kerberoasting).22
5. **KRB_AP_REQ (Acceso al Recurso):**
   - El usuario presenta el Ticket de Servicio al servidor de aplicaciones.
   - El servidor descifra el ticket (usando su propio hash), extrae el PAC y determina si el usuario tiene permisos de acceso.

**Comparativa Técnica: NTLM vs. Kerberos**

| Característica              | NTLM                                       | Kerberos                                         |
| :-------------------------- | :----------------------------------------- | :----------------------------------------------- |
| **Mecanismo**               | Desafío-Respuesta (3 vías)                 | Basado en Tickets y Tercero de Confianza (KDC)   |
| **Criptografía**            | Simétrica (DES/RC4/MD5) \- Débil           | Simétrica (AES) y Asimétrica (PKINIT) \- Fuerte  |
| **Autenticación Mutua**     | No (Solo Cliente a Servidor)               | Sí (Cliente y Servidor se verifican mutuamente)  |
| **Gestión de Credenciales** | Hash enviado (vulnerable a Relay)          | Tickets (TGT/ST) expiran y están firmados        |
| **Velocidad**               | Lento (requiere validación DC por intento) | Rápido (TGT permite SSO sin re-validar password) |
| **Uso de Puertos**          | Aleatorios (RPC), 445 (SMB)                | Estandarizado (Puerto 88 UDP/TCP)                |
| **Dependencia**             | Requiere conectividad IP directa           | Requiere DNS y Sincronización de Tiempo (NTP)    |

---

# **Capítulo 4: Peligros en la Configuración y Vectores de Ataque**

La complejidad de Active Directory, combinada con configuraciones predeterminadas orientadas a la compatibilidad, crea una superficie de ataque extensa. Los atacantes modernos no suelen explotar vulnerabilidades de software (exploits), sino debilidades en la configuración y la arquitectura.

### **4.1 Ataques a la Identidad y Credenciales**

#### **Kerberoasting**

Este ataque explota la arquitectura de Kerberos. Cualquier usuario autenticado puede solicitar un Ticket de Servicio (TGS) para cualquier servicio con un SPN registrado.

- **Mecánica:** El atacante solicita un ticket para un servicio (ej. MSSQLSvc). AD devuelve el ticket cifrado con el hash NTLM de la cuenta de servicio. El atacante guarda el ticket y usa herramientas como Hashcat para adivinar la contraseña offline.
- **Vulnerabilidad:** Cuentas de servicio con contraseñas débiles o antiguas son triviales de comprometer. Una vez obtenida la contraseña, el atacante puede acceder al servicio o escalar privilegios si la cuenta es administrador local.22

#### **AS-REP Roasting**

- **Mecánica:** Si la "Pre-autenticación Kerberos" está deshabilitada en una cuenta de usuario, el KDC devolverá un AS-REP cifrado con el hash del usuario ante cualquier solicitud, sin verificar primero la identidad.
- **Peligro:** Permite a un atacante obtener hashes de contraseñas de usuarios específicos sin enviar ningún paquete al usuario, siendo completamente silencioso y permitiendo ataques de fuerza bruta offline.19

#### **DCSync (Abuso de Replicación)**

- **Mecánica:** El protocolo MS-DRSR permite a los DCs sincronizar datos. Un atacante con los permisos extendidos DS-Replication-Get-Changes y DS-Replication-Get-Changes-All puede simular ser un DC y solicitar al DC real que replique los datos sensibles, incluyendo el hash de la contraseña de cualquier usuario (incluido el KRBTGT o Administradores).26
- **Detección:** Este ataque es difícil de detectar porque utiliza tráfico legítimo de replicación. Se debe monitorear el Event ID 4662 con acceso a los GUIDs específicos de replicación.29

### **4.2 Ataques de Falsificación de Tickets**

#### **Golden Ticket (Ticket Dorado)**

Considerado el "Game Over" en AD. Si un atacante obtiene el hash NTLM de la cuenta KRBTGT (generalmente vía DCSync), puede forjar sus propios TGTs.

- **Impacto:** El atacante puede crear un TGT válido para un usuario inexistente, otorgarle membresía en el grupo "Domain Admins" manipulando el PAC, y establecer una validez de 10 años. Esto permite persistencia total e indetectable en el dominio, ya que el TGT es matemáticamente válido.20
- **Defensa:** Requiere rotar la contraseña de la cuenta KRBTGT dos veces consecutivas para invalidar todos los tickets existentes.31

#### **Silver Ticket (Ticket Plateado)**

A diferencia del Golden Ticket, el Silver Ticket falsifica un Ticket de Servicio (TGS).

- **Mecánica:** Si un atacante obtiene el hash de una cuenta de servicio (ej. servidor de archivos), puede forjar un TGS para acceder a ese servicio con privilegios administrativos.
- **Peligro Oculto:** El Silver Ticket no interactúa con el KDC; se presenta directamente al servidor de aplicaciones. Por lo tanto, no deja rastros en los logs del Controlador de Dominio, lo que lo hace extremadamente sigiloso.32

#### **Diamond Ticket**

Una evolución del Golden Ticket. En lugar de forjar un ticket desde cero, el atacante intercepta un TGT legítimo, lo descifra con el hash KRBTGT, modifica el PAC para escalar privilegios y lo vuelve a cifrar.

- **Ventaja para el Atacante:** El ticket parece más legítimo porque se basa en una solicitud real, eludiendo algunas detecciones modernas que buscan TGTs completamente sintéticos.17

### **4.3 Configuraciones Peligrosas Comunes**

1. **Delegación Sin Restricciones (Unconstrained Delegation):**
   - Si un servidor está configurado con delegación sin restricciones, cuando un usuario se conecta a él, el DC envía una copia del TGT del usuario al servidor para que este lo use posteriormente.
   - **Riesgo:** Si un atacante compromete este servidor, puede volcar la memoria y robar los TGTs de cualquier usuario que se haya conectado, incluidos Administradores de Dominio, permitiendo la suplantación de identidad completa.21
2. **Cifrado Débil (RC4):**
   - Mantener habilitado RC4 para Kerberos permite a los atacantes romper tickets interceptados mucho más rápido que con AES. Microsoft está eliminando activamente este soporte en Windows 11 y Server 2025, pero muchos entornos antiguos lo mantienen habilitado.25
3. **Active Directory Certificate Services (AD CS) Mal Configurados:**
   - Plantillas de certificados que permiten a los usuarios especificar el "Subject Alternative Name" (SAN) en la solicitud.
   - **Riesgo (ESC1):** Un usuario normal puede solicitar un certificado para sí mismo pero especificar en el SAN que es el "Administrador". AD aceptará este certificado para la autenticación, otorgando acceso administrativo total.4

---

# **Capítulo 5: Estrategias de Defensa y Hardening para 2025**

Frente a este panorama de amenazas, la defensa de Active Directory no puede ser reactiva. Requiere una reingeniería basada en principios de Confianza Cero y aislamiento de privilegios.

### **5.1 Modelo de Niveles Administrativos (Tiering Model)**

El modelo de niveles es la estrategia defensiva más eficaz para prevenir el movimiento lateral y la escalada de privilegios. Divide el directorio en zonas de seguridad estancas.36

| Nivel (Tier) | Definición y Alcance                                                                                                                                | Restricciones de Acceso (GPO)                                                                                                                                                                      |
| :----------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tier 0**   | **Identidad y Control Total.** Incluye Controladores de Dominio, PKI (AD CS), ADFS, Azure AD Connect y cuentas de Administrador de Dominio/Empresa. | Los administradores T0 solo pueden iniciar sesión en activos T0. Se les **niega** el inicio de sesión en servidores T1 y estaciones T2 para evitar exponer sus credenciales en máquinas inseguras. |
| **Tier 1**   | **Servidores de Aplicación.** Incluye servidores miembros, bases de datos (SQL), Exchange, servidores de archivos y aplicaciones empresariales.     | Los administradores T1 gestionan servidores pero no pueden acceder a DCs ni iniciar sesión en estaciones de trabajo de usuarios finales.                                                           |
| **Tier 2**   | **Estaciones de Trabajo.** Incluye PCs de escritorio, portátiles, dispositivos móviles e impresoras.                                                | Los administradores T2 (soporte técnico) tienen derechos sobre las estaciones de trabajo pero no pueden acceder a servidores ni DCs.                                                               |

Implementación Técnica:  
Se utilizan GPOs para imponer restricciones de inicio de sesión (User Rights Assignment). Específicamente, se configuran las políticas "Deny log on locally", "Deny log on as a service" y "Deny log on through Remote Desktop Services" para asegurar que las credenciales de un nivel superior nunca se almacenen en la memoria de un nivel inferior.36

### **5.2 Estaciones de Trabajo de Acceso Privilegiado (PAW)**

Es inaceptable que un administrador gestione el directorio desde la misma máquina que utiliza para leer correo electrónico y navegar por internet, actividades que son vectores comunes de phishing y malware.

- **Concepto:** Una PAW es una estación de trabajo dedicada, endurecida y aislada, utilizada exclusivamente para tareas administrativas de Tier 0\. No tiene acceso directo a internet ni correo corporativo.
- **Separación:** El administrador utiliza una cuenta estándar en su PC normal para tareas de oficina y una cuenta administrativa dedicada en la PAW para gestionar AD.37

### **5.3 Transición y Eliminación de Protocolos Obsoletos**

#### **Erradicación de NTLM**

Microsoft ha señalado el fin de NTLM en Windows 11 y Server 2025\. La estrategia de transición segura implica:

1. **Auditoría:** Habilitar la política Network security: Restrict NTLM: Audit NTLM authentication in this domain para generar eventos (Event ID 8001, 8002, 8003, 8004\) que identifiquen aplicaciones dependientes de NTLM.39
2. **Restricción Progresiva:** Configurar Network security: LAN Manager authentication level a "Send NTLMv2 response only. Refuse LM & NTLM".
3. **Bloqueo:** Una vez remediadas las aplicaciones, establecer la política Restrict NTLM: Outgoing NTLM traffic to remote servers a "Deny All".23

#### **Firma de Protocolos (SMB y LDAP)**

Para mitigar ataques de Relay (ntlmrelayx), es crucial forzar la firma digital de paquetes.

- **SMB Signing:** Debe habilitarse en todos los servidores y clientes. Previene que un atacante modifique o retransmita paquetes SMB.
- **LDAP Signing y Channel Binding:** Configurar Domain controller: LDAP server signing requirements a "Require signing" previene ataques de retransmisión LDAP que podrían permitir cambios en el directorio o la creación de objetos maliciosos.4

### **5.4 Gestión Moderna de Cuentas**

- **LAPS (Local Administrator Password Solution):** Automatiza la gestión de contraseñas de administradores locales en estaciones de trabajo y servidores, asegurando que cada máquina tenga una contraseña única y rotada aleatoriamente, eliminando el movimiento lateral vía hash local.4
- **gMSA (Group Managed Service Accounts):** Reemplazan las cuentas de servicio tradicionales. AD gestiona automáticamente la complejidad y rotación de sus contraseñas (cada 30 días por defecto, con 120 caracteres de entropía), mitigando eficazmente el riesgo de Kerberoasting.4
- **dMSA (Delegated MSA):** Una novedad en Server 2025 que permite vincular cuentas de servicio gestionadas a máquinas específicas, restringiendo aún más su uso y previniendo el robo de credenciales para uso en otras máquinas.5

### **5.5 Monitoreo y Detección de Amenazas**

La implementación de un SIEM (Security Information and Event Management) es esencial para correlacionar eventos y detectar patrones de ataque. A continuación, se detallan los Event IDs críticos que deben monitorearse 22:

| Vector de Ataque            | Event ID Clave         | Lógica de Detección                                                                                                                                        |
| :-------------------------- | :--------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Fuerza Bruta / Spraying** | **4625**               | Picos repentinos de fallos de autenticación desde una misma IP o hacia un mismo usuario.                                                                   |
| **AS-REP Roasting**         | **4768**               | Solicitudes de TGT donde el campo PreAuthType es 0 (sin pre-autenticación) o código de resultado 0x0.                                                      |
| **Kerberoasting**           | **4769**               | Solicitudes excesivas de Tickets de Servicio (TGS) para múltiples servicios distintos en un corto periodo, especialmente con cifrado RC4 (0x17).           |
| **DCSync**                  | **4662**               | Acceso a objetos con GUIDs de replicación (1131f6aa... o 1131f6ad...) por cuentas que no son Controladores de Dominio.                                     |
| **Golden Ticket**           | **4624 (Tipo 3\)**     | Inicios de sesión con privilegios administrativos donde no existe un evento 4768 (solicitud TGT) correspondiente en los logs del KDC (indica TGT forjado). |
| **Modificación de Grupos**  | **4728 / 4732 / 4756** | Adición de usuarios a grupos privilegiados como "Domain Admins", "Enterprise Admins" o "Schema Admins".                                                    |
| **Limpieza de Logs**        | **1102**               | El borrado de los logs de auditoría es un indicador casi seguro de actividad maliciosa post-compromiso.                                                    |

---

**Conclusión y Perspectivas Futuras**

Active Directory sigue siendo el sistema nervioso central de la infraestructura de TI global. Su longevidad es testimonio de su utilidad, pero su arquitectura heredada representa un riesgo existencial si no se gestiona con una mentalidad de seguridad moderna.

El análisis realizado en este informe subraya que la seguridad de AD en 2025 no se trata simplemente de aplicar parches, sino de una reestructuración arquitectónica. La adopción del modelo de niveles (Tiering), la eliminación despiadada de protocolos inseguros como NTLMv1 y RC4, y la implementación de controles estrictos sobre la delegación y las cuentas de servicio son pasos no negociables.

Hacia el futuro, la integración con la nube (Microsoft Entra ID, anteriormente Azure AD) y las características de Windows Server 2025, como dMSA y la seguridad mejorada de Kerberos, ofrecen nuevas herramientas para la defensa. Sin embargo, la premisa fundamental permanece: **la identidad es el nuevo perímetro**. Proteger Active Directory requiere vigilancia constante, auditoría profunda y una comprensión técnica exhaustiva de los mecanismos que, en silencio, autentican cada acceso en la red corporativa.

#### **Fuentes citadas**

1. Active Directory Setup Guide: Key Steps for 2025 \- Cayosoft, acceso: diciembre 17, 2025, [https://www.cayosoft.com/blog/active-directory-setup/](https://www.cayosoft.com/blog/active-directory-setup/)
2. Active Directory Series: Active Directory Fundamentals \- Cobalt, acceso: diciembre 17, 2025, [https://www.cobalt.io/blog/active-directory-series-active-directory-fundamentals](https://www.cobalt.io/blog/active-directory-series-active-directory-fundamentals)
3. Understanding the Active Directory Logical Model | Microsoft Learn, acceso: diciembre 17, 2025, [https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/understanding-the-active-directory-logical-model](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/understanding-the-active-directory-logical-model)
4. Active Directory security best practices for 2025 \- Specops Software, acceso: diciembre 17, 2025, [https://specopssoft.com/blog/active-directory-security-best-practices/](https://specopssoft.com/blog/active-directory-security-best-practices/)
5. Windows Server 2025, security baseline | Microsoft Community Hub, acceso: diciembre 17, 2025, [https://techcommunity.microsoft.com/blog/microsoft-security-baselines/windows-server-2025-security-baseline/4358733](https://techcommunity.microsoft.com/blog/microsoft-security-baselines/windows-server-2025-security-baseline/4358733)
6. AD DS Design Requirements \- Microsoft Learn, acceso: diciembre 17, 2025, [https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/ad-ds-design-requirements](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/ad-ds-design-requirements)
7. Designing the Logical Structure | Microsoft Learn, acceso: diciembre 17, 2025, [https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/designing-the-logical-structure](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/designing-the-logical-structure)
8. Designing the Site Topology | Microsoft Learn, acceso: diciembre 17, 2025, [https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/designing-the-site-topology](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/designing-the-site-topology)
9. step by step instruction on how to add a domain controller to windows server 2025, acceso: diciembre 17, 2025, [https://learn.microsoft.com/en-us/answers/questions/5636005/step-by-step-instruction-on-how-to-add-a-domain-co](https://learn.microsoft.com/en-us/answers/questions/5636005/step-by-step-instruction-on-how-to-add-a-domain-co)
10. Install Active Directory Domain Services (AD DS), acceso: diciembre 17, 2025, [https://activedirectorypro.com/install-ad-ds/](https://activedirectorypro.com/install-ad-ds/)
11. Install and Set Up Active Directory on Windows Server 2025 with LDAPS \- kifarunix.com, acceso: diciembre 17, 2025, [https://kifarunix.com/set-up-active-directory-on-windows-server-2025/](https://kifarunix.com/set-up-active-directory-on-windows-server-2025/)
12. NTLM vs. Kerberos: What's the Difference? \- Rublon, acceso: diciembre 17, 2025, [https://rublon.com/blog/ntlm-vs-kerberos/](https://rublon.com/blog/ntlm-vs-kerberos/)
13. Kerberos vs. NTLM \- Pure Storage Blog, acceso: diciembre 17, 2025, [https://blog.purestorage.com/purely-educational/kerberos-vs-ntlm/](https://blog.purestorage.com/purely-educational/kerberos-vs-ntlm/)
14. NTLMv1, NTLMv2 vs Kerberos – Key Differences & Best Practices \- CalCom Software, acceso: diciembre 17, 2025, [https://calcomsoftware.com/ntlm-v1-and-v2-vs-kerberos/](https://calcomsoftware.com/ntlm-v1-and-v2-vs-kerberos/)
15. Active Directory Hardening Series \- Part 1 – Disabling NTLMv1 | Microsoft Community Hub, acceso: diciembre 17, 2025, [https://techcommunity.microsoft.com/blog/coreinfrastructureandsecurityblog/active-directory-hardening-series---part-1-%E2%80%93-disabling-ntlmv1/3934787](https://techcommunity.microsoft.com/blog/coreinfrastructureandsecurityblog/active-directory-hardening-series---part-1-%E2%80%93-disabling-ntlmv1/3934787)
16. What is Kerberos Authentication? A Complete Overview \- UpGuard, acceso: diciembre 17, 2025, [https://www.upguard.com/blog/kerberos-authentication](https://www.upguard.com/blog/kerberos-authentication)
17. Diamond Ticket Attack: Abusing Kerberos Trust \- Hacking Articles, acceso: diciembre 17, 2025, [https://www.hackingarticles.in/diamond-ticket-attack-abusing-kerberos-trust/](https://www.hackingarticles.in/diamond-ticket-attack-abusing-kerberos-trust/)
18. How the Kerberos PAC Works \- Netwrix, acceso: diciembre 17, 2025, [https://netwrix.com/en/resources/blog/what-is-the-kerberos-pac/](https://netwrix.com/en/resources/blog/what-is-the-kerberos-pac/)
19. AS-REP Roasting: Detection & Remediation Guide \- Netwrix, acceso: diciembre 17, 2025, [https://netwrix.com/en/cybersecurity-glossary/cyber-security-attacks/as-rep-roasting/](https://netwrix.com/en/cybersecurity-glossary/cyber-security-attacks/as-rep-roasting/)
20. Understanding Golden Ticket Attacks \- Netwrix, acceso: diciembre 17, 2025, [https://netwrix.com/en/cybersecurity-glossary/cyber-security-attacks/golden-ticket-attack/](https://netwrix.com/en/cybersecurity-glossary/cyber-security-attacks/golden-ticket-attack/)
21. What is the Kerberos Ticket Granting Service (TGS)? \- JumpCloud, acceso: diciembre 17, 2025, [https://jumpcloud.com/it-index/what-is-the-kerberos-ticket-granting-service-tgs](https://jumpcloud.com/it-index/what-is-the-kerberos-ticket-granting-service-tgs)
22. Understanding Kerberoasting: From Theory to Detection | by Rakshit ..., acceso: diciembre 17, 2025, [https://medium.com/@rakshit68/understanding-kerberoasting-from-theory-to-detection-9e622c996aa9](https://medium.com/@rakshit68/understanding-kerberoasting-from-theory-to-detection-9e622c996aa9)
23. Understanding NTLM and Kerberos: Key Differences and Use Cases \- Netwrix, acceso: diciembre 17, 2025, [https://netwrix.com/en/resources/blog/ntlm-vs-kerberos-authentication-differences/](https://netwrix.com/en/resources/blog/ntlm-vs-kerberos-authentication-differences/)
24. 5 Active Directory misconfigurations (& how they're exploited) \- Hack The Box, acceso: diciembre 17, 2025, [https://www.hackthebox.com/blog/active-directory-misconfigurations](https://www.hackthebox.com/blog/active-directory-misconfigurations)
25. Active Directory misconfigurations guide \- The Quest Blog, acceso: diciembre 17, 2025, [https://blog.quest.com/10-active-directory-misconfigurations-and-how-to-mitigate-them/](https://blog.quest.com/10-active-directory-misconfigurations-and-how-to-mitigate-them/)
26. DCSync Attack: Definition, Examples, and Prevention | ExtraHop, acceso: diciembre 17, 2025, [https://www.extrahop.com/resources/attacks/dcsync](https://www.extrahop.com/resources/attacks/dcsync)
27. DCSync Attacks Explained: Threat to Active Directory Security \- Netwrix, acceso: diciembre 17, 2025, [https://netwrix.com/en/cybersecurity-glossary/cyber-security-attacks/dcsync-attack/](https://netwrix.com/en/cybersecurity-glossary/cyber-security-attacks/dcsync-attack/)
28. Active Directory Replication \- Threat Hunter Playbook, acceso: diciembre 17, 2025, [https://threathunterplaybook.com/library/windows/active_directory_replication.html](https://threathunterplaybook.com/library/windows/active_directory_replication.html)
29. Golden Ticket Attack | Netwrix, acceso: diciembre 17, 2025, [https://www.netwrix.com/en/cybersecurity-glossary/cyber-security-attacks/golden-ticket-attack/](https://www.netwrix.com/en/cybersecurity-glossary/cyber-security-attacks/golden-ticket-attack/)
30. Potential Credential Access via DCSync \- Detection.FYI, acceso: diciembre 17, 2025, [https://detection.fyi/elastic/detection-rules/windows/credential_access_dcsync_replication_rights/](https://detection.fyi/elastic/detection-rules/windows/credential_access_dcsync_replication_rights/)
31. Golden Ticket Attacks on Active Directory \- Semperis, acceso: diciembre 17, 2025, [https://www.semperis.com/blog/golden-ticket-attacks-active-directory/](https://www.semperis.com/blog/golden-ticket-attacks-active-directory/)
32. What is a Silver Ticket Attack? \- CrowdStrike, acceso: diciembre 17, 2025, [https://www.crowdstrike.com/en-us/cybersecurity-101/cyberattacks/silver-ticket-attack/](https://www.crowdstrike.com/en-us/cybersecurity-101/cyberattacks/silver-ticket-attack/)
33. How to Defend Against Silver Ticket Attacks | Semperis Guide, acceso: diciembre 17, 2025, [https://www.semperis.com/blog/how-to-defend-against-silver-ticket-attacks/](https://www.semperis.com/blog/how-to-defend-against-silver-ticket-attacks/)
34. Active directory: disable DES/RC4 and enable AES \- Microsoft Q\&A, acceso: diciembre 17, 2025, [https://learn.microsoft.com/en-us/answers/questions/5628878/active-directory-disable-des-rc4-and-enable-aes](https://learn.microsoft.com/en-us/answers/questions/5628878/active-directory-disable-des-rc4-and-enable-aes)
35. AllExtendedRights \- SpecterOps, acceso: diciembre 17, 2025, [https://bloodhound.specterops.io/resources/edges/all-extended-rights](https://bloodhound.specterops.io/resources/edges/all-extended-rights)
36. AD Tier Model | TryHackMe | Walkthrough | by rootRS7 | Nov, 2025 ..., acceso: diciembre 17, 2025, [https://medium.com/@sehgalrudra07/ad-tier-model-tryhackme-walkthrough-8d3e034546cf](https://medium.com/@sehgalrudra07/ad-tier-model-tryhackme-walkthrough-8d3e034546cf)
37. Active Directory Tiering Explained: Secure Your AD Now\! \- Truesec, acceso: diciembre 17, 2025, [https://www.truesec.com/security/active-directory-tiering](https://www.truesec.com/security/active-directory-tiering)
38. PAM environment tier model | Microsoft Learn, acceso: diciembre 17, 2025, [https://learn.microsoft.com/en-us/microsoft-identity-manager/pam/tier-model-for-partitioning-administrative-privileges](https://learn.microsoft.com/en-us/microsoft-identity-manager/pam/tier-model-for-partitioning-administrative-privileges)
39. Microsoft transitions NTLM to Kerberos in Windows to boost security \- Specops Software, acceso: diciembre 17, 2025, [https://specopssoft.com/blog/microsoft-phases-out-ntlm-with-kerberos/](https://specopssoft.com/blog/microsoft-phases-out-ntlm-with-kerberos/)
40. Network security Restrict NTLM Audit NTLM authentication in this domain \- Windows 10, acceso: diciembre 17, 2025, [https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/network-security-restrict-ntlm-audit-ntlm-authentication-in-this-domain](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/network-security-restrict-ntlm-audit-ntlm-authentication-in-this-domain)
41. How to enable LDAP signing \- Windows Server \- Microsoft Learn, acceso: diciembre 17, 2025, [https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/enable-ldap-signing-in-windows-server](https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/enable-ldap-signing-in-windows-server)
42. 2020, 2023, and 2024 LDAP channel binding and LDAP signing requirements for Windows (KB4520412) \- Microsoft Support, acceso: diciembre 17, 2025, [https://support.microsoft.com/en-au/topic/2020-2023-and-2024-ldap-channel-binding-and-ldap-signing-requirements-for-windows-kb4520412-ef185fb8-00f7-167d-744c-f299a66fc00a](https://support.microsoft.com/en-au/topic/2020-2023-and-2024-ldap-channel-binding-and-ldap-signing-requirements-for-windows-kb4520412-ef185fb8-00f7-167d-744c-f299a66fc00a)
43. The 8 most critical Windows security event IDs \- ManageEngine, acceso: diciembre 17, 2025, [https://download.manageengine.com/products/active-directory-audit/the-eight-most-critical-windows-event-ids.pdf](https://download.manageengine.com/products/active-directory-audit/the-eight-most-critical-windows-event-ids.pdf)
44. Windows Event Log Cheat Sheet | PDF | Login | Remote Desktop Services \- Scribd, acceso: diciembre 17, 2025, [https://www.scribd.com/document/659681382/Windows-Event-Log-Cheat-Sheet](https://www.scribd.com/document/659681382/Windows-Event-Log-Cheat-Sheet)
45. Day 01: Windows Event IDs Insights Aligned with MITRE ATT\&CK | by Nesar Uddin, acceso: diciembre 17, 2025, [https://medium.com/@nesaruddindawood/day-01-windows-event-ids-insights-aligned-with-mitre-att-ck-bb02adfcf54a](https://medium.com/@nesaruddindawood/day-01-windows-event-ids-insights-aligned-with-mitre-att-ck-bb02adfcf54a)
46. What is a Pass-the-Ticket Attack? Detection & Prevention \- Cymulate, acceso: diciembre 17, 2025, [https://cymulate.com/cybersecurity-glossary/pass-the-ticket-attack/](https://cymulate.com/cybersecurity-glossary/pass-the-ticket-attack/)
