# Jetson---Spark

This project was done to understand Jetson Agx Orin and Spark Hardware infra and the socket Communication part of send and receive between two heterogeneous devices doing the inference 

**Jetson Orin AGX Developer Kit**

Jetpack supplies CUDA libs at the OS level (JetPack), conda env supplies Python + many libraries. pip might install wheels that assume a different CUDA / different GLIBC / different libstdc++ than what Jetson has.

3 classic failure modes:
-> CPU-only wheel gets installed
  pip install torch on Jetson might pull a CPU wheel (or source build fails and you end up without CUDA-enabled torch)
  Then torch.cuda.is_available() -> False
  Or torch.version.cuda is None
  
-> Wheel installs, import works, CUDA fails
  Because runtime can’t find matching CUDA libs or symbols
  You’ll see errors referencing libcudart.so, libcublas.so, libcudnn.so, or GLIBCXX_x.y.z
  
-> ABI mismatch
  You install cp312 python but the repo has only cp310 wheels for that package on aarch64
  pip can’t use wheel -> tries to build -> fails or produces a broken build


This is why the Jetson AI Lab index exists: it hosts wheels that match Jetson realities.


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


HOW THESE WHEELS GET “PUT TOGETHER” INTO A WORKING CONTAINER
A container image is basically:
1)Base OS (Ubuntu/L4T for Jetson)
2)CUDA stack (from JetPack inside the image, or mounted from host depending on how container is designed)
3)Python env (system python or conda)
4)pip installs using an index that contains compatible wheels

Typical “Jetson container” strategy:
Start from an L4T base image that matches host JetPack
Ensure CUDA libs are present/visible
Set pip to use pypi.jetson-ai-lab.io/jp6/cu12x
Install torch / vllm / flash-attn / etc from that index so you get the right aarch64+CUDA wheels
🔥 Container “ready for use” basically means the wheel set matches the base image’s CUDA + Python ABI.


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

I ran the Qwen2.5-VL-3B-Instruct model -> Image: dustynv/vllm:0.7.4-r36.4.0-cu128-24.04

Container/Image Layer:
The Docker image (dustynv/vllm:0.7.4-r36.4.0-cu128-24.04) contains:
-> CUDA 12.8 libraries for GPU acceleration
-> vLLM framework and dependencies
-> Python environment
-> Model:Qwen2.5-VL-3B-Instruct

Starting vLLM Inside the Container
### 1. **Run the container with vLLM server::**
```
docker run -d \
  --gpus all \
  -p 8000:8000 \
  --name vllm-server \
  dustynv/vllm:0.7.4-r36.4.0-cu128-24.04 \
  vllm serve Qwen/Qwen2.5-VL-3B-Instruct \
  --host 0.0.0.0 \
  --port 8000
```

### 2. **What happens when the container starts:**

**a) Model Loading Phase:**
- vLLM downloads the model (if not cached) from HuggingFace
- Loads model weights into GPU memory
- Initializes the KV cache (key-value cache for attention)
- Sets up paged attention mechanism
- Creates worker processes for parallel inference

**b) Server Initialization:**
- Starts an HTTP server (typically FastAPI/OpenAI-compatible API)
- Listens on port 8000
- Ready to accept requests

**c) Behind the scenes:**
```
Container starts → vLLM engine initializes → Model loads to GPU → 
→ Paged Attention setup → KV cache allocated → HTTP server ready
```

Sending Queries & Response Flow
Method 1: OpenAI-Compatible API (Recommended)
```
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-VL-3B-Instruct",
    "prompt": "Explain quantum computing in simple terms",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

Method 2: Chat Completions API
```
curl http://localhost:8000/v1/chat/completions \
-H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-VL-3B-Instruct",
    "messages": [
      {"role": "user", "content": "What is machine learning?"}
    ]
  }'
```

## **Behind-the-Scenes Flow (Query → Response)**
```
┌─────────────┐
│ Your Query  │
│  (HTTP)     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│  vLLM HTTP Server           │
│  (FastAPI/OpenAI API)       │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  Request Preprocessing      │
│  - Tokenization             │
│  - Batch formation          │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  vLLM Engine Core           │
│  - Request scheduling       │
│  - Continuous batching      │
│  - Paged Attention          │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  GPU Inference              │
│  - Model forward pass       │
│  - KV cache management      │
│  - Token generation         │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  Decoding & Detokenization  │
│  - Token → Text             │
│  - Response formatting      │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────┐
│   Response  │
│   (JSON)    │
└─────────────┘
```

**Response**
```
{
  "id": "cmpl-12345",
  "object": "text_completion",
  "created": 1234567890,
  "model": "Qwen/Qwen2.5-VL-3B-Instruct",
  "choices": [
    {
      "text": "Machine learning is a subset of AI...",
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 50,
    "total_tokens": 65
  }
}
```

**Spark**


For Spark I used the python script to query -> 

┌─────────────────────────────────────────────────────┐
│         OPTION 1: vLLM Server (What you started)    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Docker Container                                   │
│  ┌──────────────────────────────────────┐          │
│  │  vLLM Server Process                 │          │
│  │  - Loads model to GPU                │          │
│  │  - Manages inference engine          │          │
│  │  - HTTP API on port 8000             │          │
│  └──────────────────────────────────────┘          │
│         ▲                                           │
│         │ HTTP Request                              │
│         │                                           │
└─────────┼───────────────────────────────────────────┘
          │
          │
┌─────────┼───────────────────────────────────────────┐
│         │  Your Python Script (Client)              │
├─────────┴───────────────────────────────────────────┤
│                                                     │
│  def chat(text):                                    │
│      requests.post("http://localhost:8000/...")    │
│                                                     │
│  - Does NOT load the model                          │
│  - Does NOT run inference                           │
│  - Just formats & sends HTTP requests               │
│  - Receives & parses responses                      │
│                                                     │
└─────────────────────────────────────────────────────┘



**Steps and flow**
1. You start vLLM container:
   ┌────────────────────────┐
   │ vLLM loads model to    │
   │ GPU and starts server  │
   └────────────────────────┘

2. You run Python script:
   ┌────────────────────────┐
   │ Script sends HTTP      │
   │ request to localhost   │
   └────────────────────────┘
            │
            ▼
   ┌────────────────────────┐
   │ vLLM receives request  │
   │ Runs inference on GPU  │
   │ Returns response       │
   └────────────────────────┘
            │
            ▼
   ┌────────────────────────┐
   │ Script receives JSON   │
   │ Extracts text          │
   │ Sends to Jetson        │
   └────────────────────────┘

