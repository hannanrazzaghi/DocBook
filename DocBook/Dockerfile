# Use a stable and smaller Python version for better reliability
FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies (gcc, libpq-dev, etc.)
# Use slim version to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt and install dependencies first to optimize caching
COPY requirements.txt /app/

# Install Python dependencies in a single layer
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Expose the application port
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
