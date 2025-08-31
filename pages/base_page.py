from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from allure import step
import logging
import allure

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://stellarburgers.nomoreparties.site/"
        self.logger = logging.getLogger('tests')
        self.wait = WebDriverWait(self.driver, 15, poll_frequency=0.5, 
                                ignored_exceptions=[StaleElementReferenceException])

    @step("Открыть страницу '{path}'")
    def open(self, path=''):
        full_url = f"{self.base_url}{path}"
        self.logger.info(f"Opening URL: {full_url}")
        self.driver.get(full_url)
        self.wait_for_page_loaded()

    @step("Найти элемент {locator}")
    def find_element(self, locator, timeout=15):
        return self._wait_for(EC.presence_of_element_located(locator), timeout)

    @step("Найти кликабельный элемент {locator}")
    def find_clickable(self, locator, timeout=15):
        return self._wait_for(EC.element_to_be_clickable(locator), timeout)

    @step("Найти все элементы {locator}")
    def find_elements(self, locator, timeout=10):
        return self._wait_for(EC.presence_of_all_elements_located(locator), timeout)

    @step("Дождаться исчезновения элемента {locator}")
    def wait_disappear(self, locator, timeout=10):
        self._wait_for(EC.invisibility_of_element_located(locator), timeout)

    @step("Обновить страницу")
    def refresh(self):
        self.driver.refresh()
        self.wait_for_page_loaded()

    @step("Проверить видимость элемента {locator}")
    def is_visible(self, locator, timeout=5):
        try:
            return self._wait_for(EC.visibility_of_element_located(locator), timeout) is not None
        except TimeoutException:
            return False

    @step("Проверить текст элемента {locator} содержит '{text}'")
    def text_contains(self, locator, text, timeout=10):
        element = self.find_element(locator, timeout)
        self._wait_for(lambda d: text.lower() in element.text.strip().lower(), timeout)

    @step("Проверить URL содержит '{text}'")
    def url_contains(self, text, timeout=10):
        self._wait_for(lambda d: text.lower() in d.current_url.lower(), timeout)

    def _wait_for(self, condition, timeout):
        return WebDriverWait(self.driver, timeout, 0.5, [StaleElementReferenceException]).until(condition)

    @step("Дождаться загрузки страницы")
    def wait_for_page_loaded(self, timeout=30):
        try:
            self._wait_for(lambda d: d.execute_script('return document.readyState') == 'complete', timeout)
            self._wait_for(lambda d: d.execute_script(
                'return window.performance.timing.loadEventEnd') > 0, timeout)
            self.logger.info("Page loaded successfully")
        except TimeoutException:
            self.logger.error("Page load timeout")
            self.take_screenshot('page_load_timeout')
            raise

    @step("Сделать скриншот '{name}'")
    def take_screenshot(self, name=None, datetime=None):
        name = name or f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        path = f"./screenshots/{name}.png"
        self.driver.save_screenshot(path)
        allure.attach.file(path, name=name, attachment_type=allure.attachment_type.PNG)

    @step("Выполнить JS: {script}")
    def js_execute(self, script, *args):
        return self.driver.execute_script(script, *args)

    @step("Скролл к элементу {locator}")
    def scroll_to_element(self, locator):
        element = self.find_element(locator)
        self.js_execute("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    @step("Клик по элементу {locator}")
    def safe_click(self, locator, timeout=15):
        element = self.find_clickable(locator, timeout)
        element.click()

    @step("Ввод текста '{text}' в элемент {locator}")
    def safe_send_keys(self, locator, text, timeout=15):
        element = self.find_clickable(locator, timeout)
        element.clear()
        element.send_keys(text)

    @step("Проверить видимость элемента {locator}")
    def assert_element_visible(self, locator, message=None):
        message = message or f"Элемент {locator} не отображается"
        assert self.is_visible(locator), message

    @step("Проверить скрытие элемента {locator}")
    def assert_element_hidden(self, locator, message=None):
        message = message or f"Элемент {locator} не скрыт"
        assert not self.is_visible(locator), message

    @step("Дождаться отображения элемента {locator}")
    def wait_for_element_visible(self, locator, timeout=15):
        self.wait.until(
            EC.visibility_of_element_located(locator),
        f"Элемент {locator} не появился за {timeout} сек"
        )

    @step("Дождаться скрытия элемента {locator}")
    def wait_for_element_hidden(self, locator, timeout=15):
        self.wait.until(
            EC.invisibility_of_element_located(locator),
        f"Элемент {locator} не скрылся за {timeout} сек"
        )

    @step("Ожидание загрузки страницы")
    def wait_for_page_loaded(self):
        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    @step("Проверка видимости элемента {locator}")
    def assert_element_visible(self, locator, message=None):
        if not self.is_visible(locator):
            raise AssertionError(message or f"Элемент {locator} не отображается")

    @step("Получить атрибут '{attribute}' элемента {locator}")
    def get_element_attribute(self, locator, attribute):
        element = self.find_element(locator)
        return element.get_attribute(attribute)