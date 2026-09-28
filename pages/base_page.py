import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def highlight_element(self, element: WebElement, duration: float = 0.3):
        """Highlights the targeted element with a red border before execution."""
        original_style = element.get_attribute('style')
        self.driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            "border: 2px solid red; background-color: yellow;"
        )
        time.sleep(duration)
        self.driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            original_style
        )

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.highlight_element(element)
        element.click()

    def send_keys(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self.highlight_element(element)
        element.clear()
        element.send_keys(text)

    def get_current_url(self) -> str:
        return self.driver.current_url