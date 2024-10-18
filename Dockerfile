FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3-pip \
    build-essential \
    wget \
    bash \
    git

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

RUN pip install --upgrade pip
RUN pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
RUN pip install \
    typing==3.7.4.3 \
    pandas==2.2.3 \
    psutil==6.1.0 \
    xformers==0.0.28.post1 \
    datasets==3.0.1 \
    rich==13.9.2 \
    openpyxl==3.1.5

RUN pip install "unsloth @ git+https://github.com/unslothai/unsloth.git@79a2112ca4a775ce0b3cb75f5074136cb54ea6df"

RUN pip install --no-deps \
    trl==0.11.3 \
    peft==0.13.2 \
    accelerate==1.0.1 \
    bitsandbytes==0.44.1

RUN pip install transformers==4.45.1 huggingface-hub==0.25.0 --force-reinstall

ENV PYTHONUNBUFFERED=1
ENV TORCHDYNAMO_DISABLE=1

WORKDIR /app
COPY . /app

EXPOSE 8000

CMD ["python3", "-u", "main.py"]