# Base image for scenicplus,
# uses Ubuntu mantic
FROM ubuntu:23.10

# Depedencies of scenicplus:
# https://github.com/aertslab/scenicplus
# @TLDR: 
#   - python/3.11
#   - pip3
#   - scenicplus
#   - git
LABEL maintainer=kuhnsa@nih.gov

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
        unzip \
        wget \
        zlib1g-dev \
    && apt-get clean && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set the locale
RUN localedef -i en_US -f UTF-8 en_US.UTF-8

# Make python3 the default interpreter
# and install Python Packages 
RUN ln -sf /usr/bin/python3.11 /usr/bin/python
RUN pip3 install --break-system-packages --upgrade pip 

############### INSTALL ################
# Install scenicplus from Github,
# https://github.com/aertslab/scenicplus
# Dependencies already satisfied: 
# - python3.11
RUN git clone https://github.com/aertslab/scenicplus /opt2/scenicplus \
        && cd /opt2/scenicplus \
        && pip install --break-system-packages .

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
# Add Dockerfile and export important 
# environment variables
ADD Dockerfile /opt2/scenicplus.dockerfile
RUN chmod -R a+rX /opt2
ENV PATH="/opt2/which-2.21/bin:${PATH}"
WORKDIR /data2