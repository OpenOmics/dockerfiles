# Base image for HLA-LA/v1.0.4
# uses Ubuntu Jammy (LTS)
FROM ubuntu:22.04

# Depedencies of HLA-LA/v1.0.4:
#   name: hla-la
#   channels:
#     - bioconda
#   dependencies:
#     - hla-la=1.0.4
LABEL maintainer="Skyler Kuhn <kuhnsa@nih.gov>" \
    base_image="ubuntu:22.04" \
    version="v1.0.4"   \
    software="HLA-LA" \
    about.summary="Fast HLA type inference from whole-genome data" \
    about.home="https://github.com/DiltheyLab/HLA-LA" \
    about.tags="Human leukocyte antigen (HLA) type inference"

############### INIT ################
# Create Container filesystem specific 
# working directory and opt directories
# to avoid collisions with the host's
# filesystem, i.e. /opt and /data
RUN mkdir -p /opt2 && mkdir -p /data2
WORKDIR /opt2 

# Set time zone to US east coast 
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
        && echo $TZ > /etc/timezone

############### SETUP ################
# This section installs system packages 
# required for your project. If you need 
# extra system packages add them here.
RUN apt-get update \
    && apt-get -y upgrade \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        build-essential \
        bzip2 \
        ca-certificates \
        curl \
        gawk \
        git \
        gzip \
        locales \
        make \
        python3 \
        python3-pip \
        python3-pandas \
        sed \
        unzip \
        wget \
        zlib1g-dev \
    && apt-get clean && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set the locale
RUN localedef -i en_US -f UTF-8 en_US.UTF-8

# Make python3 the default interpreter
# and install Python Packages 
RUN ln -sf /usr/bin/python3.10 /usr/bin/python
RUN pip3 install --upgrade pip 

############### INSTALL ################
# Install conda and mamba and create an
# environment called, hla-la to install
# hla-la and its dependencies.
RUN mkdir -p /opt2/conda/ \
        && wget -O /opt2/conda/Miniforge3_install.sh "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" \
        && bash /opt2/conda/Miniforge3_install.sh -b -f -p /opt2/conda/ \
        && . "/opt2/conda/etc/profile.d/conda.sh" \
        && . "/opt2/conda/etc/profile.d/mamba.sh" \
        && mamba create -y --name hla-la -c bioconda -c conda-forge hla-la=1.0.4 \
        && mamba clean --all -y \
        && rm -f /opt2/conda/Miniforge3_install.sh

# Install GNU which, increases compatiability
# with which distros included with Debian/Rocky
# linux installations, this version of which
# includes extra options that the ubuntu version 
# does not have. The gnu verison is backwards 
# compatiable with the ubunutu version.
RUN mkdir -p /opt2/ \
        && wget --no-check-certificate -O /opt2/which.tar.gz https://ftp.gnu.org/gnu/which/which-2.21.tar.gz \
        && tar -xvf /opt2/which.tar.gz -C /opt2/ \
        && rm /opt2/which.tar.gz \
        && cd /opt2/which-2.21/ \
        && ./configure --prefix=/opt2/which-2.21 \
        && make \
        && make install

################ POST #################
# Add Dockerfile and export env variables
COPY Dockerfile /opt2/hla-la.dockerfile
RUN chmod -R a+rX /opt2
ENV PATH="/opt2/conda/envs/hla-la/bin:/opt2/which-2.21/bin:${PATH}"
WORKDIR /data2