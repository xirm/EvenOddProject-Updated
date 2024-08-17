# Base image
FROM python:3.9-slim

# Install git and git-lfs
RUN apt-get update && \
    apt-get install -y git wget && \
    wget https://github.com/git-lfs/git-lfs/releases/download/v3.4.0/git-lfs-linux-amd64-v3.4.0.tar.gz && \
    tar -xzf git-lfs-linux-amd64-v3.4.0.tar.gz && \
    ./install.sh && \
    git lfs install && \
    rm -rf git-lfs-linux-amd64-v3.4.0.tar.gz install.sh

# Set work directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port (if needed)
EXPOSE 8000

# Command to run your application
CMD ["python", "predict_and_notify.py"]
