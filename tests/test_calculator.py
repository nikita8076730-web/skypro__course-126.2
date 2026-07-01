from pages.calculator_page import CalculatorPage


class TestCalculator:

    def test_slow_calculator(self, chrome_driver):
        calculator_page = CalculatorPage(chrome_driver)

        calculator_page.open()
        calculator_page.set_delay(45)
        calculator_page.click_7()
        calculator_page.click_plus()
        calculator_page.click_8()
        calculator_page.click_equals()

        calculator_page.wait_for_result("15")
        result = calculator_page.get_result()

        assert result == "15", f"Ожидался результат '15', получен '{result}'"
        print(f"Тест успешно пройден! Результат: {result}")
