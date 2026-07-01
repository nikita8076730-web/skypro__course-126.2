from selenium.webdriver.common.by import By


class LoginPage:
    """Page Object для страницы авторизации"""
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "user-name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")

    def open(self):
        """Открыть страницу авторизации"""
        self.driver.get("https://www.saucedemo.com/")
        return self

    def enter_username(self, username):
        """Ввести имя пользователя"""
        self.driver.find_element(*self.username_input).send_keys(username)
        return self

    def enter_password(self, password):
        """Ввести пароль"""
        self.driver.find_element(*self.password_input).send_keys(password)
        return self

    def click_login(self):
        """Нажать кнопку входа"""
        self.driver.find_element(*self.login_button).click()
        return self

    def login(self, username, password):
        """Выполнить авторизацию"""
        self.open()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self
