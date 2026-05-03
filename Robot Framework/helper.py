import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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




def extract_table_to_dataframe(driver):
    try:
        wait = WebDriverWait(driver, 10)

        table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "table")))

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
                cells = col.find_elements(By.CLASS_NAME, "cell-text")
                row.append(cells[i].text.strip() if i < len(cells) else "")
            data.append(row)

        df = pd.DataFrame(data, columns=header_row)

        return df

    except Exception as e:
        print(f"Table error: {e}")
        return pd.DataFrame()
    

def read_parquet_dataset(folder_path):
    try:
        df = pd.read_parquet(folder_path)
        return df
    except Exception as e:
        print(f"Error reading parquet dataset: {e}")
        return pd.DataFrame()
    

def compare_dataframes(df1, df2):
    result = {}

    result["shape_df1"] = df1.shape
    result["shape_df2"] = df2.shape
    result["shape_equal"] = df1.shape == df2.shape

    cols1 = set(df1.columns)
    cols2 = set(df2.columns)

    result["columns_equal"] = cols1 == cols2
    result["columns_only_in_df1"] = list(cols1 - cols2)
    result["columns_only_in_df2"] = list(cols2 - cols1)

    common_cols = list(cols1 & cols2)

    df1_common = df1[common_cols].sort_index(axis=1)
    df2_common = df2[common_cols].sort_index(axis=1)

    df1_common, df2_common = df1_common.align(df2_common, join="outer", axis=0)

    try:
        diff = df1_common.compare(df2_common)
    except Exception:
        diff = "Could not compare values"

    result["value_diff"] = diff
    result["values_equal"] = diff.empty if isinstance(diff, pd.DataFrame) else False

    return result

def filter_by_partition_date(df, partition_date):
    df = df.copy()
    df.columns = df.columns.str.strip()
    if "partition_date" not in df.columns:
        raise KeyError("partition_date column not found in DataFrame")

    filtered_df = df[df["partition_date"] == partition_date]

    return filtered_df




# if __name__ == "__main__":
#     file_path = "file:///C:/Users/sofiia_ziniuk/Desktop/report.html"

#     with SeleniumWebDriverContextManager() as driver:
#         driver.get(file_path)

#         print(extract_table_to_dataframe(driver))
#         # print(read_parquet_dataset("C:\\Users\\sofiia_ziniuk\\Desktop\\parquet_data").head())
