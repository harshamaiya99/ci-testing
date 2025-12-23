import pytest
import csv
import os
from selenium.webdriver.common.by import By


# --- Data Loading Logic ---
def get_csv_data():
    """Reads the CSV file and returns a list of tuples for parameterization."""
    data_path = os.path.join(os.path.dirname(__file__), 'test_data.csv')
    test_data = []
    with open(data_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Skip header if your CSV has one, otherwise keep as is
            # if row[0] == 'num1': continue
            test_data.append(tuple(row))
    return test_data


# --- The Test ---
@pytest.mark.parametrize("num1, num2, expected", get_csv_data())
def test_calculator(driver, start_server, num1, num2, expected):
    # 'start_server' fixture returns the URL string we yielded in conftest.py
    base_url = start_server

    # 1. Navigate
    driver.get(base_url)

    # 2. Interact
    driver.find_element(By.ID, "num1").clear()
    driver.find_element(By.ID, "num1").send_keys(num1)

    driver.find_element(By.ID, "num2").clear()
    driver.find_element(By.ID, "num2").send_keys(num2)

    driver.find_element(By.ID, "calculateBtn").click()

    # 3. Verify
    result_text = driver.find_element(By.ID, "result").text
    assert result_text == expected, f"Failed: {num1} + {num2} = {result_text} (Expected {expected})"