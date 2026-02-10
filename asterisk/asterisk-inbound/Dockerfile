FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ASTERISK_VERSION=22.8.1

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
# 3. Optional MP3 support
# ----------------------------
RUN contrib/scripts/get_mp3_source.sh

# ----------------------------
# 4. Configure (bundled pjproject)
# ----------------------------
RUN ./configure

# ----------------------------
# 5. Enable PJSIP modules (NON-INTERACTIVE)
# ----------------------------
# ----------------------------
# 5. Enable required modules (Asterisk 22 compatible)
# ----------------------------
RUN make menuselect.makeopts && \
    menuselect/menuselect \
      --enable chan_pjsip \
      --enable res_pjsip \
      --enable res_pjsip_authenticator_digest \
      --enable res_pjsip_endpoint_identifier_ip \
      --enable res_pjsip_registrar \
      --enable res_pjsip_session \
      --enable bridge_simple \
      --enable bridge_native_rtp \
      --enable codec_ulaw \
      --enable codec_alaw \
      menuselect.makeopts
# ----------------------------
# 6. Build & install
# ----------------------------
RUN make -j$(nproc) \
    && make install \
    && make samples \
    && make config \
    && ldconfig

# ----------------------------
# 7. Runtime directories
# ----------------------------
RUN mkdir -p /var/run/asterisk \
    /var/log/asterisk \
    /var/lib/asterisk \
    /etc/asterisk

# ----------------------------
# 8. Expose SIP & RTP ports
# ----------------------------
EXPOSE 5060/udp
EXPOSE 5060/tcp
EXPOSE 10000-20000/udp

# ----------------------------
# 9. Run Asterisk
# ----------------------------
CMD ["asterisk", "-fvvvv"]
