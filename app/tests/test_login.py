# Generated by Selenium IDE
import time

from selenium.webdriver.common.by import By

from app.tests.base import BaseSeleniumTestCase
from app.tests.constants import USERNAME_USER_DEFAULT, PASSWORD_USER_DEFAULT
from app.tests.utils import create_user, delete_user


class TestLogin(BaseSeleniumTestCase):
    def setUp(self):
        create_user()
        super(TestLogin, self).setUp()

    def tearDown(self) -> None:
        delete_user(USERNAME_USER_DEFAULT)
        super(TestLogin, self).tearDown()

    def test_login(self):
        print('Test Login on platform')
        self.get('http://localhost:8080/login/')
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys(USERNAME_USER_DEFAULT)
        self.driver.find_element(By.ID, "id_password").send_keys(PASSWORD_USER_DEFAULT)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".popover-navigation > .btn").click()
        self.driver.find_element(By.CSS_SELECTOR, ".jumbotron").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".display-5").text == "Lista de Músicas"
