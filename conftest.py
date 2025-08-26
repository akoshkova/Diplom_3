import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions


@pytest.fixture(scope='function', params=['chrome', 'firefox'])
def driver(request):
    if request.param == 'chrome':
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
    elif request.param == 'firefox':
        options = FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)

    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def user_credentials():
    return {
        'email': 'test_user@example.com',
        'password': 'P@ssw0rd123'
    }
