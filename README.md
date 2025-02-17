# 🕷️ Django Celery Web Scraper

This project is a **Django-based web scraper** that uses **Celery** for asynchronous task execution. Given a list of domains, the scraper fetches product URLs from each domain **concurrently** and allows checking task statuses via an API.

## 🚀 Features
- **Asynchronous Scraping**: Uses **Celery** and **Redis** to scrape multiple domains simultaneously.
- **Task Tracking**: Check the status of scraping tasks using Celery task IDs.
- **Django REST API**: Exposes endpoints to start scraping tasks and check statuses.
- **Docker Support**: Easy deployment with Docker and Kubernetes.

## 📦 Installation

### 1️⃣ Clone the Repository
```sh
git clone 
cd django-celery-scraper
```

### 2️⃣ Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Start Redis (Required for Celery)
Make sure you have **Redis** installed and running. If not, install Redis:

- **Linux/macOS** (Homebrew):
  ```sh
  brew install redis
  brew services start redis
  ```
- **Windows**: Use **Docker**:
  ```sh
  docker run -d -p 6379:6379 redis
  ```

### 5️⃣ Apply Migrations
```sh
python manage.py migrate
```

### 6️⃣ Start Django Server
```sh
python manage.py runserver
```

### 7️⃣ Start Celery Worker
Run Celery to process tasks asynchronously:
```sh
celery -A your_project_name worker --loglevel=info
```

---

## 📡 API Endpoints

### **1️⃣ Start Scraping**
**Endpoint**: `POST /start_scraping/`  
**Payload (JSON)**:
```json
{
  "domains": ["https://www.bewakoof.com/", "https://www.gyros.farm/"]
}
```
**Response**:
```json
{
  "tasks": [
    {"domain": "https://www.bewakoof.com/", "task_id": "abc123"},
    {"domain": "https://www.gyros.farm/", "task_id": "xyz456"}
  ],
  "status": "Tasks started"
}
```

---

### **2️⃣ Check Task Status**
**Endpoint**: `GET /task_status/{task_id}/`  
**Example**:
```sh
curl http://127.0.0.1:8000/task_status/abc123/
```
**Response (Pending)**:
```json
{
  "task_id": "abc123",
  "status": "PENDING",
  "result": null
}
```

**Response (Success)**:
```json
{
  "task_id": "abc123",
  "status": "SUCCESS",
  "result": {
    "domain": "https://www.bewakoof.com/",
    "product_urls": ["https://www.bewakoof.com/product-1", "https://www.bewakoof.com/product-2"]
  }
}
```

---

## 💪 Docker Setup (Optional)
Run the project using **Docker**:
```sh
docker-compose up --build
```

---

## 🛠 Technologies Used
- **Django** - Backend framework
- **Celery** - Asynchronous task queue
- **Redis** - Message broker for Celery
- **BeautifulSoup / Scrapy** - Web scraping libraries
- **Docker** - Containerized deployment

---

## 🔥 Contributing
1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch`
3. Make your changes and commit: `git commit -m 'Added new feature'`
4. Push the changes: `git push origin feature-branch`
5. Submit a pull request 🚀

---


## ✨ Contact
For questions or support, reach out to **Aman** at **yadavaman4491@gmail.com**.

