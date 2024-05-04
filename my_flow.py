from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

def get_table_data(driver):
    # Find the table element by its ID
    table = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder2_LData"]')
    # Find all rows of the table
    rows = table.find_elements(By.TAG_NAME, "tr")

    table_data = []
    print(len(rows))
    for i, row in enumerate(rows[4:]):  # Skip the first four rows
        if i % 100 == 0:
            print(f"Processing row {i}")
        # Find all cells of the row
        cells = row.find_elements(By.TAG_NAME, "td")
        # Extract text from each cell and append to table_data
        table_data.append([cell.text for cell in cells])

    return table_data


def run_selenium():
    # import chromedriver_autoinstaller

    # chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(
    #     service=ChromiumService(
    #         ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
    #         options=options,
    #     )
    # )

    # service = webdriver.ChromeService(executable_path=chromedriver_bin)

    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(options=options)

    driver.get("https://oop.ky.gov/")

    # Find and interact with elements using Selenium
    pc_checkbox = driver.find_element(
        By.XPATH, '//*[@id="ContentPlaceHolder2_chkBoards_9"]'
    )
    pc_checkbox.click()

    all_data = []

    for letter in "AB":
        print(f"Scraping for {letter}...")
        last_name_box = driver.find_element(
            By.XPATH, '//*[@id="ContentPlaceHolder2_TLname"]'
        )
        last_name_box.clear()
        last_name_box.send_keys(letter)

        search_button = driver.find_element(
            By.XPATH, '//*[@id="ContentPlaceHolder2_BSrch"]'
        )
        search_button.click()
        time.sleep(5)
        print("---getting table data...")
        t_data = get_table_data(driver)
        print(f"---{len(t_data)} rows retrieved...")
        all_data.extend(t_data)

    return all_data
