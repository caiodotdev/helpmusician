import logging
import time

from django.conf import settings
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from app.tests.constants import USERNAME_USER_DEFAULT, PASSWORD_USER_DEFAULT
from app.tests.utils import create_user, delete_user, create_sourcetrack_dynamicmix, delete_track_and_mix

BROWSERSTACK_LOCAL_IDENTIFIER = settings.BROWSERSTACK_LOCAL_IDENTIFIER
BROWSERSTACK_USERNAME = settings.BROWSERSTACK_USERNAME
BROWSERSTACK_ACCESSKEY = settings.BROWSERSTACK_ACCESSKEY
LOCAL = settings.LOCAL_TESTS

LT_USERNAME = settings.LT_USERNAME
LT_ACCESS_TOKEN = settings.LT_ACCESS_TOKEN


class BaseSeleniumTestCase(LiveServerTestCase):
    port = 8080

    logger = None

    def setupLogger(self):
        self.logger = logging.getLogger(__name__)
        fileHandler = logging.FileHandler('logfile.log')
        self.logger.addHandler(fileHandler)
        self.logger.setLevel(logging.DEBUG)

    def setUp(self):
        super(BaseSeleniumTestCase, self).setUp()
        if LOCAL:
            print('----- Local')
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
            self.driver.get(self.live_server_url)
        else:
            print('----- Remoto')
            # caps = {
            #     "platform": "Windows 10",
            #     "browserName": "Chrome",
            #     "version": "99.0",
            #     "resolution": "1280x800",
            #     "selenium_version": "3.141.0",
            #     "tunnel": True,
            #     "console": "true",
            #     "network": True,
            #     "video": True,
            #     "driver_version": "99.0"
            # }
            # gridUrl = "hub.lambdatest.com/wd/hub"
            # url = "https://" + LT_USERNAME + ":" + LT_ACCESS_TOKEN + "@" + gridUrl
            # self.driver = webdriver.Remote(
            #     command_executor=url,
            #     desired_capabilities=caps)
            caps = {
                'browserstack.local': 'true',
                'browserstack.localIdentifier': BROWSERSTACK_LOCAL_IDENTIFIER,
            }
            self.driver = webdriver.Remote(
                command_executor='https://' + BROWSERSTACK_USERNAME + ":" + BROWSERSTACK_ACCESSKEY + '@hub-cloud.browserstack.com/wd/hub',
                desired_capabilities=caps)
            self.get(self.live_server_url)

    def tearDown(self) -> None:
        self.driver.quit()
        super(BaseSeleniumTestCase, self).tearDown()

    def get(self, url):
        self.driver.get(url)
        self.driver.set_window_size(1920, 1200)

    def do_login(self):
        self.get("http://localhost:8080/")
        self.driver.find_element(By.CSS_SELECTOR, ".btn-secondary").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys(USERNAME_USER_DEFAULT)
        self.driver.find_element(By.ID, "id_password").send_keys(PASSWORD_USER_DEFAULT)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".popover-navigation > .btn").click()
        self.driver.find_element(By.CSS_SELECTOR, ".jumbotron").click()


class BaseLoggedSeleniumTestCase(BaseSeleniumTestCase):
    user = None

    def setUp(self):
        self.user = create_user()
        create_sourcetrack_dynamicmix(self.user)
        super(BaseLoggedSeleniumTestCase, self).setUp()
        self.do_login()

    def tearDown(self) -> None:
        delete_user(USERNAME_USER_DEFAULT)
        delete_track_and_mix(self.user)
        super(BaseLoggedSeleniumTestCase, self).tearDown()
