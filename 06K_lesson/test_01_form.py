from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options


class TestForm:
    def setup_method(self):
        edge_options = Options()
        edge_options.add_argument("--start-maximized")
        service = Service(EdgeChromiumDriverManager().install())
        self.driver = webdriver.Edge(service=service, options=edge_options)
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self):
        if self.driver:
            self.driver.quit()

    def test_form_submission(self):
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
            var zipInput = document.querySelector('input[name="zip-code"]');
            zipInput.setAttribute('required', true);
            var inputs = document.querySelectorAll('input');
            inputs.forEach(function(input) {
                if (input.checkValidity()) {
                    input.classList.add('is-valid');
                } else {
                    input.classList.add('is-invalid');
                }
            });
        """)

        zip_field = self.driver.find_element(By.NAME, "zip-code")
        zip_class = zip_field.get_attribute("class")
        assert "is-invalid" in zip_class, (
            "Zip code должен быть подсвечен красным"
        )

        green_fields = [
            "first-name", "last-name", "address", "e-mail",
            "phone", "city", "country", "job-position", "company"
        ]

        for field_name in green_fields:
            field = self.driver.find_element(By.NAME, field_name)
            field_class = field.get_attribute("class")
            assert "is-valid" in field_class, (
                f"Поле {field_name} должно быть подсвечено зеленым"
            )


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
