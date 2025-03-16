# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables to avoid python buffering output (useful for logging in Docker)
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Install system dependencies and pip
RUN apt-get update \
    && apt-get install -y \
    gcc \
    libpq-dev \
    && pip install --upgrade pip

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the entire project to the container
COPY . /app/

# Expose the port the app will run on (8000 for Django default dev server)
EXPOSE 8000 8001

# Command to run the Django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
