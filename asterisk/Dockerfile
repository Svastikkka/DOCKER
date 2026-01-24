FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    ca-certificates \
    && apt-get update \
    && apt-get install -y \
    asterisk \
    && rm -rf /var/lib/apt/lists/*

CMD ["asterisk", "-f"]