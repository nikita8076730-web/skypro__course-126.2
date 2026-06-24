from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
import time


class TestShop:
    def setup_method(self):
        """Настройка браузера перед каждым тестом"""
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--start-maximized")

        service = FirefoxService(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(
            service=service, options=firefox_options
        )
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self):
        """Закрытие браузера после каждого теста"""
        if self.driver:
            time.sleep(2)
            self.driver.quit()

    def test_shop_purchase(self):
        """Тест покупки товаров в магазине"""
        print("\n" + "=" * 70)
        print("  ТЕСТ ПОКУПКИ В ИНТЕРНЕТ-МАГАЗИНЕ")
        print("=" * 70)

        print("\n[1/10] Открываем сайт магазина...")
        self.driver.get("https://www.saucedemo.com/")
        time.sleep(3)
        print("  ✓ Сайт загружен")

        print("\n[2/10] Авторизация пользователя standard_user...")

        print("  Вводим логин...")
        username = self.wait.until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        username.send_keys("standard_user")
        time.sleep(1)
        print("  ✓ Логин введен")

        print("  Вводим пароль...")
        password = self.driver.find_element(By.ID, "password")
        password.send_keys("secret_sauce")
        time.sleep(1)
        print("  ✓ Пароль введен")

        print("  Нажимаем кнопку Login...")
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
        time.sleep(3)
        print("  ✓ Авторизация выполнена")

        print("\n[3/10] Добавляем товары в корзину...")

        print("  Добавляем Sauce Labs Backpack...")
        backpack_xpath = (
            "//div[text()='Sauce Labs Backpack']"
            "/ancestor::div[@class='inventory_item']//button"
        )
        backpack_add = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, backpack_xpath))
        )
        backpack_add.click()
        time.sleep(2)
        print("  ✓ Sauce Labs Backpack добавлен")

        print("  Добавляем Sauce Labs Bolt T-Shirt...")
        bolt_xpath = (
            "//div[text()='Sauce Labs Bolt T-Shirt']"
            "/ancestor::div[@class='inventory_item']//button"
        )
        bolt_add = self.driver.find_element(By.XPATH, bolt_xpath)
        bolt_add.click()
        time.sleep(2)
        print("  ✓ Sauce Labs Bolt T-Shirt добавлен")

        print("  Добавляем Sauce Labs Onesie...")
        onesie_xpath = (
            "//div[text()='Sauce Labs Onesie']"
            "/ancestor::div[@class='inventory_item']//button"
        )
        onesie_add = self.driver.find_element(By.XPATH, onesie_xpath)
        onesie_add.click()
        time.sleep(2)
        print("  ✓ Sauce Labs Onesie добавлен")

        cart_badge = self.driver.find_element(
            By.CLASS_NAME, "shopping_cart_badge"
        )
        cart_count = cart_badge.text
        print(f"  В корзине товаров: {cart_count}")
        assert cart_count == "3", (
            f"Ожидалось 3 товара, в корзине {cart_count}"
        )

        print("\n[4/10] Переходим в корзину...")
        cart_icon = self.driver.find_element(
            By.CLASS_NAME, "shopping_cart_link"
        )
        cart_icon.click()
        time.sleep(3)
        print("  ✓ Корзина открыта")

        print("\n[5/10] Нажимаем кнопку Checkout...")
        checkout_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout_button.click()
        time.sleep(3)
        print("  ✓ Переход к оформлению заказа")

        print("\n[6/10] Заполняем форму данными...")

        print("  Вводим имя: Иван")
        first_name = self.wait.until(
            EC.presence_of_element_located((By.ID, "first-name"))
        )
        first_name.send_keys("Иван")
        time.sleep(1)
        print("  ✓ Имя введено")

        print("  Вводим фамилию: Петров")
        last_name = self.driver.find_element(By.ID, "last-name")
        last_name.send_keys("Петров")
        time.sleep(1)
        print("  ✓ Фамилия введена")

        print("  Вводим почтовый индекс: 123456")
        postal_code = self.driver.find_element(By.ID, "postal-code")
        postal_code.send_keys("123456")
        time.sleep(1)
        print("  ✓ Почтовый индекс введен")

        print("\n[7/10] Нажимаем кнопку Continue...")
        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()
        time.sleep(3)
        print("  ✓ Переход к подтверждению заказа")

        print("\n[8/10] Читаем итоговую стоимость...")

        self.wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "summary_total_label")
            )
        )

        total_element = self.driver.find_element(
            By.CLASS_NAME, "summary_total_label"
        )
        total_text = total_element.text
        print(f"  Итоговая стоимость: {total_text}")

        total_value = total_text.replace("Total: ", "").strip()
        print(f"  Сумма: {total_value}")

        print("\n[9/10] Закрываем браузер...")
        print("  Браузер будет закрыт автоматически")

        print("\n[10/10] Проверяем итоговую сумму...")
        expected_total = "$58.29"
        print(f"  Ожидаемая сумма: {expected_total}")
        print(f"  Фактическая сумма: {total_value}")

        assert total_value == expected_total, (
            f"Итоговая сумма не совпадает. "
            f"Ожидалось {expected_total}, получено {total_value}"
        )

        print("  ✓ Сумма совпадает!")

        print("\n" + "=" * 70)
        print("  ✅ ТЕСТ ПРОЙДЕН УСПЕШНО!")
        print(f"    Итоговая сумма: {total_value}")
        print("    Добавлено 3 товара")
        print("=" * 70)


