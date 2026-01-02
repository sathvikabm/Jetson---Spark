# Jetson---Spark

**Jetson Orin AGX Developer Kit**
1) L4T version - JetPack  - so you cannot have the driver installed seapratedly 
exaplin l4t and its advantages and how this architecture helps

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




**Spark**
