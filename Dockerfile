# --- Stage 1: Build Stage ---
# Use a full Python image to build dependencies, which may have build-time requirements
FROM python:3.9-alpine AS builder

WORKDIR /usr/src/app

# Install build dependencies required for some Python packages
RUN apk add --no-cache build-base

# Copy requirements file and install dependencies into a virtual environment
COPY requirements.txt ./
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 2: Final Stage ---
# Use a slim image for the final product to reduce size
FROM python:3.9-alpine

# Create a non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

WORKDIR /home/appuser/app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code
COPY ./app ./app
COPY ./run.py .

# Make the virtual environment's Python the default
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port the app runs on
EXPOSE 5000

# Run the application with Gunicorn, a production-ready web server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]