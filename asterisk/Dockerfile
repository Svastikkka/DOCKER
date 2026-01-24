FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ASTERISK_VERSION=22.8.0

# ----------------------------
# 1. Install build dependencies
# ----------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    wget \
    curl \
    ca-certificates \
    pkg-config \
    libedit-dev \
    libssl-dev \
    libxml2-dev \
    libsqlite3-dev \
    uuid-dev \
    libjansson-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libcurl4-openssl-dev \
    libnewt-dev \
    libtool \
    subversion \
    automake \
    autoconf \
    bison \
    flex \
    sox \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# 2. Download Asterisk source
# ----------------------------
WORKDIR /usr/src

RUN wget https://downloads.asterisk.org/pub/telephony/asterisk/asterisk-${ASTERISK_VERSION}.tar.gz \
    && tar xzf asterisk-${ASTERISK_VERSION}.tar.gz \
    && rm asterisk-${ASTERISK_VERSION}.tar.gz

WORKDIR /usr/src/asterisk-${ASTERISK_VERSION}

# ----------------------------
# 3. Install bundled pjproject deps
# ----------------------------
# RUN contrib/scripts/install_prereq install

# Optional MP3 support (safe)
RUN contrib/scripts/get_mp3_source.sh

# ----------------------------
# 4. Configure Asterisk (with bundled PJSIP)
# ----------------------------
RUN ./configure

# ----------------------------
# 5. Build & install
# ----------------------------
RUN make -j$(nproc) \
    && make install \
    && make samples \
    && make config

# ----------------------------
# 6. Runtime directories
# ----------------------------
RUN mkdir -p /var/run/asterisk \
    && mkdir -p /var/log/asterisk \
    && mkdir -p /var/lib/asterisk \
    && mkdir -p /etc/asterisk

# ----------------------------
# 7. Expose SIP & RTP ports
# ----------------------------
EXPOSE 5060/udp
EXPOSE 5060/tcp
EXPOSE 10000-20000/udp

# ----------------------------
# 8. Run Asterisk (foreground)
# ----------------------------
CMD ["asterisk", "-fvvvv"]
