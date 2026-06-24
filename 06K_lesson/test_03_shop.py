from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager


class TestShop:
    def setup_method(self):
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--start-maximized")
        service = FirefoxService(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(
            service=service,
            options=firefox_options
        )
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self):
        if self.driver:
            self.driver.quit()

    def test_shop_purchase(self):
        self.driver.get("https://www.saucedemo.com/")

        username = self.wait.until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        username.send_keys("standard_user")

        password = self.driver.find_element(By.ID, "password")
        password.send_keys("secret_sauce")

        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()

        products = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]

        for product in products:
            xpath = (
                f"//div[text()='{product}']"
                "/ancestor::div[@class='inventory_item']//button"
            )
            add_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            add_button.click()

        cart_icon = self.driver.find_element(
            By.CLASS_NAME, "shopping_cart_link"
        )
        cart_icon.click()

        checkout_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout_button.click()

        first_name = self.wait.until(
            EC.presence_of_element_located((By.ID, "first-name"))
        )
        first_name.send_keys("Иван")

        last_name = self.driver.find_element(By.ID, "last-name")
        last_name.send_keys("Петров")

        postal_code = self.driver.find_element(By.ID, "postal-code")
        postal_code.send_keys("123456")

        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()

        total_element = self.wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "summary_total_label")
            )
        )
        total_value = total_element.text.replace("Total: ", "").strip()

        assert total_value == "$58.29"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
