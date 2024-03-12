# Contact tomdeore@gmail.com
# Distributed under the terms of MIT License.
# Usage 'docker run -it --gpus all <image> bash'

FROM nvidia/cuda:12.2.0-devel-ubuntu22.04
MAINTAINER Milind Deore <tomdeore@gmail.com>

# Enviornment variables:
ENV TZ=Asia/Kolkata
ENV DEBIAN_FRONTEND=noninteractive

# Update and Upgrade the packages:
RUN apt-get -y update -qq && apt-get -y upgrade -qq && apt-get install tzdata

# Install essentials:
RUN apt-get -y install wget unzip build-essential gfortran pkg-config cmake git python3.10 python-is-python3 python3-pip python3.10-venv

# Work directory inside docker:
WORKDIR /root

# Python virtual env:
ENV VIRTUAL_ENV=/root/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Load model and application
COPY src/nonymus-7b-q8_0-v0.1.gguf .
COPY src/nonymus_llm.bin .
COPY src/requirements.txt .
COPY src/dist .

# Install dependencies:
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN CMAKE_ARGS="-DLLAMA_CUBLAS=on -DCMAKE_CUDA_COMPILER:PATH=nvcc" FORCE_CMAKE=1 pip install llama-cpp-python

# Run the application
EXPOSE 8080
CMD uvicorn nn_main:app --proxy-headers --reload --host 0.0.0.0 --port 8080


