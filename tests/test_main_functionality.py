import pytest
from pages.main_page import MainPage
from data.test_data import TestData
from allure import title


@title("Тесты основной функциональности")
class TestMainFunctionality:
    @title("Проверка перехода в конструктор")
    def test_constructor_navigation(self, driver):
        page = MainPage(driver)
        page.open()
        page.go_to_constructor()
        assert "constructor" in driver.current_url

    @title("Проверка открытия модального окна ингредиента")
    def test_ingredient_modal(self, driver):
        page = MainPage(driver)
        page.open()
        page.select_ingredient()
        assert page.is_modal_displayed()
        page.close_modal()
        assert not page.is_modal_displayed()
