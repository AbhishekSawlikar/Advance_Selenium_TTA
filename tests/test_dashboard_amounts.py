import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.transaction_utils import TransactionUtils
from database.db_manager import DBManager

@allure.feature("Applitools Dashboard Validation")
@allure.story("Calculate and Verify Monthly Spent vs Database Audit")
class TestDashboardAmounts:

    @pytest.mark.regression
    def test_calculate_total_spent(self, driver, base_url):
        with allure.step("1. Navigate to Applitools Demo Login"):
            driver.get(base_url)

        with allure.step("2. Perform Login with Credentials"):
            login_page = LoginPage(driver)
            login_page.login("Admin", "Password@123")

        with allure.step("3. Verify Redirection to app.html"):
            # Explicitly wait until the browser reaches app.html
            WebDriverWait(driver, 10).until(EC.url_contains("app.html"))
            assert "app.html" in driver.current_url

        with allure.step("4. Fetch Transaction Amount Strings from Dashboard Table"):
            dashboard_page = DashboardPage(driver)
            raw_amounts = dashboard_page.get_all_amount_texts()
            allure.attach(str(raw_amounts), name="Raw Amounts Table Data", attachment_type=allure.attachment_type.TEXT)

        with allure.step("5. Parse and Categorize Spent vs Earned"):
            summary = TransactionUtils.categorize_transactions(raw_amounts)
            total_spent = summary["total_spent"]
            total_earned = summary["total_earned"]
            allure.attach(
                f"Total Spent: {total_spent} | Total Earned: {total_earned}",
                name="Parsed Transaction Summary",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("6. Fetch Expected Target from MySQL Database"):
            expected_spent_amount = DBManager.get_expected_spent_amount(month="current")

        with allure.step("7. Assert Total Spent matches 1996.22"):
            assert total_spent == 1996.22, f"Expected 1996.22, but calculated {total_spent}"
            assert total_spent == expected_spent_amount, \
                f"Calculated amount ({total_spent}) does not match DB audit value ({expected_spent_amount})"