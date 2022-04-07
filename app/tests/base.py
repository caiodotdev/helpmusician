from django.conf import settings
from django.test import LiveServerTestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

BROWSERSTACK_LOCAL_IDENTIFIER = settings.BROWSERSTACK_LOCAL_IDENTIFIER
BROWSERSTACK_USERNAME = settings.BROWSERSTACK_USERNAME
BROWSERSTACK_ACCESSKEY = settings.BROWSERSTACK_ACCESSKEY
LOCAL = False

LT_USERNAME = settings.LT_USERNAME
LT_ACCESS_TOKEN = settings.LT_ACCESS_TOKEN


class BaseSeleniumTestCase(LiveServerTestCase):
    port = 8080

    def setUp(self):
        super(BaseSeleniumTestCase, self).setUp()
        if LOCAL:
            print('----- Local')
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
            self.driver.get(self.live_server_url)
        else:
            print('----- Remoto')
            caps = {
                "platform": "Windows 10",
                "browserName": "Chrome",
                "version": "99.0",
                "resolution": "1280x800",
                "selenium_version": "3.141.0",
                "tunnel": True,
                "console": "true",
                "network": True,
                "video": True,
                "driver_version": "99.0"
            }
            gridUrl = "hub.lambdatest.com/wd/hub"
            url = "https://" + LT_USERNAME + ":" + LT_ACCESS_TOKEN + "@" + gridUrl
            self.driver = webdriver.Remote(
                command_executor=url,
                desired_capabilities=caps)
            # caps = {
            #     'browserstack.local': 'true',
            #     'browserstack.localIdentifier': BROWSERSTACK_LOCAL_IDENTIFIER,
            # }
            # self.driver = webdriver.Remote(
            #     command_executor='https://' + BROWSERSTACK_USERNAME + ":" + BROWSERSTACK_ACCESSKEY + '@hub-cloud.browserstack.com/wd/hub',
            #     desired_capabilities=caps)
            self.driver.get(self.live_server_url)


    def tearDown(self) -> None:
        self.driver.quit()
        super(BaseSeleniumTestCase, self).tearDown()
