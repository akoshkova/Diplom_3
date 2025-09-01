from pages.main_page import MainPage
from allure import title


@title("Тесты конструктора бургеров")
class TestConstructor:
    @title("Проверка добавления ингредиента")
    def test_add_ingredient(self, driver):
        main_page = MainPage(driver)
        main_page.open()
        initial_count = main_page.get_ingredient_count('Булка')
        main_page.add_ingredient('Булка')
        assert main_page.get_ingredient_count('Булка') == initial_count + 1

    @title("Проверка сброса конструктора")
    def test_reset_constructor(self, driver):
        main_page = MainPage(driver)
        main_page.open()
        main_page.add_ingredient('Соус')
        main_page.reset_constructor()
        assert main_page.get_total_ingredients() == 0
