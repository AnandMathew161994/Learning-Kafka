# Dockerfile for producer
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install the necessary Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app files into the container
COPY . /app

# Default command to run producer.py
CMD ["python", "producer.py"]

