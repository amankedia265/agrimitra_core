# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code (including the 'agent' folder)
COPY . .

# Command to run the app. Cloud Run provides the $PORT environment variable.
CMD ["uvicorn", "web:app", "--host", "0.0.0.0", "--port", "8080"]

# CMD ["gunicorn", "web:app", "--bind", "0.0.0:8080"]