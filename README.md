# Jetson---Spark

**Jetson Orin AGX Developer Kit**
1) L4T version - JetPack  - so you cannot have the driver installed seapratedly 
exaplin l4t and its advantages and how this architecture helps
The JetPack for L4T (Jetson Development Pack) is an on-demand all-in-one package that bundles and installs all software tools required to develop for the NVIDIA® Jetson Embedded Platform (including flashing your Jetson Development Kit with the latest OS images). JetPack includes host and target development tools, APIs and packages (OS images, tools, APIs, middleware, samples, documentation including compiling samples) to enable developers to jump start their development environment for developing with the Jetson Embedded Platform. The latest release of JetPack runs on an Ubuntu 14.04 Linux 64-bit host system and supports both the latest Jetson TX1 Development Kit and Jetson TK1 Development Kit.

2) Jetson software aligns with the Server Base System Architecture (SBSA), positioning Jetson Thor alongside industry-standard ARM server design.
SBSA standardizes critical hardware and firmware interfaces, delivering stronger OS support, simpler software portability, and smoother enterprise integration. 
JetPack is built on a modern foundation with a redesigned compute stack featuring Linux kernel 6.8 and Jetson Linux, which is derived from Ubuntu 24.04 LTS.
It introduces several critical technical advancements: 
The Holoscan Sensor Bridge enables flexible, high-throughput sensor data integration; Multi-Instance GPU (MIG) support brings resource partitioning to Jetson, 
allowing concurrent and isolated workloads; and the inclusion of a PREEMPT_RT kernel unlocks true deterministic performance for mission-critical, real-time use cases.
Jetson software is optimized for humanoid robotics and machines that interact dynamically with the physical world. 
It is fully ready for generative AI, enabling developers to deploy large language models (LLM), diffusion models, and vision-language models (VLM) directly at the edge. 

SBSA - wheels made available - https://pypi.jetson-ai-lab.io/jp6/cu126

sudo bash -c 'echo "deb https://repo.download.nvidia.com/jetson/common r34.1 main" >> /etc/apt/sources.list.d/nvidia-l4t-apt-source.list'
sudo bash -c 'echo "deb https://repo.download.nvidia.com/jetson/t234 r34.1 main" >> /etc/apt/sources.list.d/nvidia-l4t-apt-source.list'
sudo apt update
sudo apt dist-upgrade
sudo reboot
sudo apt install nvidia-jetpack

[Jetpack Explained]
<img src="https://developer.download.nvidia.com/images/jetson/jetson-software-stack-diagram-r1-01(1).svg">

**Jetson Container Speciality**
```
jtop
sudo apt-get update && sudo apt-get intall git python3-pip
# install the container tools
git clone https://github.com/dusty-nv/jetson-containers
bash jetson-containers/install.sh

#docker add yourself to not get permission everytime
sudo usermod -aG docker $USER

#reboot

# automatically pull & run any container
jetson-containers run $(autotag l4t-pytorch)

#localhost -> 
```




**Spark**
