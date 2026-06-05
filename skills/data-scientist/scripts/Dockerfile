# Data Scientist Skill — Test Image
# Build: docker build -t ds-test -f scripts/Dockerfile .
# Use:   docker run --rm ds-test bash scripts/test_detect_compute.sh

FROM python:3.12-slim

# Install baseline ML deps (no torch — tests verify graceful degradation)
RUN pip install --quiet --no-cache-dir \
    scipy>=1.10 \
    numpy>=1.24 \
    scikit-learn>=1.4 \
    pandas>=2.0 \
    psutil

WORKDIR /data-scientist
COPY . .
