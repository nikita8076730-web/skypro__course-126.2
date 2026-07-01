# pages/checkout_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


class CheckoutPage:
    """Page Object для страницы оформления заказа"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        self.first_name_input = (By.ID, "first-name")
        self.last_name_input = (By.ID, "last-name")
        self.postal_code_input = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.total_label = (
            By.CLASS_NAME,
            "summary_total_label"
        )

    def fill_checkout_info(self, first_name, last_name, postal_code):
        """Заполнить форму данными"""
        self.driver.find_element(*self.first_name_input).send_keys(first_name)
        self.driver.find_element(*self.last_name_input).send_keys(last_name)
        # ИСПРАВЛЕНО: строка разбита на две
        element = self.driver.find_element(*self.postal_code_input)
        element.send_keys(postal_code)
        return self

    def click_continue(self):
        """Нажать кнопку Continue"""
        self.driver.find_element(*self.continue_button).click()
        return self

    def get_total(self):
        """Получить итоговую стоимость"""
        total_element = self.wait.until(
            EC.presence_of_element_located(self.total_label)
        )
        total_text = total_element.text

        numbers = re.findall(r'\d+\.\d+', total_text)
        if numbers:
            return numbers[0]
        return total_text.strip()
