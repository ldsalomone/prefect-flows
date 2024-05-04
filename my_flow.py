import time
from prefect import flow

def get_table_data(page):
    table = page.locator('//*[@id="ContentPlaceHolder2_LData"]')
    table.wait_for()
    rows = table.locator("tr").all()
    print(rows)
    table_data = []
    for row in rows[4:]:
        print(row)
        table_data.append([cell.inner_text() for cell in row.locator("td").all()])
    return table_data

@flow()
def run_playwright():
    import playwright.sync_api as p

    with p.sync_playwright() as pw:

        browser = pw.chromium.connect_over_cdp(
            "wss://production-sfo.browserless.io?token=Q24V0Yq4e6ifri9f9b1b075944bcdad3f742ad9f8c"
        )
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://oop.ky.gov/")

        pc_checkbox = page.locator('//*[@id="ContentPlaceHolder2_chkBoards_9"]')
        pc_checkbox.hover()
        pc_checkbox.click()

        last_name_box = page.locator('//*[@id="ContentPlaceHolder2_TLname"]')
        last_name_box.hover()
        last_name_box.click()

        all_data = []

        for letter in "AB":
            t_data = []
            print(f"Scraping for {letter}...")
            last_name_box.fill(letter)

            search_button = page.locator('//*[@id="ContentPlaceHolder2_BSrch"]')
            search_button.hover()
            search_button.click()
            time.sleep(5)
            print("---getting table data...")
            t_data = get_table_data(page)
            print(f"---{len(t_data)} rows retrieved...")
            all_data.extend(t_data)

    return all_data
