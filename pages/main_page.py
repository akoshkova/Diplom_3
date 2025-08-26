from .base_page import BasePage
from allure import step


class MainPage(BasePage):
    # Локаторы
    CONSTRUCTOR_BUTTON = ('xpath', '//a[contains(text(),"Конструктор")]')
    ORDER_FEED_BUTTON = ('xpath', '//a[contains(text(),"Лента заказов")]')
    INGREDIENT_ITEM = ('css', 'ul.BurgerIngredients_ingredients__list__2A-mT li')
    MODAL_CLOSE_BUTTON = ('css', 'div.Modal_modal__close__2F_7J')

    @step("Перейти в конструктор")
    def go_to_constructor(self):
        self.find_element(self.CONSTRUCTOR_BUTTON).click()

    @step("Открыть ленту заказов")
    def open_order_feed(self):
        self.find_element(self.ORDER_FEED_BUTTON).click()

    @step("Выбрать ингредиент")
    def select_ingredient(self, index=0):
        ingredients = self.find_elements(self.INGREDIENT_ITEM)
        ingredients[index].click()

    @step("Закрыть модальное окно")
    def close_modal(self):
        self.find_element(self.MODAL_CLOSE_BUTTON).click()
