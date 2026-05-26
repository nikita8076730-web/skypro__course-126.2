from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

try:
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
except ImportError:
    driver = webdriver.Chrome()

try:
    driver.get("http://uitestingplayground.com/textinput")
    print("Страница загружена")

    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#newButtonName"))
    )
    input_field.send_keys("SkyPro")
    print("В поле ввода введен текст: SkyPro")

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#updatingButton"))
    )
    button.click()
    print("Кнопка нажата")

    expected_text = "SkyPro"
    button_selector = "#updatingButton"
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, button_selector), expected_text
        )
    )

    new_button_text = button.text
    print(f"Текст кнопки после нажатия: {new_button_text}")

    assert new_button_text == expected_text, (
        f"Текст не совпадает. Ожидалось: '{expected_text}', "
        f"Получено: '{new_button_text}'"
    )
    print("✅ Текст кнопки успешно изменен на 'SkyPro'")

except Exception as e:
    print(f"❌ Ошибка: {e}")

finally:
    driver.quit()
    print("Браузер закрыт")
