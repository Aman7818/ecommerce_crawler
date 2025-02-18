import time
import re
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Predefined URL Patterns for Specific Platforms
from crawler.models import ProductURL

PLATFORM_PATTERNS = {

    "flipkart.com": re.compile(r"https://www\.flipkart\.com/.+/p/\w+"),

}


class WebDriverSetup:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.service = Service(ChromeDriverManager().install())

    def get_driver(self):
        driver = webdriver.Chrome(service=self.service, options=self.options)
        return driver


class WebCrawler:
    def __init__(self, domains):
        self.domains = domains
        self.driver_setup = WebDriverSetup()
        self.product_urls = set()

    def extract_links(self, page_source, base_url, domain):
        soup = BeautifulSoup(page_source, "html.parser")
        links = set(urljoin(base_url, a["href"]) for a in soup.find_all("a", href=True))
        return self.filter_product_links(links, domain)

    def filter_product_links(self, links, domain):
        parsed_domain = urlparse(domain).netloc.replace("www.", "")
        pattern = PLATFORM_PATTERNS.get(parsed_domain)
        if pattern:
            return {link for link in links if pattern.match(link)}
        return links

    def selenium_crawl(self, domain):
        print(f"Crawling {domain} with Selenium...")
        driver = self.driver_setup.get_driver()
        driver.get(domain)
        time.sleep(3)

        # Scroll for dynamic content loading
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        page_source = driver.page_source
        driver.quit()

        links = self.extract_links(page_source, domain, domain)
        self.product_urls.update(links)

    def run_crawler(self):
        result = {}
        for domain in self.domains:
            self.selenium_crawl(domain)
            result[domain] = list(self.product_urls)  # Store URLs under the domain key
        print("Crawling completed.")
        for url in result.get(domain, []):
            try:
                if len(url) > 2083:
                    print(f"Skipping long URL: {url}")
                    continue

                ProductURL.objects.get_or_create(domain=domain, url=url)
            except Exception as e:
                print(f"Skipping URL due to error: {url} - Error: {e}")

        return result

