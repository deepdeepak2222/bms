# Use the official Python image from the Docker Hub
# alpine is very minimal image
FROM python:3.9-alpine

# Set environment variables to prevent Python from writing .pyc files to disc
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apk update \
    && apk add --no-cache \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    libpq \
    build-base \
    linux-headers \
    pcre-dev \
    libffi-dev \
    openssl-dev \
    jpeg-dev \
    zlib-dev

# Set working directory
WORKDIR /app/bms/

# Copy the requirements file to the working directory
# COPY ../requirements.txt /app/bms # When docker-compose is in development folder
COPY requirements.txt /app/bms

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/bms
COPY . /app/bms

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the application
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
