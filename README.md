MultiExplorer Tool
===================

The MultiExplorer is a framework developed with the aim of automating design space exploration for computer architectures. Currently, MultiExplorer has an infrastructure that enables design space exploration for heterogeneous multicore processors, GPUs, and virtual machines.

The multicore processors flow designs chips by integrating performance simulation, physical estimation, and design space exploration steps, using Sniper as the performance simulator and McPAT as the physical estimator. The design space exploration (DSE) is carried out by an NSGA2-based algorithm.

It assumes that all processor designs are dark-silicon aware, using power density as a constraint in the DSE step. For more information about the MultiExplorer CPU flow and its dark-silicon-aware DSE approach, please refer to our paper:

SANTOS, R.;DUENHA, L.; SILVA, A. C. S.; BIGNARDI, T.; SOUSA, M.; TEDESCO, L.; MELGAREJO JUNIOR, J.; AZEVEDO, R.; ORDONEZ, E. D. M.. 
Dark-Silicon Aware Design Space Exploration. JOURNAL OF PARALLEL AND DISTRIBUTED COMPUTING, v. 120, 2018, pp 295-306, ISSN 0743-7315.

For the virtual machine system design space exploration flow, the performance of the virtual machines was measured using the CloudSim}simulator, and the exploration was conducted using the NSGA-II genetic algorithm. The goal of this exploration flow is to maximize application performance and minimize the cost of using virtual machines in a cloud computing environment.

For more information about this execution flow, refer to the paper:

Arigoni, D. and Santos, R. (2022). Exploração do espaço de projetos de sistemas heterogêneos aplicada ao problema de alocação de recursos em nuvem. 
Master’s thesis, Universidade Federal de Mato Grosso do Sul.

