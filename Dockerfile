# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install necessary OS utilities
RUN apt-get update \
    && apt-get install -y wget unzip \
    && rm -rf /var/lib/apt/lists/*

# Download and install Chrome
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chrome-linux64.zip \
    && unzip chrome-linux64.zip -d /usr/bin/ \
    && rm chrome-linux64.zip

# Download and install ChromeDriver
# Download and install ChromeDriver
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chromedriver-linux64.zip \
    && mkdir -p /tmp/chromedriver \
    && unzip chromedriver-linux64.zip -d /tmp/chromedriver/ \
    && ls -la /tmp/chromedriver/ \
    && mv /tmp/chromedriver/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm chromedriver-linux64.zip \
    && rm -rf /tmp/chromedriver




# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 4444 available to the world outside this container
EXPOSE 4444

# Run app.py when the container launches
CMD ["python", "./main.py"]
