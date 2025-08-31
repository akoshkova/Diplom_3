from base_page import BasePage
from allure import step


class OrderDetailsModal(BasePage):
    MODAL_TITLE = ('css', 'div.OrderModal_title__2Fc7s')
    INGREDIENTS_LIST = ('css', 'ul.OrderModal_ingredientsList__3XlUY')

@step("Получить состав заказа")
def get_ingredients_list(self):
    return [ingredient.text for ingredient in self.find_elements(self.INGREDIENTS_LIST)]

@step("Проверить наличие ингредиента {ingredient_name}")
def check_ingredient_present(self, ingredient_name):
    ingredients = self.get_ingredients_list()
    assert any(ingredient_name in item for item in ingredients)
