from base_page import BasePage
from allure import step
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    REGISTER_LINK = ('css', 'a[href="/register"]')
    FORGOT_PASSWORD_LINK = ('css', 'a[href="/forgot-password"]')
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[name="email"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[name="password"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')

    @step("Заполнить email: {email}")
    def enter_email(self, email):
        self.find_element(self.EMAIL_INPUT).send_keys(email)

    @step("Заполнить пароль: {password}")
    def enter_password(self, password):
        self.find_element(self.PASSWORD_INPUT).send_keys(password)

    @step("Отправить форму авторизации")
    def submit_login(self):
        self.safe_click(self.LOGIN_BUTTON)
        self.wait_for_element_hidden(self.LOGIN_BUTTON)
        return self

    @step("Полная процедура авторизации")
    def full_login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.submit_login()
