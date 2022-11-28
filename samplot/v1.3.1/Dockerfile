# Dockerfile for samplot:v1.3.1
# https://github.com/ryanlayer/samplot
# There is an issue with the latest conda
# release of samplot, building a docker
# image with the latest Github release.
# Using Ubuntu Focal (20.04 LTS) as base image
FROM ubuntu:20.04
LABEL maintainer=kuhnsa@nih.gov

# Create Container filesystem specific 
# working directory and opt directories
# to avoid collisions with host filesyetem 
RUN mkdir -p /opt2 && mkdir -p /data2
WORKDIR /opt2 

# Set time zone to US east coast 
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

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
        git \
        gzip \
        libz-dev \
        libbz2-dev \
        liblzma-dev \
        locales \
        pandoc \
        python3 \
        python3-pip \
        samtools \
        unzip \
        wget \
    && apt-get clean && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set the locale
RUN localedef -i en_US -f UTF-8 en_US.UTF-8

# Make python3 the default interpreter
# and install python packages
RUN ln -sf /usr/bin/python3.8 /usr/bin/python \
    && ln -sf /usr/bin/python3.8 /usr/bin/python3

# Install samplot (v1.3.1)
# As of 11/28/2022, there is no tagged release
# for the latest version of samplot (v1.3.1),
# cloning the repo and checkout out the latest
# commit ID: 70cad157e7764c59a6149538305dcccaea8e11b9
RUN git clone https://github.com/ryanlayer/samplot.git \
    && cd samplot \
    && git checkout 70cad157e7764c59a6149538305dcccaea8e11b9 \
    && pip install --upgrade pip \
    && pip install . \
    && pip install --upgrade numpy 

# Add Dockerfile and export env variables
ADD Dockerfile /opt2/Dockerfile
RUN chmod -R a+rX /opt2 
ENV PATH="/opt2:$PATH"
WORKDIR /data2