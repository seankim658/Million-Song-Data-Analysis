# Build base Docker image with PostgreSQL
FROM postgres:latest

# Update default PostgreSQL environment variables
# and set conda environment variables
ENV POSTGRES_USER db_user
ENV POSTGRES_PASSWORD LetMeIn
ENV POSTGRES_DB msd_db
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash
ENV PATH="${CONDA_DIR}/bin:${PATH}"

# Swap to root to avoid using `sudo`
USER root

# Install base packages for future use
RUN apt-get update && \
    apt-get install -y software-properties-common gcc wget && \
    apt-get update && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

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
    psycopg2 \
    pandas \
    numpy \
    h5py \
    pytables \
    sqlalchemy && \
    mamba clean --all -f -y

# Download data to seed database, decompress
# file, and remove tar when done
RUN wget --quiet http://labrosa.ee.columbia.edu/~dpwe/tmp/millionsongsubset.tar.gz && \
    tar -xvzf millionsongsubset.tar.gz && \
    rm -f millionsongsubset.tar.gz

# Copy database seeding scripts
COPY seed_database.py .
COPY seed_database.sh /docker-entrypoint-initdb.d
