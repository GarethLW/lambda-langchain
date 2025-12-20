FROM public.ecr.aws/lambda/python:3.11

# Install runtime dependencies
COPY requirements.txt  ./
# Upgrade pip & install system build tools needed by some Python packages
RUN pip install --upgrade pip setuptools wheel && \
    yum install -y gcc make openssl-devel libffi-devel && \
    # Install Rust toolchain via rustup so packages like tiktoken can build
    curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    # Ensure rust is on PATH for subsequent pip invocations
    export PATH="/root/.cargo/bin:$PATH" && \
    pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also use a custom bootstrap for ASGI apps)
CMD ["handler.lambda_handler"]