def test_shop_purchase_slow():
    """Очень медленный тест покупки"""
    print("\n" + "=" * 70)
    print("  ОЧЕНЬ МЕДЛЕННЫЙ ТЕСТ ПОКУПКИ")
    print("  (каждый шаг с паузой 2-4 секунды)")
    print("=" * 70)

    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--start-maximized")

    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(
        service=service, options=firefox_options
    )
    wait = WebDriverWait(driver, 10)

    try:
        print("\n[1/12] Открываем сайт магазина...")
        driver.get("https://www.saucedemo.com/")
        time.sleep(4)
        print("  ✓ Сайт загружен")

        print("\n[2/12] Вводим логин...")
        username = wait.until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        username.send_keys("standard_user")
        time.sleep(2)
        print("  ✓ Логин: standard_user")

        print("\n[3/12] Вводим пароль...")
        password = driver.find_element(By.ID, "password")
        password.send_keys("secret_sauce")
        time.sleep(2)
        print("  ✓ Пароль введен")

        print("\n[4/12] Нажимаем кнопку Login...")
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        time.sleep(4)
        print("  ✓ Авторизация выполнена")

        print("\n[5/12] Добавляем Sauce Labs Backpack...")
        backpack_xpath = (
            "//div[text()='Sauce Labs Backpack']"
            "/ancestor::div[@class='inventory_item']//button"
        )
        backpack = wait.until(
            EC.element_to_be_clickable((By.XPATH, backpack_xpath))
        )
        backpack.click()
        time.sleep(3)
        print("  ✓ Добавлен")

        print("\n[6/12] Добавляем Sauce Labs Bolt T-Shirt...")
        bolt_xpath = (
            "//div[text()='Sauce Labs Bolt T-Shirt']"
            "/ancestor::div[@class='inventory_item']//button"
        )
        bolt = driver.find_element(By.XPATH, bolt_xpath)
        bolt.click()
        time.sleep(3)
        print("  ✓ Добавлен")

        print("\n[7/12] Добавляем Sauce Labs Onesie...")
        onesie_xpath = (
            "//div[text()='Sauce Labs Onesie']"
            "/ancestor::div[@class='inventory_item']//button"
        )
        onesie = driver.find_element(By.XPATH, onesie_xpath)
        onesie.click()
        time.sleep(3)
        print("  ✓ Добавлен")

        print("\n[8/12] Переходим в корзину...")
        cart = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart.click()
        time.sleep(3)
        print("  ✓ Корзина открыта")

        print("\n[9/12] Нажимаем Checkout...")
        checkout = wait.until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )
        checkout.click()
        time.sleep(3)
        print("  ✓ Переход к оформлению")

        print("\n[10/12] Заполняем форму...")

        print("  Имя: Иван")
        driver.find_element(By.ID, "first-name").send_keys("Иван")
        time.sleep(2)

        print("  Фамилия: Петров")
        driver.find_element(By.ID, "last-name").send_keys("Петров")
        time.sleep(2)

        print("  Индекс: 123456")
        driver.find_element(By.ID, "postal-code").send_keys("123456")
        time.sleep(2)
        print("  ✓ Данные введены")

        print("\n[11/12] Нажимаем Continue...")
        driver.find_element(By.ID, "continue").click()
        time.sleep(4)
        print("  ✓ Переход к подтверждению")

        print("\n[12/12] Проверяем итоговую сумму...")
        wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "summary_total_label")
            )
        )

        total = driver.find_element(
            By.CLASS_NAME, "summary_total_label"
        ).text
        print(f"  Текст: {total}")

        total_value = total.replace("Total: ", "").strip()
        print(f"  Сумма: {total_value}")

        expected = "$58.29"
        assert total_value == expected, (
            f"Ожидалось {expected}, получено {total_value}"
        )

        print("\n" + "=" * 70)
        print("  🎉 ТЕСТ ПРОЙДЕН УСПЕШНО!")
        print(f"    Итоговая сумма: {total_value}")
        print("    Все товары добавлены и оплачены")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        driver.save_screenshot("error_shop.png")
        print("  Скриншот сохранен как error_shop.png")
        raise
    finally:
        time.sleep(3)
        driver.quit()
        print("\nБраузер закрыт.")


if __name__ == "__main__":
    test_shop_purchase_slow()
