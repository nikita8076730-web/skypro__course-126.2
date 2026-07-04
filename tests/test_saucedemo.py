from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestSauceDemo:
    """Тесты для интернет-магазина"""

    def test_saucedemo_purchase(self, firefox_driver):
        """Тест покупки в интернет-магазине"""
        login_page = LoginPage(firefox_driver)
        inventory_page = InventoryPage(firefox_driver)
        cart_page = CartPage(firefox_driver)
        checkout_page = CheckoutPage(firefox_driver)

        login_page.open()
        login_page.enter_username("standard_user")
        login_page.enter_password("secret_sauce")
        login_page.click_login()

        inventory_page.add_backpack_to_cart()
        inventory_page.add_bolt_t_shirt_to_cart()
        inventory_page.add_onesie_to_cart()

        cart_count = inventory_page.get_cart_count()
        assert cart_count == 3, (
            f"В корзине должно быть 3 товара, а не {cart_count}"
        )

        inventory_page.go_to_cart()

        cart_page.click_checkout()

        checkout_page.fill_checkout_info("John", "Doe", "12345")
        checkout_page.click_continue()

        total = checkout_page.get_total()
        print(f"Итоговая стоимость: {total}")

        expected_total = "58.29"
        assert total == expected_total, (
            f"Ожидалась сумма {expected_total}, получена {total}"
        )

        print("Тест успешно пройден!")
