# Main image
FROM docker.io/library/debian:bookworm-20240701
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install packages
RUN DEBIAN_FRONTEND=noninteractive \
  apt-get update \
  && \
  apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates=20230311 \
    curl=7.88.1-10+deb12u7 \
    git \
    python3-pip=23.0.1+dfsg-1 \
  && \
  apt-get clean \
  && \
  rm -rf /var/lib/apt/lists/*

# Install s6 overlay
RUN \
  if [ "$(uname -m)" = "x86_64" ]; then \
    curl https://github.com/just-containers/s6-overlay/releases/download/v2.2.0.3/s6-overlay-amd64-installer --location --output /tmp/s6-overlay-installer \
  ; fi \
  && \
  if [ "$(uname -m)" = "aarch64" ]; then \
    curl https://github.com/just-containers/s6-overlay/releases/download/v2.2.0.3/s6-overlay-aarch64-installer --location --output /tmp/s6-overlay-installer \
  ; fi \
  && \
  chmod +x \
    /tmp/s6-overlay-installer \
  && \
  /tmp/s6-overlay-installer / \
  && \
  rm /tmp/s6-overlay-installer

ENV \
    DATA_CONFIG_DIR=/config \
    DATA_DO_MIGRATIONS=true \
    XDG_CONFIG_HOME=/config/.cache \
    DATA_ENABLE_SERVER=true \
    DATA_PORT=8000 \
    PYTHONUNBUFFERED=1 \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2

WORKDIR /config

EXPOSE 8000 5555

# Set command
CMD ["/init"]

# Copy rootfs
COPY rootfs /

# Install app
COPY src/ /app/src/
COPY pyproject.toml /app/
COPY README.md /app/

RUN \
  python3 -m pip install --break-system-packages /app/
  