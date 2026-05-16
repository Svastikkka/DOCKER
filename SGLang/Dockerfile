FROM cgr.dev/chainguard/wolfi-base AS builder

# 1. Configure Wolfi and Chainguard Repositories
RUN echo "https://packages.wolfi.dev/os" > /etc/apk/repositories && \
    echo "https://apk.cgr.dev/chainguard" >> /etc/apk/repositories && \
    echo "https://apk.cgr.dev/extra-packages" >> /etc/apk/repositories

# 2. Install system dependencies
RUN (apk update || (sleep 5 && apk update)) && apk add \
    python-3.13 \
    py3-pip \
    python-3.13-dev \
    build-base \
    git \
    bash \
    cmake \
    linux-headers \
    wget \
    curl \
    zlib \
    patchelf \
    curl \
    glibc-dev \
    libxml2-dev \
    zlib-dev \
    libxml2 \
    glibc \
    samurai \
    curl \
    gcc \
    libffi-dev \
    openssl-dev \
    protobuf-dev \
    numactl-dev

# 3. Install Rust via rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# 4. Add Rust to the PATH so the next RUN commands can see 'cargo'
ENV PATH="/root/.cargo/bin:${PATH}"

# 5. Install NVCC and CUDA Toolkit via PIP
RUN pip install --no-cache-dir \
    nvidia-cuda-nvcc-cu12==12.2.140 \
    nvidia-cuda-runtime-cu12==12.2.140 \
    nvidia-cudnn-cu12==8.9.4.25 \
    nvidia-cublas-cu12==12.2.5.6

# 6. Add symlink
RUN ln -sf /usr/lib/libxml2.so.16 /usr/lib/libxml2.so.2

# 7. Download and Extract CUDA Toolkit
RUN wget https://developer.download.nvidia.com/compute/cuda/12.2.0/local_installers/cuda_12.2.0_535.54.03_linux.run && \
    sh cuda_12.2.0_535.54.03_linux.run --target /opt/cuda-extracted --noexec && \
    rm cuda_12.2.0_535.54.03_linux.run

# 8. Create wrapper scripts
RUN echo '#!/bin/sh' > /usr/bin/nvcc && \
    echo '/lib/ld-linux-x86-64.so.2 --library-path /opt/cuda-extracted/builds/cuda_nvcc/lib:/usr/lib /opt/cuda-extracted/builds/cuda_nvcc/bin/nvcc "$@"' >> /usr/bin/nvcc && \
    chmod +x /usr/bin/nvcc && \
    \
    echo '#!/bin/sh' > /usr/bin/ptxas && \
    echo '/lib/ld-linux-x86-64.so.2 --library-path /opt/cuda-extracted/builds/cuda_nvcc/lib:/usr/lib /opt/cuda-extracted/builds/cuda_nvcc/bin/ptxas "$@"' >> /usr/bin/ptxas && \
    chmod +x /usr/bin/ptxas

# 9. Environment
ENV CUDA_HOME="/opt/cuda-extracted/builds/cuda_nvcc"
ENV PATH="/usr/bin:${PATH}"
ENV LD_LIBRARY_PATH="/opt/cuda-extracted/builds/cuda_nvcc/lib:/usr/lib:${LD_LIBRARY_PATH}"

# 10. Verification
RUN python3 --version && nvcc --version && cargo --version

# 11. Python deps
RUN pip install --no-cache-dir setuptools-rust setuptools wheel numpy && \
    pip install --no-cache-dir torch==2.5.1 --index-url https://download.pytorch.org/whl/cu121

# 12. SGLang
# RUN pip install --no-cache-dir --upgrade pip && \
#    pip install --no-cache-dir --no-build-isolation "sglang[all]" --find-links https://flashinfer.ai/whl/cu121/torch2.5/flashinfer/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --no-build-isolation "sglang[all]>=v0.5.10.post1"

# 13. Install Transformers
# RUN pip install --no-cache-dir "transformers==4.46.3" "compressed-tensors==0.8.0"
RUN pip install --no-cache-dir "transformers>=4.57.0" "compressed-tensors==0.8.0"

RUN UTILS_PATH=$(python3 -c "import sglang.srt.utils as u; print(u.__file__)") && \
    sed -i 's/raise ValueError("No GPU memory values found.")/return 80 * 1024**3/g' "$UTILS_PATH"

FROM cgr.dev/chainguard/wolfi-base

# Repositories
RUN echo "https://packages.wolfi.dev/os" > /etc/apk/repositories && \
    echo "https://apk.cgr.dev/chainguard" >> /etc/apk/repositories && \
    echo "https://apk.cgr.dev/extra-packages" >> /etc/apk/repositories

# Only runtime deps (minimal)
RUN apk update && apk add \
    python-3.13 \
    python-3.13-dev \
    build-base \
    py3-pip \
    libxml2 \
    glibc \
    libstdc++ \
    libgcc \
    bash \
    samurai \
    gcc-14-default \
    libstdc++-dev \
    linux-headers \
    numactl

# Copy Python environment
COPY --from=builder /usr/lib/python3.13 /usr/lib/python3.13
COPY --from=builder /usr/bin/python3 /usr/bin/python3

# Copy CUDA + wrappers
COPY --from=builder /opt/cuda-extracted /opt/cuda-extracted
COPY --from=builder /usr/bin/nvcc /usr/bin/nvcc
COPY --from=builder /usr/bin/ptxas /usr/bin/ptxas

# Copy site-packages (important)
COPY --from=builder /usr/lib/python3.13/site-packages /usr/lib/python3.13/site-packages

RUN mkdir -p /usr/local && \
    ln -s /opt/cuda-extracted/builds/cuda_nvcc /usr/local/cuda

# Copy Rust toolchain from builder
COPY --from=builder /root/.cargo /root/.cargo
COPY --from=builder /root/.rustup /root/.rustup

# Add cargo to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# EnvS
ENV CC=gcc
ENV CXX=g++
ENV CUDA_HOME=/usr/local/cuda
ENV PATH="/usr/bin:${PATH}"
ENV LD_LIBRARY_PATH="/opt/cuda-extracted/builds/cuda_nvcc/lib:/usr/lib:${LD_LIBRARY_PATH}"

RUN pip install --no-cache-dir "transformers>=4.57.0" "compressed-tensors==0.8.0"

# Entry
# ENTRYPOINT ["python3", "-m", "sglang.launch_server", "--model-path", "qwen/qwen2.5-0.5b-instruct", "--host", "0.0.0.0"]
# python3 -m sglang.launch_server --model-path qwen/qwen2.5-0.5b-instruct --host 0.0.0.0 --attention-backend triton --mem-fraction-static 0.7
# python3 -m sglang.launch_server --model-path voicing-ai/Voicing-Agent-30B-Instruct --served-model-name voicing-llm-v1.5 --host 0.0.0.0 --port 8000 --tp 1 --trust-remote-code --dtype bfloat16 --mem-fraction-static 0.75 --attention-backend triton --sampling-backend pytorch
# python3 -c "from sglang.srt.parser.reasoning_parser import ReasoningParser; print(list(ReasoningParser.DetectorMap.keys()))"
