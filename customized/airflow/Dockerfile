# Use the official Ubuntu 19.04 LTS image as the base image
FROM ubuntu:19.04

# Add TimeZone
ENV TIMEZONE=Asia/Kolkata

# Add WORKDIR
WORKDIR /app

# Set non-interactive mode for the installation
ENV DEBIAN_FRONTEND=noninteractive

# Update sources.list to use old-releases.ubuntu.com for Disco
COPY ./source.list /etc/apt/sources.list

# Update and install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        freetds-bin \
        krb5-user \
        ldap-utils \
        libffi6 \
        libsasl2-2 \
        libsasl2-modules \
        libssl1.1 \
        locales  \
        lsb-release \
        sasl2-bin \
        sqlite3 \
        unixodbc \
        build-essential \
        zlib1g-dev \
        libncurses5-dev \
        libgdbm-dev \
        libnss3-dev \
        libssl-dev \
        libreadline-dev \
        libffi-dev \
        libsqlite3-dev \
        wget \
        libbz2-dev \
        curl \
        ca-certificates \
        apt-transport-https \
        apt-utils \
        dumb-init \
        gosu krb5-user \
        libgeos-dev \
        libxmlsec1 \
        lsb-release \
        openssh-client \
        python3-selinux \
        rsync \
        netcat-openbsd \
        libldap-2.4-2 \
        postgresql-client \
        cmake \
        sudo \
        git \
        vim

# Set the CURL_CA_BUNDLE environment variable
ENV CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt


# Set the locale to avoid potential issues with encoding
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# Set up Conda environment with Python 3.8.12
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh

# Add Conda to the system PATH
ENV PATH=/opt/conda/bin:$PATH

# Clean up and creating user airflow
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* \
    mkdir script

COPY ./balte/ /app/balte_live

RUN conda env create -f ./balte_live/environment.yml && \
    echo "source activate env_balte_0.0.3" >> /etc/bash.bashrc

# Install Apache Airflow Latest Version
ARG AIRFLOW_VERSION=2.2.2
ARG CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.8.txt"
RUN /opt/conda/envs/env_balte_0.0.3/bin/pip install psycopg2-binary
RUN /opt/conda/envs/env_balte_0.0.3/bin/pip install "apache-airflow[async,postgres,google]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Set environment variables for Conda activation
ENV CONDA_EXE=/opt/conda/bin/conda
ENV CONDA_PREFIX=/opt/conda/envs/env_balte_0.0.3
ENV CONDA_PROMPT_MODIFIER=(env_balte_0.0.3)

# Copy the entrypoint script into the image
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

# Installing additional dependencies
RUN /opt/conda/envs/env_balte_0.0.3/bin/pip install -r /app/balte_live/requirements.txt


# CMD to run entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
