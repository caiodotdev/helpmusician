# Generated by Selenium IDE
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from app.tests.base import BaseSeleniumTestCase
from app.tests.constants import USERNAME_USER_DEFAULT, PASSWORD_USER_DEFAULT, EMAIL_USER_DEFAULT
from app.tests.utils import delete_user


class TestRegisterbase(BaseSeleniumTestCase):

    def setUp(self):
        delete_user(USERNAME_USER_DEFAULT)
        super(TestRegisterbase, self).setUp()

    def tearDown(self) -> None:
        delete_user(USERNAME_USER_DEFAULT)
        super(TestRegisterbase, self).tearDown()

    def test_registerbase(self):
        self.logger.debug('Test Register User on Site')
        self.get("http://localhost:8080/register/")
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys(USERNAME_USER_DEFAULT)
        self.driver.find_element(By.ID, "id_password").send_keys(PASSWORD_USER_DEFAULT)
        self.driver.find_element(By.ID, "id_first_name").send_keys(EMAIL_USER_DEFAULT)
        self.driver.find_element(By.ID, "id_email").send_keys(EMAIL_USER_DEFAULT)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        self.driver.find_element(By.CSS_SELECTOR, "h2").click()
        WebDriverWait(self.driver, 30).until(
            expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR, "h2"), "Sucesso"))
        self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(7)").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(7)").text == "Usuario registrado com sucesso."
        assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(7)").text == "Usuario registrado com sucesso."
        self.driver.find_element(By.CSS_SELECTOR, ".sweet-alert").click()
