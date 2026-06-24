from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


URL = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"


class TestCalculator:
    def setup_method(self):
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
        self.wait = WebDriverWait(self.driver, 50)

    def teardown_method(self):
        if self.driver:
            self.driver.quit()

    def test_calculator_with_delay(self):
        self.driver.get(URL)

        delay_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "delay"))
        )
        delay_input.clear()
        delay_input.send_keys("45")

        buttons = ["7", "+", "8", "="]
        for btn_text in buttons:
            button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//span[text()='{btn_text}']")
                )
            )
            button.click()

        screen_locator = (By.CSS_SELECTOR, ".screen")
        self.wait.until(
            EC.text_to_be_present_in_element(screen_locator, "15")
        )

        result = self.driver.find_element(*screen_locator).text
        assert result == "15"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
