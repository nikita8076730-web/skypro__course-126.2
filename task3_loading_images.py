from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# Подключаем ChromeDriver
try:
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
except ImportError:
    driver = webdriver.Chrome()

try:
    driver.get(
        "https://bonigarcia.dev/selenium-webdriver-java/loading-images.html"
    )
    print("Страница загружена")

    wait = WebDriverWait(driver, 30)
    wait.until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "p"), "Done!")
    )
    print("Все изображения загружены (появился текст 'Done!')")

    images = driver.find_elements(By.TAG_NAME, "img")
    print(f"Всего загружено изображений: {len(images)}")

    third_image = images[2]

    src_value = third_image.get_attribute("src")

    print(f"Значение атрибута src у 3-й картинки: {src_value}")

except Exception as e:
    print(f"❌ Ошибка: {e}")

finally:
    driver.quit()
    print("Браузер закрыт")
