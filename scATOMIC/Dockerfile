# Use a Posit/Rocker image as the base
FROM rocker/rstudio:latest

# Install Python and related development tools
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    python3-numpy \
    python3-pandas \
    python3-igraph \
    # Clean up apt lists
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --break-system-packages magic-impute

# Set a system-wide environment variable for reticulate to use the correct Python executable
ENV RETICULATE_PYTHON=/usr/bin/python3
ADD scATOMIC_install.R /usr/bin/install_deps_scatomic.R
RUN chmod +x /usr/bin/install_deps_scatomic.R; Rscript /usr/bin/install_deps_scatomic.R
