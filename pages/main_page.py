from base_page import BasePage
from allure import step
from selenium.webdriver.common.by import By


def _format_locator(locator, **kwargs):
    return locator[0], locator[1].format(**kwargs)


class MainPage(BasePage):
    # Локаторы
    CONSTRUCTOR_BUTTON = (By.XPATH, '//a[contains(text(),"Конструктор")]')
    ORDER_FEED_BUTTON = (By.XPATH, '//a[contains(text(),"Лента заказов")]')
    INGREDIENT_ITEM = (By.XPATH, f'//ul[contains(@class, "BurgerIngredients_ingredients__list")]//li//p[text()="{{name}}"]/ancestor::li')
    MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, 'div.Modal_modal__close__2F_7J')
    INGREDIENT_COUNTER = (By.XPATH, f'//p[text()="{{name}}"]/following-sibling::div[contains(@class, "counter_counter__")]')
    CONSTRUCTOR_AREA = (By.CSS_SELECTOR, 'div.BurgerConstructor_basket__list__3LywD')
    RESET_BUTTON = (By.XPATH, '//button[contains(text(), "Сбросить")]')
    CONSTRUCTOR_ITEMS = (By.CSS_SELECTOR, 'div.BurgerConstructor_basket__list__3LywD > div')
    MODAL_CONTENT = (By.CSS_SELECTOR, 'div.Modal_modal__content__1Gtlm')
    CONSTRUCTOR_SECTION = (By.CSS_SELECTOR, 'section.BurgerIngredients_ingredients__1SoVX')
    ORDER_FEED_SECTION = (By.CSS_SELECTOR, 'section.OrderFeed_feed__3Nw20')
    ORDER_BUTTON = (By.XPATH, '//buttoncontains(text(), "Оформить заказ")')
    ORDER_MODAL = (By.CSS_SELECTOR, 'div.OrderModal_modal__content__2MpkD')
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    SUBMIT_LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ORDER_NUMBER = (By.CSS_SELECTOR, "div.OrderModal_number__text")
    ORDER_STATUS = (By.XPATH, "//p[contains(text(), 'Ваш заказ начали готовить')]")

    def __init__(self, driver):
        super().__init__(driver)

    @step("Перейти в конструктор")
    def go_to_constructor(self):
        self.safe_click(self.CONSTRUCTOR_BUTTON)
        self.wait_for_page_loaded()

    @step("Открыть ленту заказов")
    def open_order_feed(self):
        self.safe_click(self.ORDER_FEED_BUTTON)
        self.url_contains('/feed')

    @step("Выбрать ингредиент '{name}'")
    def select_ingredient(self, name):
        locator = _format_locator(self.INGREDIENT_ITEM, name=name)
        self.scroll_to_element(locator)
        self.safe_click(locator)

    @step("Добавить ингредиент '{name}'")
    def add_ingredient(self, name):
        initial_count = self.get_ingredient_count(name)
        self.select_ingredient(name)
        self.wait_for_counter_update(name, initial_count + 1)

    @step("Получить количество ингредиента '{name}'")
    def get_ingredient_count(self, name):
        counter = _format_locator(self.INGREDIENT_COUNTER, name=name)
        if self.is_visible(counter):
            return int(self.find_element(counter).text)
        return 0

    @step("Сбросить конструктор")
    def reset_constructor(self):
        self.safe_click(self.RESET_BUTTON)
        self.wait_disappear(self.RESET_BUTTON)
        self.wait.until(lambda d: self.get_total_ingredients() == 0)

    @step("Получить общее количество ингредиентов")
    def get_total_ingredients(self):
        return len(self.find_elements(self.CONSTRUCTOR_ITEMS))

    @step("Дождаться обновления счетчика для '{name}' до {expected_count}")
    def wait_for_counter_update(self, name, expected_count):
        def _check_counter():
            return self.get_ingredient_count(name) == expected_count
        self.wait.until(_check_counter, f"Счетчик для {name} не обновился до {expected_count}")

    @step("Проверить открытие конструктора")
    def verify_constructor_opened(self):
        self.assert_element_visible(self.CONSTRUCTOR_SECTION, "Раздел конструктора не открылся")

    @step("Открыть детали ингредиента")
    def open_ingredient_details(self, name):
        self.select_ingredient(name)
        self.wait_for_element_visible(self.MODAL_CONTENT)

    @step("Закрыть модальное окно ингредиента")
    def close_ingredient_modal(self):
        self.safe_click(self.MODAL_CLOSE_BUTTON)
        self.wait_for_element_hidden(self.MODAL_CONTENT)

    @step("Проверить открытие ленты заказов")
    def verify_order_feed_opened(self):
        self.assert_element_visible(
            self.ORDER_FEED_SECTION,
            "Раздел ленты заказов не открылся"
        )

    @step("Проверить видимость модального окна")
    def verify_modal_visible(self):
        self.assert_element_visible(
            self.MODAL_CONTENT,
            "Модальное окно не отображается"
        )

    @step("Проверить закрытие модального окна")
    def verify_modal_closed(self):
        self.assert_element_hidden(
            self.MODAL_CONTENT,
            "Модальное окно не закрылось"
        )

    @step("Открыть конструктор")
    def open_constructor(self):
        self.safe_click(self.CONSTRUCTOR_BUTTON)
        self.wait_for_page_loaded()

    @step("Выполнить вход")
    def perform_login(self, email, password):
        self._open_auth_modal()
        self._fill_credentials(email, password)
        self._submit_login()

    @step("Разместить заказ")
    def submit_order(self):
        self.safe_click(self.ORDER_BUTTON)
        self.wait_for_element_visible(self.ORDER_MODAL)
        return {
        'number': self.find_element(self.ORDER_NUMBER).text,
        'status': self.find_element(self.ORDER_STATUS).text
        }

    @step("Открыть модальное окно авторизации")
    def _open_auth_modal(self):
        self.safe_click(self.LOGIN_BUTTON)
        self.wait_for_element_visible(self.EMAIL_INPUT)
        return self

    @step("Заполнить учетные данные: {email}/{password}")
    def _fill_credentials(self, email, password):
        self.find_element(self.EMAIL_INPUT).send_keys(email)
        self.find_element(self.PASSWORD_INPUT).send_keys(password)
        return self

    @step("Подтвердить авторизацию")
    def _submit_login(self):
        self.safe_click(self.SUBMIT_LOGIN_BUTTON)
        self.wait_for_element_hidden(self.SUBMIT_LOGIN_BUTTON)
        return self

    @step("Выполнить вход")
    def perform_login(self, email, password):
        (self._open_auth_modal()
         ._fill_credentials(email, password)
         ._submit_login())
        return self

    @step("Разместить заказ")
    def submit_order(self):
        self.safe_click(self.ORDER_BUTTON)
        self.wait_for_element_visible(self.ORDER_MODAL)
        return {
            'number': self.find_element(self.ORDER_NUMBER).text,
            'status': self.find_element(self.ORDER_STATUS).text
        }