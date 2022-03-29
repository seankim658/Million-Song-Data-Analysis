# Build base Docker image with PostgreSQL
FROM postgres:latest

# Swap to root to avoid using `sudo`
USER root

# Install Python 3.9 for use in loading data
RUN apt-get update && \
	apt-get install -y software-properties-common gcc wget && \
	apt-get update && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables for container
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash
ENV PATH="${CONDA_DIR}/bin:${PATH}"

# CONDA_MIRROR is a mirror prefix to speed up downloading
ARG CONDA_MIRROR=https://github.com/conda-forge/miniforge/releases/latest/download

# Install Miniforge, conda, and mamba for installing
# the necessary Python and Python packages
RUN set -x && \
    miniforge_arch=$(uname -m) && \
    miniforge_installer="Mambaforge-Linux-${miniforge_arch}.sh" && \
    wget --quiet "${CONDA_MIRROR}/${miniforge_installer}" && \
    /bin/bash "${miniforge_installer}" -f -b -p "${CONDA_DIR}" && \
    rm "${miniforge_installer}" && \
    mamba list python | grep '^python ' | tr -s ' ' | cut -d ' ' -f 1,2 >> "${CONDA_DIR}/conda-meta/pinned" && \
    conda update --all --quiet --yes && \
    conda clean --all -f -y && \
    rm -rf "/home/.cache/yarn"

# Install necessary Python packages
RUN mamba install --quiet --yes \
	psycopg2 && \
	mamba clean --all -f -y