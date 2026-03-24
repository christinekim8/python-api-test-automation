FROM python:3.13-slim

# Install Java runtime, curl, and utilities required for Allure CLI
RUN apt-get update && apt-get install -y \
    openjdk-21-jre-headless \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Download and install Allure CLI
RUN curl -o allure.zip -L \
    https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.zip \
    && unzip allure.zip -d /opt/ \
    && ln -s /opt/allure-2.27.0/bin/allure /usr/local/bin/allure \
    && rm allure.zip

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source code into the container
COPY . .

# Create directories for Allure results and generated reports
RUN mkdir -p /app/allure-results /app/allure-report