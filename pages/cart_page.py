from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class CartPage:
    """Page Object для страницы корзины"""
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "#checkout")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "#continue-shopping")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, ".cart_button")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click_checkout(self):
        """Нажать кнопку Checkout"""
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()
        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)

    def get_cart_items_count(self):
        """Получить количество товаров в корзине"""
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def get_item_names(self):
        """Получить названия всех товаров в корзине"""
        items = self.driver.find_elements(*self.ITEM_NAMES)
        return [item.text for item in items]

    def is_item_in_cart(self, item_name):
        """Проверить, есть ли товар в корзине"""
        names = self.get_item_names()
        return item_name in names
