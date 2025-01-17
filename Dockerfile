# Use the official Python base image
FROM python:3.9-slim

# Install required dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the environment variable for the Chromium binary location
ENV CHROMIUM_BINARY=/usr/bin/chromium

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Set the working directory
WORKDIR /app

# Copy your application code
COPY . .

# Expose the port that your Flask app will run on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
