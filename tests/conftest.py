import sys
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from dotenv import load_dotenv

# Dynamically add the project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

load_dotenv()

@pytest.fixture(scope="function")
def driver():
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--headless=new")  # Optional for CI/CD runs

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://demo.applitools.com")