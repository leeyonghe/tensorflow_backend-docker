# CUDA 기반 Ubuntu 이미지를 사용
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

# 기본 환경 설정
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

# 기본 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    python3 \
    python3-pip \
    python3-dev \
    ninja-build \
    pkg-config \
    libssl-dev \
    clang \
    clang-format \
    ccache \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt* ./
RUN if [ -f requirements.txt ]; then pip3 install -r requirements.txt; fi
RUN pip3 install \
    tensorflow \
    numpy \
    pytest \
    pre-commit \
    black \
    isort \
    flake8

# CMake 최신 버전 설치 (3.27.0)
RUN wget https://github.com/Kitware/CMake/releases/download/v3.27.0/cmake-3.27.0-linux-x86_64.sh \
    -q -O /tmp/cmake-install.sh \
    && chmod u+x /tmp/cmake-install.sh \
    && mkdir /opt/cmake \
    && /tmp/cmake-install.sh --skip-license --prefix=/opt/cmake \
    && ln -s /opt/cmake/bin/* /usr/local/bin/ \
    && rm /tmp/cmake-install.sh

# 작업 디렉토리 설정
WORKDIR /workspace

# 기본 쉘 명령어 설정
CMD ["/bin/bash"] 