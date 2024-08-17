# Use Python 3.9 base image
FROM python:3.9-buster

# Install dependencies
RUN apt-get update && \
    apt-get install -y git wget && \
    wget https://github.com/git-lfs/git-lfs/releases/download/v3.4.0/git-lfs-linux-amd64-v3.4.0.tar.gz && \
    tar -xzf git-lfs-linux-amd64-v3.4.0.tar.gz && \
    ./install.sh && \
    git lfs install && \
    rm -rf git-lfs-linux-amd64-v3.4.0.tar.gz install.sh && \
    git --version && \
    wget --version

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Set the default command to run the application
CMD ["python", "predict_and_notify.py"]
