# Use official Python 3.5 slim image for exact bytecode compatibility
FROM python:3.5-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy repository files into the container
COPY . /app

# Run the test suite by default
CMD ["python", "tests/run_all_tests.py"]
