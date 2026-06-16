FROM python:3.11-slim

WORKDIR /app

# Install build dependencies and runtime dependencies
COPY requirements.txt ./
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Ensure directories exist
RUN mkdir -p /app/uploads /app/data

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
