import pytest
import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Constants
PORT = 8000
# Calculate paths relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, 'app')


@pytest.fixture(scope="session", autouse=True)
def start_server():
    """
    Starts the web server before any tests run, and stops it after all tests finish.
    """
    os.chdir(WEB_DIR)
    server = HTTPServer(('localhost', PORT), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    yield f"http://localhost:{PORT}"  # We yield the URL so tests can use it

    server.shutdown()
    os.chdir(BASE_DIR)


@pytest.fixture(scope="module")
def driver():
    """
    Sets up the Headless Chrome Driver.
    """
    chrome_options = Options()  # Creates a settings object to configure the browser before it starts

    chrome_options.add_argument("--headless")  # Runs the browser in the background without a visible UI window (Crucial for CI servers)
    chrome_options.add_argument("--no-sandbox")  # Disables the security sandbox; prevents crashes on Linux/Docker where the user lacks permissions
    chrome_options.add_argument("--disable-dev-shm-usage")  # Forces Chrome to use the disk for memory instead of RAM; prevents crashes in environments with low shared memory

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield driver

    driver.quit()