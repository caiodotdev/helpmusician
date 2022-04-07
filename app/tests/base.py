from django.conf import settings
from django.test import LiveServerTestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

BROWSERSTACK_LOCAL_IDENTIFIER = settings.BROWSERSTACK_LOCAL_IDENTIFIER
BROWSERSTACK_USERNAME = settings.BROWSERSTACK_USERNAME
BROWSERSTACK_ACCESSKEY = settings.BROWSERSTACK_ACCESSKEY
LOCAL = True


class BaseSeleniumTestCase(LiveServerTestCase):
    port = 8080

    def setUp(self):
        if LOCAL:
            print('----- euu')
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
            self.driver.get(self.live_server_url)
        else:
            print('----- eleee')
            caps = {
                'browserstack.local': 'true',
                'browserstack.localIdentifier': BROWSERSTACK_LOCAL_IDENTIFIER,
                'os': "Windows",
                'os_version': "11",
                'browser': "Chrome",
                'browser_version': "99.0",
                'browserstack.selenium_version': "3.14.0"
            }
            self.driver = webdriver.Remote(
                command_executor='https://' + BROWSERSTACK_USERNAME + ":" + BROWSERSTACK_ACCESSKEY + '@hub-cloud.browserstack.com/wd/hub',
                desired_capabilities=caps)
            self.driver.get(self.live_server_url)
        super(BaseSeleniumTestCase, self).setUp()

    def tearDown(self) -> None:
        self.driver.quit()
        super(BaseSeleniumTestCase, self).tearDown()
