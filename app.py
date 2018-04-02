import logging
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import EMAIL, PASSWORD
from wishes import BIRTHDAY_WISHES


logging.basicConfig(level=logging.INFO,
                    format=' %(asctime)s - %(levelname)s - %(message)s')


class FB_Auto_Birthday(object):

    def __init__(self):
        self.driver = None
        self.email = None
        self.password = None
        self.login = False

    def send_birthday_wishes(self):
        divs = self.get_birthday_list()
        birthday_div = divs.find_element_by_xpath("..")

        def is_today_birthday():
            return "Today's Birthdays" in birthday_div.text

        def execute_no_birthday():
            logging.info("There is no birthday today")
            self.driver.close()

        def execute_birthday():
            text_areas = birthday_div.find_elements_by_tag_name("textArea")

            if len(text_areas) == 0:
                logging.info("You have wished everyone already :)")
                self.driver.close()

            import random

            for text in text_areas:
                text.send_keys(random.choice(BIRTHDAY_WISHES))
                text.send_keys(Keys.RETURN)
                time.sleep(10)

        if is_today_birthday():
            execute_birthday()
        else:
            execute_no_birthday()

    def get_birthday_list(self):
        return self.driver.find_element_by_id("birthdays_today_card")

    def getting_login_details(self):
        def ask_email():
            email = input("What's your FB email? >> ") if len(
                EMAIL) == 0 else EMAIL
            self.email = email

        def ask_password():
            import getpass
            password = getpass.getpass("What's your FB password? >> ") if len(
                PASSWORD) == 0 else PASSWORD
            self.password = password

        ask_email()
        ask_password()

    def firing_up_driver(self):
        def initialize_driver():
            try:  # Linux
                logging.info("Initializing chrome for linux")
                self.driver = webdriver.Chrome('./chromedriver_linux')
            except:
                logging.error("Can't initialize chrome for linux")
                try:
                    logging.info("Initializing chrome for windows")
                    self.driver = webdriver.Chrome('./chromedriver_win.exe')
                except:
                    logging.error("Can't initialize chrome for windows")
                    try:
                        logging.info("Initializing chrome for mac")
                        self.driver = webdriver.Chrome('./chromedriver_mac')
                    except:
                        logging.error("Can't initialize chrome for mac")
                        logging.error("Can't initialize chrome at all")
                    else:
                        logging.info("Setup successful")
                else:
                    logging.info("Setup successful")
            else:
                logging.info("Setup successful")

        def driver_open_url():
            self.driver.get("http://facebook.com/events/birthdays")

        initialize_driver()
        driver_open_url()

    def sending_login_details(self):
        def send_email():
            em = self.driver.find_element_by_name("email")
            em.clear()
            em.send_keys(self.email)

        def send_password():
            pwd = self.driver.find_element_by_name("pass")
            pwd.clear()
            pwd.send_keys(self.password)
            pwd.send_keys(Keys.RETURN)

        send_email()
        send_password()

    def sign_in(self):
        def login_attempt():
            self.getting_login_details()
            self.firing_up_driver()
            logging.info("Logging in...")
            self.sending_login_details()

        while self.login is False:
            login_attempt()

            try:
                self.get_birthday_list()
            except:
                # self.driver.close()
                logging.error("Wrong email or password?")
                global EMAIL
                global PASSWORD
                EMAIL = ""
                PASSWORD = ""
            else:
                self.login = True
                logging.info("Login Successful!")

    def main(self):
        self.sign_in()
        self.send_birthday_wishes()


def main():
    app = FB_Auto_Birthday()
    app.main()

if __name__ == '__main__':
    main()
