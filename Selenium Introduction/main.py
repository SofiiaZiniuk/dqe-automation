import time
import os
import pandas as pd
import csv

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class SeleniumWebDriverContextManager:
    def __init__(self):
        self.driver = None

    def __enter__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        if self.driver:
            self.driver.quit()



def extract_table_to_csv(driver):
    try:
        wait = WebDriverWait(driver, 10)

        table = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "table")))
        table = driver.find_element(By.CLASS_NAME, "table")

        columns = table.find_elements(By.CLASS_NAME, "y-column")

        header_row = []
        for col in columns:
            try:
                header_row.append(col.find_element(By.ID, "header").text.strip())
            except:
                header_row.append("")
            
        row_count = len(columns[0].find_elements(By.CLASS_NAME, "cell-text"))
        data = []

        for i in range(row_count - 1):
            row = []

            for col in columns:
                row.append(col.find_elements(By.CLASS_NAME, "cell-text")[i].text.strip())

            data.append(row)


        
        with open("table.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header_row)
            writer.writerows(data)

        print("table.csv created successfully")

    except Exception as e:
        print(f"Table error: {e}")


# =========================
# DOUGHNUT CHART (FIXED)
# =========================
def process_doughnut_chart(driver):
    try:
        wait = WebDriverWait(driver, 10)

        data = []
        surfaces = driver.find_elements(By.CSS_SELECTOR, "g.slice text.slicetext")
        for surface in surfaces:
            lines = surface.find_elements(By.CLASS_NAME, "line")
            row = []
            try:
                for line in lines:
                    text = line.text.strip()
                    row.append(text)

            except Exception as e:
                continue

            data.append(row)
        print(data)


        driver.save_screenshot("screenshot0.png")

        filters = driver.find_elements(By.CLASS_NAME, "traces")

        if not filters:
            print("No filters found")
            return
        
        headers = ["Facility Type", "Min Average Time Spent"]
        for i, row in enumerate(data):
            filename = f"doughnut{i}.csv"

            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerow(row)  
            
            print(f"{filename} created")

        for i, f in enumerate(filters, start=1):
            try:
                f.click()
                time.sleep(1)

                driver.save_screenshot(f"screenshot{i}.png")

            except (NoSuchElementException, TimeoutException):
                print(f"Filter {i} failed")
                continue

    except Exception as e:
        print(f"Doughnut error: {e}")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    file_path = "file:///C:/Users/sofiia_ziniuk/Desktop/report.html"

    with SeleniumWebDriverContextManager() as driver:
        driver.get(file_path)

        # extract_table_to_csv(driver)

        process_doughnut_chart(driver)