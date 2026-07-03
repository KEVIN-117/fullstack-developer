![Are you referring to the circle art that appears at the beginning of each chapter? If so, we are considering this a decorative image and therefore it will not have alt text. However, if you are referring to a different image, please let me know.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341655102/files/images/f00xxiii-01.jpg)

Hacking is the most important skill set of the 21st century! I don’t make that statement lightly. In recent years, every morning’s headlines reaffirm it. Nations spy on one another to gain secrets, cybercriminals steal billions of dollars, digital worms demand ransoms from their victims, adversaries influence each other’s elections, and combatants take down each other’s utilities. Consider the cyberwar between Ukraine and Russia as an example. These events are all the work of hackers, and we’re only beginning to understand their power in our increasingly digital world.

I decided to write this book after working with tens of thousands of aspiring hackers through Null-Byte, Hackers Arise (_[https://www.hackers-arise.com](https://www.hackers-arise.com/)_), and nearly every branch of the US military and intelligence agencies (including the NSA, DIA, CIA, and FBI). These experiences taught me that many aspiring hackers have little or no experience with Linux, and this lack of experience is the primary barrier to their starting the journey to becoming professionals. Almost all the best hacker tools are written in Linux, so you’ll need some basic Linux skills as a prerequisite to becoming an experienced, professional hacker. I have written this book to help you get over this barrier.

Hacking is an elite profession within the IT field. As such, it requires an extensive and detailed understanding of IT concepts and technologies. At the most fundamental level, Linux is a requirement. I strongly suggest you invest time and energy into understanding it if you want to make hacking and information security your career.

This book is not intended for the experienced hacker or Linux admin. Instead, it is intended for those who want to get started along the exciting path of hacking, cybersecurity, and pentesting. It is also intended not as a complete treatise on Linux or hacking but rather a starting point into these worlds. It begins with the essentials of Linux and extends into some basic scripting in both bash and Python. Wherever appropriate, I use hacking examples to teach these Linux principles.

In this introduction, we’ll look at the growth of ethical hacking for information security, and I’ll take you through the process of installing a virtual machine so you can install Kali Linux on your system without disturbing the operating system you are already running.

## What’s in This Book

In the first set of chapters, you’ll become comfortable with the fundamentals of Linux. **[Chapter 1](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch01.xhtml#ch01)** will get you used to the filesystem and the terminal, and give you some basic commands. **[Chapter 2](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch02.xhtml#ch02)** shows you how to manipulate text to find, examine, and alter software and files.

In **[Chapter 3](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch03.xhtml#ch03)**, you’ll manage networks. You’ll scan for networks, find information on connections, and disguise yourself by masking your network and DNS information.

**[Chapter 4](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch04.xhtml#ch04)** teaches you to add, remove, and update software, and how to keep your system streamlined. In **[Chapter 5](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch05.xhtml#ch05)**, you’ll manipulate file and directory permissions to control who can access what. You’ll also learn some privilege escalation techniques.

**[Chapter 6](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch06.xhtml#ch06)** teaches you how to manage services, including starting and stopping processes and allocating resources to give you greater control. In **[Chapter 7](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch07.xhtml#ch07)**, you’ll manage environment variables for optimal performance, convenience, and even stealth. You’ll find and filter variables, change your PATH variable, and create new environment variables.

**[Chapter 8](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch08.xhtml#ch08)** introduces you to bash scripting, a staple for any serious hacker. You’ll learn the basics of bash and build a script to scan for target ports that you might later infiltrate.

**[Chapters 9](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch09.xhtml#ch09)** and **[10](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch10.xhtml#ch10)** give you some essential filesystem management skills, showing you how to compress and archive files to keep your system clean, copy entire storage devices, and get information on files and connected disks.

The latter chapters dig deeper into hacking topics. In **[Chapter 11](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch11.xhtml#ch11)**, you’ll use and manipulate the logging system to get information on a target’s activity and cover your own tracks. **[Chapter 12](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch12.xhtml#ch12)** shows you how to use and abuse three core Linux services: Apache web server, OpenSSH, and MySQL. You’ll create a web server, build a remote video spy, and learn about databases and their vulnerabilities. **[Chapter 13](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch13.xhtml#ch13)** will show you how to stay secure and anonymous with proxy servers, the Tor network, virtual private networks, and encrypted email.

**[Chapter 14](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch14.xhtml#ch14)** deals with wireless networks. You’ll learn basic networking commands, then crack Wi-Fi access points and detect and connect to Bluetooth signals.

**[Chapter 15](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch15.xhtml#ch15)** dives deeper into Linux itself with a high-level view of how the kernel works and how its drivers can be abused to deliver malicious software. In **[Chapter 16](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch16.xhtml#ch16)**, you’ll learn essential scheduling skills in order to automate your hacking scripts. **[Chapter 17](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch17.xhtml#ch17)** will teach you core Python concepts, and you’ll script two hacking tools: a scanner to spy on TCP/IP connections and a simple password cracker. **[Chapter 18](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch18.xhtml#ch18)** explores the intersection of hacking and artificial intelligence, introducing basic concepts and demonstrating how AI can assist in cybersecurity.

## What Is Ethical Hacking?

With the growth of the information security field in recent years has come dramatic growth in the field of ethical hacking, also known as _white hat_ (good guy) hacking. Ethical hacking is the practice of attempting to infiltrate and exploit a system in order to find out its weaknesses and better secure it. I segment the field of ethical hacking into two primary components: penetration testing for a legitimate information security firm and working for your nation’s military or intelligence agencies. Both are rapidly growing areas, and demand is strong.

### Penetration Testing

As organizations become increasingly security conscious and the cost of security breaches rises exponentially, many large organizations are beginning to contract out security services. One of these key security services is penetration testing. A _penetration test_ is essentially a legal, commissioned hack to demonstrate the vulnerability of a firm’s network and systems.

Generally, organizations conduct a vulnerability assessment first to find potential vulnerabilities in their network, operating systems, and services. I emphasize _potential_, as this vulnerability scan includes a significant number of false positives (things identified as vulnerabilities that really are not). It is the role of the penetration tester to attempt to hack, or penetrate, these vulnerabilities. Only then can the organization know whether the vulnerability is real and decide to invest time and money to close the vulnerability.

### Military and Espionage

Nearly every nation on Earth now engages in cyber espionage and cyber warfare. The cyberwar in Ukraine has brought cyberwar to the forefront of everyone’s consciousness, as hackers worldwide have supported Ukraine’s efforts to remain free. (The hackers at _[https://www.hackers-arise.com](https://www.hackers-arise.com/)_ have played a crucial role in this cyberwar.) In less heated times, one only needs to scan headlines to see that governments use cyber activities to spy on, and even attack, military and industrial systems.

Over time, the impact of hacking in these military and intelligence-gathering activities will become only more significant. Imagine a war of the future in which hackers can gain access to their adversary’s war plans and knock out their electric grid, oil refineries, and water systems. In such a world, the hacker has become a key component of their nation’s defense.

## Why Hackers Use Linux

So, why do hackers use Linux over other operating systems? Mostly because Linux offers a far higher level of control via a few different methods.

### Linux Is Open Source

Unlike Windows, Linux is open source, meaning that the source code of the operating system is available to you. As such, you can change and manipulate it as you please. If you are trying to make a system operate in ways it was not intended to, being able to manipulate the source code is essential.

### Linux Is Transparent

To hack effectively, you must know and understand your operating system and, to a large extent, the operating system you are attacking. Linux is totally transparent, meaning we can see and manipulate all its working parts.

Not so with Windows. Microsoft tries hard to make it as difficult as possible to know the inner workings of its operating systems, so you never really know what’s going on “under the hood,” whereas in Linux, you have a spotlight shining directly on each and every component of the operating system. This makes working with Linux more effective.

### Linux Offers Granular Control

Linux is granular. That means that you have an almost infinite amount of control over the system. In Windows, you can control only what Microsoft allows you to control. In Linux, everything can be controlled by the terminal, at the most miniscule level or the most macro level. In addition, Linux makes scripting in any of the scripting languages simple and effective.

### Most Hacking Tools Are Written for Linux

Well over 90 percent of all hacking tools are written for Linux. There are exceptions, of course, such as Cain and Abel and Wikto, but those exceptions prove the rule. Even when hacking tools such as Metasploit or nmap are ported for Windows, not all capabilities transfer from Linux.

### The Future Belongs to Linux/Unix

This might seem like a radical statement, but I firmly believe that the future of information technology belongs to Linux and Unix systems. Microsoft had its day in the 1980s and 1990s, but its growth is slowing.

Since the internet began, Linux/Unix has been the operating system of choice for web servers due to its stability, reliability, and robustness. Even today, Linux/Unix is used in two-thirds of web servers and dominates the market. Embedded systems in routers, switches, and other devices almost always use a Linux kernel, and the world of virtualization is dominated by Linux, with both VMware and Citrix built on the Linux kernel.

Over 80 percent of mobile devices run Unix or Linux (iOS is Unix, and Android is Linux), so if you believe that the future of computing lies in mobile devices such as tablets and phones (it would be hard to argue otherwise), then the future is Linux/Unix. Microsoft Windows has just 7 percent of the mobile devices market. Is that the wagon you want to be hitched to?

## Downloading Kali Linux

Before getting started, you need to download and install Kali Linux on your computer. This is the Linux distribution we will be working with throughout this book. Linux was first developed by Linus Torvalds in 1991 as an open source alternative to Unix. Since it is open source, volunteer developers code the kernel, the utilities, and the applications. This means that there is no overriding corporate entity overseeing development, and as a result, conventions and standardization are often lacking.

Kali Linux was developed by Offensive Security as a hacking operating system built on a distribution of Linux called Debian. There are many distributions of Linux, and Debian is one of the best. You are probably most familiar with Ubuntu as a popular desktop distribution of Linux. Ubuntu is also built on Debian. Other distributions include Red Hat, CentOS, Mint, Arch, and SUSE. Although they all share the same Linux kernel (the heart of the operating system that controls the CPU, RAM, and so on), each has its own utilities, applications, and choice of graphical interface (GNOME, KDE, and others) for different purposes. As a result, each of these distributions of Linux looks and feels slightly different. Kali was designed for penetration testers and hackers and comes with a significant complement of hacking tools.

I strongly recommend that you use Kali for this book. Although you can use another distribution, you will likely have to manually download and install the various tools we will be using, which could mean many hours of downloading and installing software. In addition, if that distribution is not built on Debian, there may be other minor differences. You can download and install Kali from _[https://www.kali.org](https://www.kali.org/)_.

**NOTE**

_If you’d prefer to install Kali through Windows Subsystem for Linux (WSL) on a computer running Windows, skip to “Installing Kali Through the Windows Subsystem for Linux” on [page xxxvii](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch00.xhtml#ch00lev1sec8)_.

From the home page, hover over the **Downloads** link at the top of the page and click **Download Kali Linux**. You’ll then be faced with multiple download choices. It’s important to choose the right download. Along the left side of the table, you will see the _image name_, which is the name of the version that the link downloads. For instance, you may see an image name called _Kali Linux 64Bit_, meaning it’s the full Kali Linux and is suitable for 64-bit systems (most modern systems use a 64-bit Intel or AMD CPU).

To determine what type of CPU is on your system, go to **Control Panel ▶ System and Security ▶ System**, where it should be listed. If your system is 64-bit, download and install the 64-bit version of the full Kali (not Light, Lxde, or any of the other alternatives). If you are running an older computer with a 32-bit CPU, you will need to install the 32-bit version, which appears lower on the page.

You have a choice of downloading the file via HTTP or Torrent. If you choose HTTP, Kali will download directly to your system just like any download and be placed in your _Downloads_ folder. The torrent download is the peer-to-peer download used by many file-sharing sites. You will need a torrenting application like BitTorrent to use this option. The Kali file will then download to the folder in which the torrenting application stores its downloads.

There are other versions for other types of CPUs, such as the commonly used ARM architecture found in so many mobile devices. If you are using a Raspberry Pi, tablet, or other mobile device, make sure you download and install the ARM architecture version of Kali by scrolling down to Download ARM Images and clicking **Kali ARM Images**. (Phone users will likely prefer Kali NetHunter.)

You should now have Kali downloaded, but before you install anything, I want to talk a bit about virtual machines. Generally, for the beginner, installing a Kali virtual image and then running it in a virtual machine such as VirtualBox or VMWare Workstation is the best solution for learning and practicing.

## Virtual Machines

Virtual machine (VM) technology allows you to run multiple operating systems from one piece of hardware like your laptop or desktop. This means that you can continue to run the Windows or macOS operating system you are familiar with, then run a VM of Kali Linux _inside_ that operating system. You don’t need to overwrite your existing operating system to learn Linux.

Numerous VM applications are available from VMware, Oracle, Microsoft, and other vendors. All are excellent, but here I will show you how to download and install Oracle’s free VirtualBox.

### Installing VirtualBox

You can download VirtualBox at _[https://www.virtualbox.org](https://www.virtualbox.org/)_. Click the **Download** link at the top of the page and select the VirtualBox package for your computer’s current operating system, which will host VirtualBox VM. Make sure to download the latest version. When the download has completed, click the setup file, and you will be greeted by a familiar Setup Wizard. Click **Next**, and you should be greeted with the Custom Setup screen, as in [Figure 1](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch00.xhtml#fig1).

![A screenshot showing how you can select features to be installed if you don’t want the default.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341655102/files/images/f00xxix-01.jpg)

_Figure 1: The Custom Setup dialog_

**NOTE**

_These instructions were written with Windows in mind. If you’re using a Mac, the process may be a little different but you should be able to follow along._

From this screen, simply click **Next**. Keep clicking **Next** until you get to the Network Interfaces warning screen and then click **Yes**.

Click **Install** to begin the process. During this process, you will likely be prompted several times about installing _device software_. These are the virtual networking devices necessary for your VMs to communicate. Click **Install** for each one.

When the installation is complete, click **Finish**.

## Setting Up Your Virtual Machine

Now let’s get you started with your VM. VirtualBox should open once it has installed (if not, open it), and you should be greeted by the VirtualBox Manager, as seen in [Figure 2](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch00.xhtml#fig2).

![A screenshot showing the Welcome screen, with global tools where you can also select basic or expert mode.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341655102/files/images/f00xxx-01.jpg)

_Figure 2: The VirtualBox Manager_

As we will be creating a new VM with Kali Linux, click **New** at the top. This opens the Create Virtual Machine dialog.

Give your machine a name (any name is okay, but I simply used Kali) and then select Linux from the **Type** drop-down menu. Finally, select **Debian (64-bit)** from the third drop-down menu (unless you are using the 32-bit version of Kali, in which case select the Debian 32-bit version). Click **Next**, and you’ll see a screen for selecting how much RAM you want to allocate to this new VM.

As a rule of thumb, I don’t recommend using more than 25 percent of your total system RAM. That means if you’ve installed 4GB on your physical or host system, then select just 1GB for your VM, and if you have 16GB on your physical system, then select 4GB (or 4096MB). The more RAM you give your VM, the better and faster it will run, but you must also leave enough RAM for your host operating system and any other VMs you might want to run simultaneously. Your VMs will not use any RAM when they are inactive, but they will use hard drive space.

Click **Next**, and you’ll get to the Hard Disk screen. Choose **Create Virtual Hard Disk** and click **Create**. You should be asked which hard disk file type to use. Select the suggested default of VDI.

In the next screen, you can decide whether you want the hard drive you are creating to be allocated dynamically or at a fixed size. If you choose **Dynamically Allocated**, the system will _not_ take the entire maximum size you allocate for the virtual hard disk until you need it, saving more unused hard disk space for your host system. I suggest you select dynamically allocated.

Click **Next**, and you’ll choose the amount of hard drive space to allocate to the VM and the location of the VM (see [Figure 3](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch00.xhtml#fig3)).

![A screenshot showing the user allocating 25 GB of hard disk space.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341655102/files/images/f00xxxi-01.jpg)

_Figure 3: Allocating hard drive space_

The default is 8GB. I usually find that to be a bit small and recommend that you allocate 20GB to 25GB at a minimum. Remember, if you chose to dynamically allocate hard drive space, it won’t use the space until you need it, and expanding your hard drive after it has already been allocated can be tricky, so better to err on the high side.

Click **Create**, and you’re ready to go!

### Installing Kali on the VM

At this point, you should see a screen like [Figure 4](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch00.xhtml#fig4). Now you’ll need to install Kali. Note that on the left of the VirtualBox Manager, you should see an indication that Kali VM is powered off. Click the **Start** button (green arrow icon).

![A screenshot of the VirtualBox welcome screen also showing system, display, storage, and audio details.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341655102/files/images/f00xxxi-02.jpg)

_Figure 4: The VirtualBox welcome screen_

The VirtualBox Manager will then ask where to find the startup disk. You’ve already downloaded a disk image with the extension _.iso_, which should be in your _Downloads_ folder (though if you used a torrent to download Kali, the _.isofile_ will be in the _Downloads_ folder of your torrenting application). Click the folder icon to the right, navigate to the _Downloads_ folder, and select the Kali image file (see [Figure 5](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch00.xhtml#fig5)).

![A screenshot of a dialog box with a dropdown menu for selecting the virtural optical disk file or a physical optical drive.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341655102/files/images/f00xxxii-01.jpg)

_Figure 5: Selecting your startup disk_

Then click **Start**. Congratulations, you’ve just installed Kali on a virtual machine!

## Setting Up Kali

Kali will now open a screen like [Figure 6](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch00.xhtml#fig6), offering you several startup choices. I suggest using the graphical install for beginners. Use your keyboard keys to navigate the menu.

If you get an error when you’re installing Kali into your VirtualBox, it’s likely because you don’t have virtualization enabled within your system’s BIOS. Each system and its BIOS are slightly different, so check with your manufacturer or search online for solutions for your system and BIOS. In addition, on Windows systems, you will likely need to disable any competing virtualization software such as Hyper-V. Again, an internet search for your system should guide you in doing so.

![A screenshot of the Kali Linux installer menu in BIOS mode.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341655102/files/images/f00xxxiii-01.jpg)

_Figure 6: Selecting the install method_

You will next be asked to select your language. Make sure you select the language you are most comfortable working in and then click **Continue**. Next, select your location, click **Continue**, and then select your keyboard layout.

When you click Continue, VirtualBox will go through a process of detecting your hardware and network adapters. Just wait patiently as it does so. Eventually, you will be greeted by a screen asking you to configure your network, as in [Figure 7](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch00.xhtml#fig7).

![A screenshot showing instructions for entering the kali hostname and a field to enter it.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341655102/files/images/f00xxxiii-02.jpg)

_Figure 7: Entering a hostname_

The first item it asks for is the name of your host. You can name it anything you please, but I left mine with the default _kali_.

Next, you will be asked for the domain name. It’s not necessary to enter anything here. Click **Continue**. The next screen, shown in [Figure 8](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch00.xhtml#fig8), is very important. Here, you are asked for the password you want to use for the root user. Beginning with Kali 2020 and later versions, Kali provides you a username and password set to _kali_.

![A screenshot of the dialog box for entering a strong password and verifying it.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341655102/files/images/f00xxxiv-01.jpg)

_Figure 8: Choosing a password_

The root user in Linux is the all-powerful system administrator. In this case, you are a regular user, _kali_. You can use any password you feel is secure. If this were a physical system on the internet, I would suggest that you use a very long and complex password to limit the ability of an attacker to crack it. But since this is a VM that people can’t access without first accessing your host operating system, password authentication is less important. Still, choose wisely.

Click **Continue**, and you will be asked to set your time zone. Do so and then continue.

The next screen asks about partition disks (a _partition_ is just what it sounds like—a portion or segment of your hard drive). Choose **Guided – use entire disk**, and Kali will detect your hard drives and set up a partitioner automatically.

Kali will then warn you that all data on the disk you select will be erased . . . but don’t worry! This is a virtual disk, and the disk is new and empty, so this won’t actually do anything. Click **Continue**.

Kali will now ask whether you want all files in one partition or if you want to have separate partitions. If this were a production system, you probably would select separate partitions for _/home_, _/var_, and _/tmp_, but considering that we will be using this as a learning system in a virtual environment, it is safe for you to simply select **All files in one partition**.

Now you be will be asked whether to write your changes to disk. Select **Finish partitioning and write changes to disk**. Kali will prompt you once more to see if you want to write the changes to disk; select **Yes** and click **Continue** (see [Figure 9](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch00.xhtml#fig9)).

![A screenshot of the partition tables that are changed for devices and the partitions to be formatted.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341655102/files/images/f00xxxv-01.jpg)

_Figure 9: Writing changes to disk_

Kali will begin to install the operating system. This could take a while, so be patient. Now is the time to take your bathroom break and get your favorite beverage.

Once the installation is complete, you will be prompted as to whether you want to use a network mirror. This really is not necessary, so click **No**.

Then Kali will prompt you as to whether you want to install Grand Unified Bootloader (GRUB), shown in [Figure 10](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch00.xhtml#fig10). A _bootloader_ enables you to select different operating systems to boot into, which means when you boot your VM, you can boot into either Kali or another operating system. Select **Yes** and click **Continue**.

![A screenshot of the prompt to install the GRUB bootloader, which shows a warning that other operating systems on your computer may be temporarily unbootable.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341655102/files/images/f00xxxvi-01.jpg)

_Figure 10: Installing GRUB_

On the next screen, you will be asked whether you want to install the GRUB bootloader automatically or manually. For reasons as yet unclear, if you choose the second option, Kali will tend to hang and display a blank screen after installation. Select **Enter device manually**.

On the following screen, select the drive where the GRUB bootloader should be installed (it will likely be something like _/dev/sda_). Click through to the next screen, which should tell you that the installation is complete.

Congratulations! You’ve installed Kali. Click **Continue**. Kali will attempt to reboot, and you will see a number of lines of code go across a blank black screen before you are eventually greeted with Kali’s login screen, as shown in [Figure 11](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch00.xhtml#fig11).

![A screenshot of the desktop with a login dialog for the kali user and a prompt to enter the password.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341655102/files/images/f00xxxvi-02.jpg)

_Figure 11: The Kali login screen_

Log in as _kali_ using the password _kali_, or whichever password you have selected. You should be greeted with the Kali desktop, as in [Figure 12](https://learning.oreilly.com/library/view/linux-basics-for/9798341655102/xhtml/ch00.xhtml#fig12).

![A screenshot of the default Kali desktop showing a dragon image in the background.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9798341655102/files/images/f00xxxvii-01.jpg)

_Figure 12: The Kali home screen_

You are now ready to begin your journey into the exciting field of hacking! Welcome!

## Installing Kali Through the Windows Subsystem for Linux

For those looking for a less intrusive method of running Linux, Microsoft offers the Windows Subsystem for Linux (WSL). Using it, you can learn the Linux operating system without the hassle of installing a VM. The drawback is that many networking (and, therefore, hacking) capabilities are not enabled. This means that you can learn Linux but not study hacking with this subsystem. That said, here’s how to install this WSL on your Windows operating system.

The first step is to enable WSL. Open PowerShell by running powershell at the command prompt or entering **PowerShell** in your application menu. Then enter the following at the PowerShell prompt:

PS>Enable_windowsOptionalFeature -Online –FeatureName Microsoft-Subsystem-Linux
Do you want to restart the computer to complete this operation now?
[Y] Yes  [N] No  [?] Help (default is Y):

As you can see, PowerShell will then ask you whether you want to restart your system to enable WSL. Press ENTER.

Now that you have enabled this feature and restarted your system, you need to install Kali. Go to the Windows Application store (_[https://apps.microsoft.com/store/apps](https://apps.microsoft.com/store/apps)_). There, you should see icons for many major Linux distributions. Click **Kali Linux**, then select **Get**.

Kali will begin to download. This is a stripped-down, essentials-only version of Kali, so the download should be quick. Once it’s complete, you will be prompted for a username and password.

The minimal version you just installed has little to no tools (depending on your definition of the word _tool_). So, you need to download all Kali tools. Enter the following command to update, upgrade, and install them from the Kali repository:

$ sudo apt update && sudo apt upgrade -y && sudo apt install kali-linux-everything -y

You will need to enter your username and password to proceed. This installation can take quite a while, so take a break and get your favorite beverage.

Note that this version of Linux differs from the one you’d install through VirtualBox in a few ways. First, the Linux system shares the same IP address and MAC address as the Windows system. This is notably different from the VirtualBox version, where the interfaces have separate IP and MAC addresses. (To see this information, run sudo ipconfig in Linux and ipconfig in the Windows command prompt and compare the output.)

Another difference is that, unfortunately, several functions on this virtualized Linux are not enabled by default. One of these is ping, the Linux utility for testing whether a host is up. When we try to ping another system on our local network or _[https://www.google.com](https://www.google.com/)_, both return this cryptic message:

ping:socket: Operation not permitted

To enable ping on our newly install Kali system, enter the following command:

$ sudo setcapcap_net_raw+p /bin/ping

After you do so, you should now be able to ping _[https://www.google.com](https://www.google.com/)_.

You are now ready to use Kali within Windows! For the seasoned Linux user, WSL makes it easy to test your tools and scripts. However, I still recommend a native install for professional penetration testing.