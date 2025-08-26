from pages.main_page import MainPage
from pages.profile_page import ProfilePage
from allure import title


@title("Тесты пользовательских сценариев")
class TestUserFlow:
    @title("Полный цикл заказа")
    def test_complete_order_flow(self, driver, test_user):
        main_page = MainPage(driver)

    main_page.open()
    main_page.login(test_user['data']['email'], test_user['data']['password'])
    main_page.add_ingredient('Булка')
    main_page.add_ingredient('Соус')
    order_modal = main_page.place_order()
    order_number = order_modal.get_order_number()

    profile_page = ProfilePage(driver)
    profile_page.open_order_history()
    assert profile_page.is_order_in_history(order_number)
