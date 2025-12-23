import pytest
import csv
import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- 1. Server Configuration for CI ---
PORT = 8000
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, 'web-app')


@pytest.fixture(scope="session", autouse=True)
def start_server():
    """Starts a simple HTTP server to serve the web-app folder."""
    os.chdir(WEB_DIR)  # Change to web directory to serve index.html at root
    server = HTTPServer(('localhost', PORT), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield
    server.shutdown()
    os.chdir(BASE_DIR)  # Reset CWD


# --- 2. Browser Configuration ---
@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Crucial for CI environments
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()


# --- 3. Data Driven Utility ---
def get_csv_data():
    data_path = os.path.join(os.path.dirname(__file__), 'test_data.csv')
    test_data = []
    with open(data_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            test_data.append(tuple(row))  # Returns [(10, 20, 30), ...]
    return test_data


# --- 4. The Test ---
@pytest.mark.parametrize("num1, num2, expected", get_csv_data())
def test_calculator(driver, num1, num2, expected):
    # Navigate to local server
    driver.get(f"http://localhost:{PORT}")

    # Interact with elements
    driver.find_element(By.ID, "num1").clear()
    driver.find_element(By.ID, "num1").send_keys(num1)

    driver.find_element(By.ID, "num2").clear()
    driver.find_element(By.ID, "num2").send_keys(num2)

    driver.find_element(By.ID, "calculateBtn").click()

    # Check result
    result_text = driver.find_element(By.ID, "result").text
    assert result_text == expected, f"Failed for input {num1}+{num2}. Expected {expected}, got {result_text}"