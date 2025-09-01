from pages.main_page import MainPage
from pages.profile_page import ProfilePage
from allure import title

@title("Тесты пользовательских сценариев")
class TestUserFlow:
    @title("Полный цикл заказа")
    def test_complete_order_flow(self, driver, test_user):
        main_page = MainPage(driver)
        profile_page = ProfilePage(driver)

        main_page.open()
        main_page.perform_login(test_user['email'], test_user['password'])
        main_page.add_ingredient('Булка')
        main_page.add_ingredient('Соус')
        order_data = main_page.submit_order()

        profile_page.navigate_to_order_history()
        profile_page.verify_order_presence(order_data['number'])


