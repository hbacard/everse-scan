# syntax=docker/dockerfile:1
#
# Multi-stage build: builder produces the wheel, runtime installs it.
# Smaller final image + no build tooling in production.

# ---- Builder stage ----
FROM python:3.13-slim AS builder

WORKDIR /build

# Copy only what is needed to build the wheel
COPY pyproject.toml README.md ./
COPY src/ ./src/

RUN pip wheel --no-cache-dir --wheel-dir /wheelhouse .

# ---- Runtime stage ----
FROM python:3.13-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /work

# Install the wheel built in the previous stage (no network resolution)
COPY --from=builder /wheelhouse /wheelhouse
RUN pip install --no-cache-dir --no-index --find-links=/wheelhouse everse-scan

# Run as a non-root user
RUN useradd --create-home --shell /usr/sbin/nologin appuser
USER appuser

ENTRYPOINT ["everse-scan"]
CMD ["--help"]
