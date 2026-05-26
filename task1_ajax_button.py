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
    driver.get("http://uitestingplayground.com/ajax")
    print("Страница загружена")

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#ajaxButton"))
    )
    button.click()
    print("Кнопка нажата")

    css_selector = ".bg-success"
    success_label = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
    )

    text = success_label.text
    print(f"Текст из зеленой плашки: {text}")

    expected_text = "Data loaded with AJAX get request."
    assert text == expected_text, (
        f"Текст не совпадает. Ожидалось: '{expected_text}', "
        f"Получено: '{text}'"
    )
    print("✅ Текст совпадает с ожидаемым")

except Exception as e:
    print(f"❌ Ошибка: {e}")

finally:
    driver.quit()
    print("Браузер закрыт")
