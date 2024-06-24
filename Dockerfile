FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    sqlite3 \
    && apt-get clean

# Install Chrome driver for selenium
RUN apt-get update && apt-get install -y wget unzip net-tools lsof && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

WORKDIR /app

# Create and activate a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements file and install dependencies
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# 5000 port for Flask
EXPOSE 5000

# 指定主程式為app.py
CMD ["python", "app.py"]
