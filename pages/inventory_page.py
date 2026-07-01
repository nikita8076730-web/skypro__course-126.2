from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class InventoryPage:
    """Page Object для главной страницы магазина"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        self.backpack_add = (By.ID, "add-to-cart-sauce-labs-backpack")
        self.bolt_tshirt_add = (
            By.ID,
            "add-to-cart-sauce-labs-bolt-t-shirt"
        )
        self.onesie_add = (By.ID, "add-to-cart-sauce-labs-onesie")
        self.cart_icon = (By.CLASS_NAME, "shopping_cart_link")

    def add_backpack_to_cart(self):
        """Добавить рюкзак в корзину"""
        self.driver.find_element(*self.backpack_add).click()
        return self

    def add_bolt_t_shirt_to_cart(self):
        """Добавить футболку в корзину"""
        self.driver.find_element(*self.bolt_tshirt_add).click()
        return self

    def add_onesie_to_cart(self):
        """Добавить комбинезон в корзину"""
        self.driver.find_element(*self.onesie_add).click()
        return self

    def go_to_cart(self):
        """Перейти в корзину"""
        self.driver.find_element(*self.cart_icon).click()
        return self

    def get_cart_count(self):
        """Получить количество товаров в корзине"""
        try:
            badge = self.driver.find_element(
                By.CLASS_NAME,
                "shopping_cart_badge"
            )
            return int(badge.text)
        except Exception:
            return 0
