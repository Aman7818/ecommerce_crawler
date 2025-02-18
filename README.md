
# Django Web Scraping API

## Overview

This project is a Django-based web scraping API that extracts product URLs from various eCommerce platforms. The API takes domain URLs as input and asynchronously crawls them using Selenium and BeautifulSoup.

## Features

- Accepts a list of domain URLs to scrape.
- Uses Selenium to load web pages dynamically and extract product URLs.
- Supports multiple platforms with predefined URL patterns.
- Runs scraping tasks asynchronously.
- Stores extracted product URLs in a MySQL database.
- Provides an API to scrape data and return the results.

## Technologies Used

- **Django 4.2** (Web framework)
- **Selenium** (For automated web scraping)
- **BeautifulSoup** (For parsing HTML content)
- **MySQL** (Database for storing extracted URLs)
- **Threading** (For asynchronous task execution)

## Installation

### Prerequisites

- Python 3.10+
- MySQL database setup
- Chrome browser installed
- Chromedriver (Managed automatically by `webdriver-manager`)

### Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/Aman7818/ecommerce_crawler.git
   cd <project-directory>
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Configure the database settings in `settings.py`. Use the environment variables for database credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': os.getenv('DB_NAME'),
           'USER': os.getenv('DB_USER'),
           'PASSWORD': os.getenv('DB_PASSWORD'),
           'HOST': os.getenv('DB_HOST'),
           'PORT': os.getenv('DB_PORT'),
       }
   }
   ```
   Add the following environment variables to your `.env` file:
   ```
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=3306
   ```

5. Run database migrations:
   ```sh
   python manage.py migrate
   ```

6. Start the Django server:
   ```sh
   python manage.py runserver
   ```

## API Usage

### Endpoint: `/crawl/`

**Method:** `POST`

**Request Body:**

```json
{
    "domains": [
        "https://www.amazon.in/s?k=laptops",
        "https://www.flipkart.com/search?q=smartphones"
    ]
}
```

**Response:**

```json
{
    "message": "Crawling started in background"
}
```

This endpoint starts the web scraping task for a list of domains asynchronously.

### Endpoint: `/scrape/`

**Method:** `POST`

**Request Body:**

```json
{
    "domains": [
        "https://www.amazon.in/s?k=laptops",
        "https://www.flipkart.com/search?q=smartphones"
    ]
}
```

**Response:**

```json
{
    "message": "Crawling completed",
    "data": [
        "https://www.amazon.in/product1",
        "https://www.flipkart.com/product2"
    ]
}
```

This endpoint returns the scraped data (product URLs) from the provided domain URLs.

## How It Works

1. The API receives a list of domain URLs.
2. For the `/crawl/` endpoint, each domain is processed asynchronously to avoid blocking the request.
3. Selenium loads the webpage, scrolls to load dynamic content, and extracts product URLs.
4. URLs matching predefined patterns are saved to the database.
5. For the `/scrape/` endpoint, the scraping process completes synchronously, and the product URLs are returned in the response.

## Notes

- Scraping eCommerce websites must comply with their Terms of Service.
- Running multiple requests can consume significant system resources.
- Ensure that your Chrome browser and Chromedriver versions are compatible.


