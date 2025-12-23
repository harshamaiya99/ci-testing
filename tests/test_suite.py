import pytest
import csv
import os
from selenium.webdriver.common.by import By


# --- Data Loading Logic ---
def get_csv_data():
    """Reads the CSV file and returns a list of lists for parameterization."""
    data_path = os.path.join(os.path.dirname(__file__), 'test_data.csv')
    test_data = []
    with open(data_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            test_data.append(row)

    return test_data


# --- The Test ---
# Pytest handles lists of lists exactly the same way as lists of tuples
@pytest.mark.parametrize("row", get_csv_data())
def test_calculator(driver, start_server, row):
    # 'start_server' fixture returns the URL string we yielded in conftest.py
    base_url = start_server

    num1 = row["num1"]
    num2 = row["num2"]
    expected = row["expected"]

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