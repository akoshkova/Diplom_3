from base_page import BasePage
from allure import step
from pages.order_details_modal import OrderDetailsModal


class OrderFeedPage(BasePage):
    ORDER_CARD = ('css', 'div.OrderHistory_orderItem__2xQbr')
    ORDER_STATUS = ('css', 'p.OrderHistory_orderStatus__3FmlJ')

    @step("Открыть детали заказа")
    def open_order_details(self, order_index=0):
        orders = self.find_elements(self.ORDER_CARD)
        orders[order_index].click()
        return OrderDetailsModal(self.driver)

    @step("Проверить статус заказа")
    def check_order_status(self, order_index, expected_status):
        status_element = self.find_elements(self.ORDER_STATUS)[order_index]
        assert status_element.text == expected_status
