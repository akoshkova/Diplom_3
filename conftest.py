import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions


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

