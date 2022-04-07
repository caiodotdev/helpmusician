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
        if LOCAL:
            print('----- euu')
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
            self.driver.get(self.live_server_url)
        else:
            print('----- eleee')
            caps = {
                'platform': "win10",
                'browserName': "chrome",
                'version': "67.0",
                "resolution": "1024x768",
                "network": True,
                "video": True,
                "visual": True,
                "console": True,
            }
            gridUrl = "hub.lambdatest.com/wd/hub"
            url = "https://" + LT_USERNAME + ":" + LT_ACCESS_TOKEN + "@" + gridUrl
            self.driver = webdriver.Remote(
                command_executor=url,
                desired_capabilities=caps)
            self.driver.get(self.live_server_url)
        super(BaseSeleniumTestCase, self).setUp()

    def tearDown(self) -> None:
        self.driver.quit()
        super(BaseSeleniumTestCase, self).tearDown()
