FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    bash \
    git

RUN mkdir -p /root/miniconda3 && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /root/miniconda3/miniconda.sh && \
    bash /root/miniconda3/miniconda.sh -b -u -p /root/miniconda3 && \
    rm /root/miniconda3/miniconda.sh

ENV PATH="/root/miniconda3/bin:$PATH"
RUN conda init bash

SHELL ["/bin/bash", "-c"]

WORKDIR /app
COPY . /app

RUN conda env create -f environment.yml
RUN conda run -n unsloth_env pip install "unsloth @ git+https://github.com/unslothai/unsloth.git@79a2112ca4a775ce0b3cb75f5074136cb54ea6df"
RUN conda run -n unsloth_env pip install --no-deps trl peft accelerate bitsandbytes
RUN conda run -n unsloth_env pip install transformers==4.45.1 --force-reinstall

EXPOSE 8000

CMD ["bash", "-c", "source /root/miniconda3/etc/profile.d/conda.sh && conda activate unsloth_env && python3 main.py"]
