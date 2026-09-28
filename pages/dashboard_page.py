from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # Grabs all spans inside the last column (Amount) of every row in the transaction table
    AMOUNT_CELLS = (
        By.XPATH,
        "//table[contains(@class, 'table')]//tbody/tr/td[contains(@class, 'text-right')]/span"
    )

    def get_all_amount_texts(self) -> List[str]:
        # Wait until table amount spans are loaded
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.AMOUNT_CELLS)
        )

        amounts = []
        for elem in elements:
            # Highlight during execution
            self.driver.execute_script("arguments[0].setAttribute('style', 'border: 2px solid green;');", elem)
            text = elem.text.strip()
            if text:
                amounts.append(text)

        return amounts