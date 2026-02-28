# Dockerfile for netprobe_lite
# https://github.com/plaintextpackets/netprobe_lite/

# Default to arm32v7 if no build argument is provided
ARG BASE_IMAGE_ARCH=arm32v7

# Default to Python 3.12 if no build argument is provided
ARG PYTHON_VERSION=3.12

FROM ${BASE_IMAGE_ARCH}/python:${PYTHON_VERSION}-slim-bookworm

WORKDIR /netprobe_lite

RUN apt-get update \
    && apt-get install -y --no-install-recommends iputils-ping traceroute \
    && rm -rf /var/lib/apt/lists/*

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
COPY src/requirements.txt /netprobe_lite/requirements.txt
RUN pip install --no-cache-dir --break-system-packages -r /netprobe_lite/requirements.txt

COPY src/ /netprobe_lite/
ENV PYTHONUNBUFFERED=1

# Make sure entrypoint.sh is executable
RUN chmod +x /netprobe_lite/entrypoint.sh

ENTRYPOINT [ "/bin/bash", "/netprobe_lite/entrypoint.sh" ]
