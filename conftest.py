import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.profile_page import ProfilePage


@pytest.fixture(scope='function', params=['chrome', 'firefox'])
def driver(request):
    if request.param == 'chrome':
        options = Options()
        options.add_argument('--headless')
        webdriver.Chrome(options=options)
    elif request.param == 'firefox':
        options = FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        yield driver
        driver.quit()

@pytest.fixture(autouse=True)
def clear_order_history(request, driver):
    profile_page = ProfilePage(driver)

    def finalizer():
        try:
            profile_page.navigate_to_order_history()
            profile_page.reset_order_history()
            profile_page.verify_no_orders_in_history()
        except Exception as e:
            print(f"Ошибка при очистке истории заказов: {e}")

    request.addfinalizer(finalizer)

