from .base_page import BasePage
from allure import step


class LoginPage(BasePage):
    REGISTER_LINK = ('css', 'a[href="/register"]')
    FORGOT_PASSWORD_LINK = ('css', 'a[href="/forgot-password"]')

@step("Заполнить email: {email}")
def enter_email(self, email):
    self.find_element(self.EMAIL_INPUT).send_keys(email)

@step("Заполнить пароль: {password}")
def enter_password(self, password):
    self.find_element(self.PASSWORD_INPUT).send_keys(password)

@step("Полная процедура авторизации")
def full_login(self, email, password):
    self.enter_email(email)
    self.enter_password(password)
    self.submit_login()
