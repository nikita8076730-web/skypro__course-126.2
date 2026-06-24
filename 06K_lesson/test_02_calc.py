from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time

URL = "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"


class TestCalculator:
    def setup_method(self):
        """Настройка браузера перед каждым тестом"""
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")

        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
        self.wait = WebDriverWait(
            self.driver,
            50
        )

    def teardown_method(self):
        """Закрытие браузера после каждого теста"""
        if self.driver:
            self.driver.quit()

    def test_calculator_with_delay(self):
        """Тест калькулятора с задержкой 45 секунд"""
        print("\n" + "=" * 60)
        print("НАЧАЛО ТЕСТА КАЛЬКУЛЯТОРА")
        print("=" * 60)

        print("\n[1/6] Открываем страницу...")
        self.driver.get(URL)
        time.sleep(2)
        print("✓ Страница загружена")

        print("\n[2/6] Устанавливаем задержку...")
        delay_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "delay"))
        )
        delay_input.clear()
        time.sleep(1)
        delay_input.send_keys("45")
        print("✓ Задержка установлена: 45 секунд")
        time.sleep(1)

        print("\n[3/6] Нажимаем кнопку 7...")
        btn_7 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='7']"))
        )
        btn_7.click()
        print("✓ Нажата кнопка 7")
        time.sleep(1)

        print("\n[4/6] Нажимаем кнопку +...")
        btn_plus = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='+']"))
        )
        btn_plus.click()
        print("✓ Нажата кнопка +")
        time.sleep(1)

        print("\n[5/6] Нажимаем кнопку 8...")
        btn_8 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='8']"))
        )
        btn_8.click()
        print("✓ Нажата кнопка 8")
        time.sleep(1)

        print("\n[6/6] Нажимаем кнопку = и ждем результат...")
        btn_equals = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='=']"))
        )
        btn_equals.click()
        print("✓ Нажата кнопка =")
        print("\n⏳ Ожидание результата 45 секунд...")

        screen_locator = (By.CSS_SELECTOR, ".screen")
        self.wait.until(
            EC.text_to_be_present_in_element(screen_locator, "15")
        )

        result_element = self.driver.find_element(*screen_locator)
        result_text = result_element.text

        assert result_text == "15", (
            f"Ожидался результат 15, получен {result_text}"
        )

        print("\n" + "=" * 60)
        print("✅ ТЕСТ ПРОЙДЕН УСПЕШНО!")
        print(f"  Вычисление: 7 + 8 = {result_text}")
        print("=" * 60)


def test_calculator_slow():
    """Медленный тест калькулятора с подробным выводом"""
    print("\n" + "=" * 60)
    print("МЕДЛЕННЫЙ ТЕСТ КАЛЬКУЛЯТОРА")
    print("=" * 60)

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        print("\n[1/7] Открываем страницу калькулятора...")
        driver.get(URL)
        time.sleep(3)
        print("✓ Страница загружена")

        print("\n[2/7] Находим поле ввода задержки...")
        delay_input = driver.find_element(By.ID, "delay")
        time.sleep(1)
        print("✓ Поле найдено")

        print("  Очищаем поле...")
        delay_input.clear()
        time.sleep(1)

        print("  Вводим значение 45...")
        delay_input.send_keys("45")
        time.sleep(1)
        print("✓ Задержка установлена на 45 секунд")

        print("\n[3/7] Нажимаем кнопку 7...")
        btn_7 = driver.find_element(By.XPATH, "//span[text()='7']")
        time.sleep(0.5)
        btn_7.click()
        time.sleep(1)
        print("✓ Кнопка 7 нажата")

        screen = driver.find_element(By.CSS_SELECTOR, ".screen")
        print(f"  На дисплее: '{screen.text}'")

        print("\n[4/7] Нажимаем кнопку +...")
        btn_plus = driver.find_element(By.XPATH, "//span[text()='+']")
        time.sleep(0.5)
        btn_plus.click()
        time.sleep(1)
        print("✓ Кнопка + нажата")
        print(f"  На дисплее: '{screen.text}'")

        print("\n[5/7] Нажимаем кнопку 8...")
        btn_8 = driver.find_element(By.XPATH, "//span[text()='8']")
        time.sleep(0.5)
        btn_8.click()
        time.sleep(1)
        print("✓ Кнопка 8 нажата")
        print(f"  На дисплее: '{screen.text}'")

        print("\n[6/7] Нажимаем кнопку = и ждем результат...")
        btn_equals = driver.find_element(By.XPATH, "//span[text()='=']")
        time.sleep(0.5)
        btn_equals.click()
        time.sleep(1)
        print("✓ Кнопка = нажата")
        print(f"  На дисплее: '{screen.text}'")

        print("\n[7/7] Проверяем результат...")
        print("⏳ Ожидание вычисления (45 секунд)...")

        wait = WebDriverWait(driver, 50)
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, ".screen"),
                "15"
            )
        )

        result = driver.find_element(By.CSS_SELECTOR, ".screen").text
        assert result == "15", f"Ожидалось 15, получено {result}"

        print("\n" + "=" * 60)
        print("✅ ТЕСТ УСПЕШНО ЗАВЕРШЕН!")
        print(f"  Выражение: 7 + 8 = {result}")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        driver.save_screenshot("error_screenshot.png")
        print("  Скриншот сохранен как error_screenshot.png")
        raise
    finally:
        print("\nЗакрываем браузер...")
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    test_calculator_slow()
