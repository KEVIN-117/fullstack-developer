### 1. Preparación y Red

Una vez que hayas arrancado la ISO de Arch Linux en tu VM, deberías estar en la terminal como usuario `root`.

- **Verifica la conexión a internet:** En una VM, la red suele configurarse automáticamente por DHCP.
    
    
    ```
    ping -c 3 archlinux.org
    ```
    
- **Actualiza el reloj del sistema:**
    


```bash
    timedatectl set-ntp true
```

### 2. Particionado del Disco
Crearemos dos particiones básicas: una para el arranque (EFI) y otra para el sistema raíz (Root). Usaremos `fdisk`.

1.  Abre la utilidad de discos:
    
```bash
    fdisk /dev/sda
```
2.  Escribe `g` y presiona Enter para crear una nueva tabla de particiones GPT.
3.  **Partición EFI (Arranque):**
    *   Escribe `n` (nueva partición), luego Enter tres veces.
    *   En *Last sector*, escribe `+512M` y presiona Enter.
    *   Escribe `t` (cambiar tipo), luego `1` (para EFI System).
4.  **Partición Root (Sistema):**
    *   Escribe `n` y presiona Enter cuatro veces para usar todo el espacio restante.
5.  Escribe `w` y presiona Enter para guardar los cambios y salir.

### 3. Formateo y Montaje
Ahora debemos darle formato a las particiones que acabamos de crear y montarlas en el sistema en vivo.

*   **Formatea la partición EFI en FAT32:**
    ```bash
    mkfs.fat -F32 /dev/sda1
    ```
*   **Formatea la partición Root en ext4:**
    ```bash
    mkfs.ext4 /dev/sda2
    ```
*   **Monta las particiones:**
    ```bash
    mount /dev/sda2 /mnt
    mount --mkdir /dev/sda1 /mnt/boot
    ```

### 4. Instalación del Sistema Base
Usaremos el script `pacstrap` para instalar el sistema base, el kernel de Linux, el firmware y un editor de texto.
```bash
pacstrap -K /mnt base linux linux-firmware nano
````

### 5. Configuración del Sistema (Chroot)

Genera el archivo `fstab` (que le dice al sistema qué particiones montar al inicio) y luego entra en tu nuevo sistema.

- **Generar fstab:**
    
    Bash
    
    ```
    genfstab -U /mnt >> /mnt/etc/fstab
    ```
    
- **Entrar al sistema instalado (Chroot):**
    
    Bash
    
    ```
    arch-chroot /mnt
    ```
    

A partir de este punto, **estás operando dentro de tu nueva instalación.**

### 6. Zona Horaria e Idioma

Configura la región y el idioma del sistema.

- **Zona horaria:** (Ajusta "America/La_Paz" según tu ubicación).
    

```
    ln -sf /usr/share/zoneinfo/America/La_Paz /etc/localtime
    hwclock --systohc
```
*   **Idioma:** Edita el archivo `locale.gen`.
    ```bash
    nano /etc/locale.gen
    ```
    Descomenta (borra el `#` al principio) las líneas `en_US.UTF-8 UTF-8` y la de tu idioma preferido (ej. `es_ES.UTF-8 UTF-8`). Guarda con `Ctrl+O`, Enter, y sal con `Ctrl+X`.
*   **Genera los locales y configura el idioma por defecto:**
    
```bash
    locale-gen
    echo "LANG=es_ES.UTF-8" > /etc/locale.conf
```

### 7. Red y Contraseña
*   **Nombre del equipo (Hostname):** (Puedes cambiar "archvm" por el nombre que quieras).
    
```bash
    echo archvm > /etc/hostname
```
*   **Establece la contraseña de root:** Escribe el siguiente comando y proporciona una contraseña segura.
    
```bash
    passwd
```

### 8. Gestor de Arranque (GRUB) y Red Automática
Para poder iniciar el sistema y tener internet tras el reinicio, necesitamos instalar GRUB y NetworkManager.

1.  **Instala los paquetes necesarios:**
    
```bash
    pacman -S grub efibootmgr networkmanager
```
2.  **Instala GRUB en el disco:**
    
```bash
    grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
```
3.  **Genera el archivo de configuración de GRUB:**
    ```bash
    grub-mkconfig -o /boot/grub/grub.cfg
    ```
4.  **Habilita el gestor de red** para que se inicie automáticamente:
    ```bash
    systemctl enable NetworkManager
    ```

### 9. Salir y Reiniciar
¡La instalación base está completa! Ahora solo queda salir limpiamente y reiniciar.

```bash
exit
umount -R /mnt
reboot
````

Una vez que la máquina virtual se reinicie (recuerda retirar la ISO virtual si la VM vuelve a iniciar desde el instalador), verás el menú de GRUB y luego se te pedirá el login de `root`. Desde ahí, puedes proceder a crear tu usuario estándar y, si lo deseas, instalar un entorno de escritorio.