[paper](https://repositorio.ufms.br/handle/123456789/5005)

For the heterogeneous GPU-based system design space exploration flow, simulation and physical estimation tools such as GPGPU-Sim and GPUWattch were used. 
The exploration algorithm employed was NSGA-II. The flow aims to maximize performance while minimizing the power density of GPU-based computational systems.

For more information:

Sonohata, R. and Duenha, L. (2022). Exploração do espaço de projetos de sistemas gpgpu ciente de dark silicon. 
Master’s thesis, Universidade Federal de Mato Grosso do Sul.

[paper](https://repositorio.ufms.br/handle/123456789/5070)

User Manual
===========
MultiExplorer has a user manual available:

[English Version](https://drive.google.com/file/d/1hCKnrWTLyh5HLZS_5E9AP_qamxDm3R26/view?usp=drive_link)

[Versão em Português](https://drive.google.com/file/d/1k-dRORaTcIzu-WT24yhHfvvvH-zKF_62/view?usp=drive_link)

[Extending MultiExplorer](https://drive.google.com/file/d/1xHp9yB6vfc2T2_3pC-Ury0blBEzYLBZf/view?usp=drive_link)

How to Install ?
================
The first step is to acquire a stable version of MultiExplorer from a release in the
[repository](https://github.com/lscad-facom-ufms/MultiExplorer.git)

To clone the repository along with its submodules, run:

`$ git clone --recurse-submodules https://github.com/lscad-facom-ufms/multiexplorer.git`

Important setting files are:
- *.env*: you must set the DISPLAY variable if you want to use the GUI (only required for **Docker** environments)
- *MultiExplorer/src/config.py*: you will need proper path settings

Then you can use our **GNU Make** script for the basic setup.

`$ make`

Using a **Docker** container is advised.
We maintain a pre-compiled version of Sniper-8.0 for use in the Docker environment
[precompiled_sniper](https://drive.google.com/file/d/1aXNxy6OZ7NjP1XUgnhOGuTFAUePtwZkW/view) that you will also need to run MultiExplorer in this preset environment.

Using the Docker Container
============================
As long as **Docker** is installed and running, you can use **MultiExplorer** in a Docker container.

We have a pre-compiled version of Sniper and benchmarks, that will work in the
container: [pre-compiled sniper-8.0](https://drive.google.com/file/d/1GiQGrqf2AhLcd1fX9bfhGLvXP78YsnD3/view?usp=share_link).
Download it and extract it in this folder.

Our docker environment requires a ".env" file, including information about what
DISPLAY to connect to when running the GUI. A "example.env" is included, so you can just copy it
or run:

`$ make config`

After the ".env" file is ready, you can start the container and ssh into it using the following commands:

`$ docker-compose up -d`

`$ docker exec -it <<container_name>> bash`

When the container is built, there's still requirements to be installed, so you should run `$ make`.

After all requirements are installed and ready (including Sniper) you can start the GUI application by running:

`$ python ME.py`

If you are using **Docker** in a Windows environment, remember to run [Xming](http://www.straightrunning.com/XmingNotes/),
and disable authentication.

Even if you are running the container in a Linux environment, you still need to disable authentication on xhost
by running `$ xhost +`

Dependencies
============
Currently **MultiExplorer** has native support only for **Linux** distributions. **Ubuntu 18.04** is recommended.

But you can use **MultiExplorer** in any platform that supports [Docker](https://www.docker.com/), by running it in
a container.

This is highly advisable even when using Linux distros, as our **Docker** environment will be easier to set up and maintain.

If you are using the container on a Windows environment, you will need to use
[XLaunch]https://sourceforge.net/projects/vcxsrv/), so **Docker** can access the graphic display.

Other software requirements are:
- [Sniper 8.0](http://snipersim.org)
  - [Sniper's Benchmarks](https://snipersim.org/w/Download_Benchmarks)  
- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [Java-JDK](https://download.oracle.com/java/22/latest/jdk-22_linux-x64_bin.deb)

In case you want to take a shortcut from compiling Sniper and it's benchmarks, you can get a pre-compiled version . We have a pre-compiled version of Sniper with benchmarks, if you use the Docker environment.
- [Pre-Compiled Sniper with Benchmarks for the Docker Environment](https://drive.google.com/file/d/1aXNxy6OZ7NjP1XUgnhOGuTFAUePtwZkW/view)

It's advisable you use the same versions for **python** libs as listed in our **pip** requirements file 
(*requirements.txt*).

Using the GUI (Graphic User Interface)
======================================
**MultiExplorer** now has a graphic user interface.

Run `$ python ME.py` to use it.

If you are using **Docker** in a Windows environment, remember to run [Xming](http://www.straightrunning.com/XmingNotes/),
and disable authentication.

If you are using **Docker** in a Linux environment, running `$ xhost +` will likewise disable authentication, allowing
the use of the display by software in the container.

Issues
=========================
If you have issues when running MultiExplorer, report them at our github
[issues](https://github.com/lscad-facom-ufms/multiexplorer/issues).

Please notice that we will be focusing on code issues. Set up difficulties can be almost always avoided using
**Docker**, so if you are having difficulties with a native set up, try that first.

Disclaimer About Python 2.7
=========================
Some tools and libs used by MultiExplorer still use Python 2.7, so there's no fixed schedule on the upgrade to Python 3.

We very much would like to advance to Python 3, but moving away from these resources or upgrading them to Python 3 ourselves proved not feasible right now. But this upgrade is still a long term objective of the MultiExplorer project.

Contact us
=========================
Please send us any doubt or comments to lscad.facom.ufms@gmail.com

Attributions
==========================
Icons used in our GUI were obtained through [Flaticon](https://www.flaticon.com/).

<a href="https://www.flaticon.com/free-icons/close" title="close icons">Close icons created by Alfredo Hernandez - Flaticon</a>

<a href="https://www.flaticon.com/free-icons/tick" title="tick icons">Tick icons created by Alfredo Hernandez - Flaticon</a>
