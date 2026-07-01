from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    """Page Object для калькулятора"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

        self.delay_input = (By.ID, "delay")
        self.result_output = (By.CLASS_NAME, "screen")
        self.button_7 = (By.XPATH, "//span[text()='7']")
        self.button_8 = (By.XPATH, "//span[text()='8']")
        self.button_plus = (By.XPATH, "//span[text()='+']")
        self.button_equals = (By.XPATH, "//span[text()='=']")

    def open(self):
        """Открыть страницу калькулятора"""
        url = (
            "https://bonigarcia.dev/"
            "selenium-webdriver-java/"
            "slow-calculator.html"
        )
        self.driver.get(url)
        return self

    def set_delay(self, seconds):
        """Установить задержку"""
        delay_element = self.driver.find_element(*self.delay_input)
        delay_element.clear()
        delay_element.send_keys(str(seconds))
        return self

    def click_7(self):
        """Нажать кнопку 7"""
        self.driver.find_element(*self.button_7).click()
        return self

    def click_8(self):
        """Нажать кнопку 8"""
        self.driver.find_element(*self.button_8).click()
        return self

    def click_plus(self):
        """Нажать кнопку +"""
        self.driver.find_element(*self.button_plus).click()
        return self

    def click_equals(self):
        """Нажать кнопку ="""
        self.driver.find_element(*self.button_equals).click()
        return self

    def get_result(self):
        """Получить результат"""
        result_element = self.wait.until(
            EC.presence_of_element_located(self.result_output)
        )
        return result_element.text

    def wait_for_result(self, expected_value):
        """Ожидать появления результата"""
        self.wait.until(
            lambda driver: driver.find_element(
                *self.result_output
            ).text == expected_value
        )
        return self
