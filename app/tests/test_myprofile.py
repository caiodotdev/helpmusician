# Generated by Selenium IDE
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from app.tests.base import BaseLoggedSeleniumTestCase
from app.tests.constants import USERNAME_USER_DEFAULT, EMAIL_USER_DEFAULT, NAME_USER_DEFAULT

NEW_SURNAME_USER = "Newsurname"


class TestPlayaudiomixer(BaseLoggedSeleniumTestCase):

    def test_myprofile(self):
        assert self.driver.find_element(By.LINK_TEXT, "Meu Perfil").text == "Meu Perfil"
        self.driver.find_element(By.LINK_TEXT, "Meu Perfil").click()
        value = self.driver.find_element(By.ID, "id_username").get_attribute("value")
        assert value == USERNAME_USER_DEFAULT
        value = self.driver.find_element(By.ID, "id_email").get_attribute("value")
        assert value == EMAIL_USER_DEFAULT
        self.driver.find_element(By.ID, "id_last_name").click()
        self.driver.find_element(By.ID, "id_last_name").send_keys(NEW_SURNAME_USER)
        self.driver.find_element(By.CSS_SELECTOR, "form").click()
        elements = self.driver.find_elements(By.LINK_TEXT, "Voltar")
        assert len(elements) > 0
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        elements = self.driver.find_elements(By.ID, "alterar")
        assert len(elements) > 0
        self.driver.find_element(By.ID, "alterar").click()
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "h2:nth-child(6)")))
        self.driver.find_element(By.CSS_SELECTOR, "h2:nth-child(6)").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "h2:nth-child(6)").text == "Sucesso"
        self.driver.find_element(By.CSS_SELECTOR, ".sweet-alert").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(7)").text == "Perfil atualizado com sucesso"
        self.driver.find_element(By.CSS_SELECTOR, ".confirm").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".display-5").text == "Lista de Músicas"
        self.driver.find_element(By.LINK_TEXT, "Meu Perfil").click()
        value = self.driver.find_element(By.ID, "id_last_name").get_attribute("value")
        assert value == NEW_SURNAME_USER
        value = self.driver.find_element(By.ID, "id_first_name").get_attribute("value")
        assert value == NAME_USER_DEFAULT
