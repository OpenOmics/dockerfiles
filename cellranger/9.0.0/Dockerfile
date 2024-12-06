# Base image for cellranger,
# uses Ubuntu Jammy
FROM ubuntu:22.04

############### ABOUT ###############
# Depedencies of cellranger:
# • https://github.com/10XGenomics/cellranger
# • https://www.10xgenomics.com/support/software/cell-ranger/downloads/cr-system-requirements
# • https://www.10xgenomics.com/support/software/cell-ranger/downloads
# @TLDR: 
#   • Ubuntu >= 14.04
#   • cellranger mkfastq requires bcl2fastq2 (v2.20 or later),
#     Down the RPM file and copy into into the same directory
#     as this dockerfile. 
#      •  https://emea.support.illumina.com/downloads/bcl2fastq-conversion-software-v2-20.html   
LABEL maintainer=kuhnsa@nih.gov

############### ARGS ################
# bcl2fastq2 RPM file, see README.md for more info
ARG BCL2FQ_RPM="bcl2fastq2-v2.20.0.422-Linux-x86_64.rpm"
# Cellranger download URL, see README.md for more info,
# the URL will look like and it can be found as part
# of the download curl/wget commands:
# https://cf.10xgenomics.com/releases/cell-exp/cellranger-9.0.0.tar.gz?Expires=123&Key-Pair-Id=ABC&Signature=1a2b3c4d..."
ARG CELLRANGER_URL 

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
        alien \
        build-essential \
        bzip2 \
        ca-certificates \
        curl \
        gawk \
        git \
        gzip \
        locales \
        # python3.10
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
RUN ln -sf /usr/bin/python3.10 /usr/bin/python
RUN pip3 install -U pip \
        && pip3 install scipy numpy pandas

############### INSTALL ################
# Installs bcl2fastq2 (v2.20.0.422), 
# `cellranger mkfastq` needs this to
# convert bcl files to fastq files,
# before running `docker build` the
# RPM file will need to be downloaded
# from Illumina's website and copied
# into the same directory as this
# dockerfile. Download the linux
# RPM from here (after logging in), 
# unzip the download, and copy it 
# into this folder:
# https://emea.support.illumina.com/downloads/bcl2fastq-conversion-software-v2-20.html
COPY ${BCL2FQ_RPM} /opt2/bcl2fastq2.rpm
RUN alien -i /opt2/bcl2fastq2.rpm \
        && rm -f /opt2/bcl2fastq2.rpm


# Install cellranger 9.0.0, requires a
# 10xgenomics account to download, and
# the download URL, which can be found
# on the downloads page:
# https://www.10xgenomics.com/support/software/cell-ranger/downloads#download-links 
RUN curl -o /opt2/cellranger-9.0.0.tar.gz "${CELLRANGER_URL}" \
        && tar -xvf /opt2/cellranger-9.0.0.tar.gz -C /opt2/ \
        && rm /opt2/cellranger-9.0.0.tar.gz 

# Install GNU which, increases compatability
# with which distros included with Debian/Rocky
# linux installations, this version of which
# includes extra options that the ubuntu version 
# does not have. The gnu verison is backwards 
# compatiable with the ubunutu version.
RUN wget --no-check-certificate -O /opt2/which.tar.gz https://ftp.gnu.org/gnu/which/which-2.21.tar.gz \
        && tar -xvf /opt2/which.tar.gz -C /opt2/ \
        && rm /opt2/which.tar.gz \
        && cd /opt2/which-2.21/ \
        && ./configure --prefix=/opt2/which-2.21 \
        && make \
        && make install
WORKDIR /opt2

################ POST #################
# Add Dockerfile and export important 
# environment variables
ADD Dockerfile /opt2/cellranger_9-0-0.dockerfile
RUN chmod -R a+rX /opt2
ENV PATH="/opt2/which-2.21/bin:/opt2/cellranger-9.0.0:${PATH}"
WORKDIR /data2