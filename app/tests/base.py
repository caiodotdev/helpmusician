import os

import percy
from django.test import LiveServerTestCase
from selenium import webdriver


class BaseSeleniumTestCase(LiveServerTestCase):
    port = 8080

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.live_server_url)
        super(BaseSeleniumTestCase, self).setUp()

    def tearDown(self) -> None:
        self.driver.quit()
        super(BaseSeleniumTestCase, self).tearDown()
