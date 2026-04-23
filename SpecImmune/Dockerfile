# Use Ubuntu as the base image
FROM ubuntu:latest

# Install necessary packages and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    software-properties-common \
    curl \
    git \
    unzip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /SpecImmune

# Define SHELL
SHELL ["/bin/bash", "-c"] 

RUN git clone https://github.com/deepomicslab/SpecImmune.git /SpecImmune
RUN cd /SpecImmune; git checkout 96c41fcf7b7b822cc45bd511a7538fc3d879a227

# Download and install Miniconda
RUN wget -c https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p /opt/conda \
    && rm /tmp/miniconda.sh

# Add Conda to PATH for build steps below
ENV PATH="/opt/conda/bin:/SpecImmune/bin:${PATH}"

# active conda environment on entry
COPY docker/entrypoint.sh /opt/conda/bin/entrypoint.sh
RUN chmod +x /opt/conda/bin/entrypoint.sh

RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# Update Conda
RUN conda update -n base -c defaults conda -y && \
    conda clean --all && \
    conda env create -p /opt/conda/envs/SpecImmune -f /SpecImmune/environment.yml && \
    conda init
RUN echo "conda activate SpecImmune" >> ~/.bashrc

# Make SpecImmune the default environment for all exec modes
# (including Singularity, which ignores ENTRYPOINT and .bashrc).
# Prepend the env's bin dir to PATH so its python/tools are found first.
ENV PATH="/opt/conda/envs/SpecImmune/bin:${PATH}" \
    CONDA_DEFAULT_ENV="SpecImmune" \
    CONDA_PREFIX="/opt/conda/envs/SpecImmune"

ENTRYPOINT ["/opt/conda/bin/entrypoint.sh"]
