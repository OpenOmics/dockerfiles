#!/bin/bash
# Enable conda for this shell session
. /opt/conda/etc/profile.d/conda.sh
# Activate the specific environment
conda activate SpecImmune
# Execute the command passed to the Docker container (e.g., from CMD)
exec "$@"
