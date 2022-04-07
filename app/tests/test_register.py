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
        # Test name: register_base
        # Step # | name | target | value
        # 1 | open | http://localhost:8080/register/ |
        self.driver.get("http://localhost:8080/register/")
        # 2 | setWindowSize | 1382x744 |
        self.driver.maximize_window()
        # 3 | click | id=id_username |
        self.driver.find_element(By.ID, "id_username").click()
        # 4 | type | id=id_username | caiomarin
        self.driver.find_element(By.ID, "id_username").send_keys(USERNAME_USER_DEFAULT)
        # 5 | type | id=id_password | oficinag3
        self.driver.find_element(By.ID, "id_password").send_keys(PASSWORD_USER_DEFAULT)
        # 6 | type | id=id_first_name | Caio
        self.driver.find_element(By.ID, "id_first_name").send_keys(EMAIL_USER_DEFAULT)
        # 7 | type | id=id_email | caiomarinho89@gmail.com
        self.driver.find_element(By.ID, "id_email").send_keys(EMAIL_USER_DEFAULT)
        # 8 | click | css=.btn-primary |
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        # 9 | click | css=h2 |
        self.driver.find_element(By.CSS_SELECTOR, "h2").click()
        # 10 | waitForText | css=h2 | Sucesso
        WebDriverWait(self.driver, 30).until(
            expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR, "h2"), "Sucesso"))
        # 11 | click | css=p:nth-child(7) |
        self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(7)").click()
        # 12 | verifyText | css=p:nth-child(7) | Usuario registrado com sucesso.
        assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(7)").text == "Usuario registrado com sucesso."
        # 13 | assertText | css=p:nth-child(7) | Usuario registrado com sucesso.
        assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(7)").text == "Usuario registrado com sucesso."
        # 14 | click | css=.sweet-alert |
        self.driver.find_element(By.CSS_SELECTOR, ".sweet-alert").click()
