from base_page import BasePage
from allure import step
from selenium.webdriver.common.by import By


def _format_locator(locator, **kwargs):
    return locator[0], locator[1].format(**kwargs)


class ProfilePage(BasePage):
    # Локаторы
    ORDER_HISTORY_LINK = (By.XPATH, '//a[contains(text(), "История заказов")]')
    ORDER_HISTORY_SECTION = (By.CSS_SELECTOR, 'section.Profile_orderHistory__3qD2T')
    ORDER_ITEM = (By.XPATH, '//p[contains(@class, "OrderHistory_number__") and text()="#{order_number}"]/ancestor::li')
    RESET_BUTTON = (By.XPATH, '//button[contains(text(), "Сбросить историю")]')
    USER_AVATAR = (By.CSS_SELECTOR, 'div.Profile_avatar__3Bhqs')

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://example.com/profile"  # Заменить на актуальный URL

    @step("Открыть страницу профиля")
    def open(self):
        self.driver.get(self.url)
        self.wait_for_page_loaded()
        return self

    @step("Перейти в раздел истории заказов")
    def navigate_to_order_history(self):
        self.safe_click(self.ORDER_HISTORY_LINK)
        self.wait_for_element_visible(self.ORDER_HISTORY_SECTION)
        return self

    @step("Проверить наличие заказа №{order_number}")
    def verify_order_presence(self, order_number):
        locator = _format_locator(self.ORDER_ITEM, order_number=order_number)
        self.assert_element_visible(
            locator,
            f"Заказ {order_number} не найден в истории"
        )
        return self

    @step("Сбросить историю заказов")
    def reset_order_history(self):
        self.safe_click(self.RESET_BUTTON)
        self.wait_for_element_hidden(self.RESET_BUTTON)
        return self

    @step("Проверить обновление аватара")
    def verify_avatar_updated(self, initial_avatar):
        self.wait.until(
            lambda d: self.get_element_attribute(self.USER_AVATAR, "src") != initial_avatar,
            "Аватар не был обновлен"
        )
        return self

    @step("Получить номер последнего заказа")
    def get_last_order_number(self):
        return self.find_element(self.ORDER_ITEM).text.strip().replace("#", "")

