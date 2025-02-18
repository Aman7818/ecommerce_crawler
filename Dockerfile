# Start with the full Python 3.11 image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CHROME_BIN=/usr/bin/google-chrome \
    DISPLAY=:99 \
    WDM_LOG_LEVEL=0 \
    WDM_PROGRESS_BAR=0

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    default-libmysqlclient-dev \
    libmariadb-dev-compat \
    wget \
    ca-certificates \
    curl \
    gnupg \
    unzip \
    ffmpeg \
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    xdg-utils \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    xvfb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Install ChromeDriver via webdriver-manager
RUN pip install webdriver-manager

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Create a script to start Xvfb and the application
RUN echo '#!/bin/bash\nXvfb :99 -screen 0 1280x1024x24 -ac +extension GLX +render -noreset &\nsleep 1\ngoogle-chrome --version && exec gunicorn Amazon_Search_Page_Scraping.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0' > /app/start.sh && \
    chmod +x /app/start.sh

# Run migrations and start server using Django's development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
