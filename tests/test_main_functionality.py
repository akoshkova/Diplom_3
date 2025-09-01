from pages.main_page import MainPage
from allure import title


@title("Тесты основной функциональности")
class TestMainFunctionality:
    @title("Проверка навигации по разделам")
    def test_section_navigation(self, driver):
        main_page = MainPage(driver)

        # Тест конструктора
        main_page.go_to_constructor()
        main_page.verify_constructor_opened()

        # Тест ленты заказов
        main_page.open_order_feed()
        main_page.verify_order_feed_opened()

    @title("Проверка работы с модальными окнами")
    def test_ingredient_modal_interaction(self, driver):
        main_page = MainPage(driver)
        main_page.open()

        # Тест открытия/закрытия модального окна
        ingredient_name = "Булка"
        main_page.open_ingredient_details(ingredient_name)
        main_page.verify_modal_visible()

        main_page.close_ingredient_modal()
        main_page.verify_modal_closed()
