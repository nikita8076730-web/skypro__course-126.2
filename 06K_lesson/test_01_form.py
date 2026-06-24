from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options


class TestForm:
    def setup_method(self):
        """Настройка браузера перед каждым тестом"""
        edge_options = Options()
        edge_options.add_argument("--start-maximized")

        service = Service(EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(service=service, options=edge_options)
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self):
        """Закрытие браузера после каждого теста"""
        if self.driver:
            self.driver.quit()

    def test_form_submission(self):
        """Тест заполнения формы и проверки подсветки полей"""
        self.driver.get(
            "https://bonigarcia.dev/selenium-webdriver-java/data-types.html"
        )

        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))

        form_data = {
            "first-name": "Иван",
            "last-name": "Петров",
            "address": "Ленина, 55-3",
            "e-mail": "test@skypro.com",
            "phone": "+7985899998787",
            "zip-code": "",
            "city": "Москва",
            "country": "Россия",
            "job-position": "QA",
            "company": "SkyPro"
        }

        for field_name, value in form_data.items():
            field = self.wait.until(
                EC.presence_of_element_located((By.NAME, field_name))
            )
            field.clear()
            if value:
                field.send_keys(value)

        self.driver.execute_script("""
            var inputs = document.querySelectorAll('input');
            inputs.forEach(function(input) {
                input.setAttribute('required', true);
            });
            var zipInput = document.querySelector('input[name="zip-code"]');
            zipInput.value = '';
        """)

        self.driver.execute_script("""
            var form = document.querySelector('form');
            form.setAttribute('novalidate', true);
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                var inputs = form.querySelectorAll('input');
                inputs.forEach(function(input) {
                    if (input.checkValidity()) {
                        input.classList.add('is-valid');
                        input.classList.remove('is-invalid');
                    } else {
                        input.classList.add('is-invalid');
                        input.classList.remove('is-valid');
                    }
                });
                form.classList.add('was-validated');
            });
            form.querySelector('button[type="submit"]').click();
        """)

        import time
        time.sleep(1)

        zip_field = self.driver.find_element(By.NAME, "zip-code")
        zip_class = zip_field.get_attribute("class")
        assert "is-invalid" in zip_class, (
            f"Zip code должен быть красным. Класс: {zip_class}"
        )
        green_fields = [
            "first-name", "last-name", "address", "e-mail",
            "phone", "city", "country", "job-position", "company"
        ]

        for field_name in green_fields:
            field = self.driver.find_element(By.NAME, field_name)
            field_class = field.get_attribute("class")
            assert "is-valid" in field_class, (
                f"Поле {field_name} должно быть зеленым. Класс: {field_class}"
            )

        print("\n✅ Все проверки пройдены успешно!")


if __name__ == "__main__":
    test = TestForm()
    test.setup_method()
    try:
        test.test_form_submission()
    finally:
        test.teardown_method()
