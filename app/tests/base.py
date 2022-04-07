import os

from django.test import LiveServerTestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from django.conf import settings

BROWSERSTACK_LOCAL_IDENTIFIER = settings.BROWSERSTACK_LOCAL_IDENTIFIER
BROWSERSTACK_USERNAME = settings.BROWSERSTACK_USERNAME
BROWSERSTACK_ACCESSKEY = settings.BROWSERSTACK_ACCESSKEY
DEBUG = settings.DEBUG


class BaseSeleniumTestCase(LiveServerTestCase):
    port = 8080

    def setUp(self):
        if DEBUG:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
            self.driver.get(self.live_server_url)
        else:
            caps = {
                'browserstack.local': 'true',
                'browserstack.localIdentifier': BROWSERSTACK_LOCAL_IDENTIFIER,
            }
            self.driver = webdriver.Remote(
                command_executor='https://' + BROWSERSTACK_USERNAME + ":" + BROWSERSTACK_ACCESSKEY + '@hub-cloud.browserstack.com/wd/hub',
                desired_capabilities=caps)
        super(BaseSeleniumTestCase, self).setUp()

    def tearDown(self) -> None:
        self.driver.quit()
        super(BaseSeleniumTestCase, self).tearDown()
