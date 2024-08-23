from captcha import CaptchaMixin
from botasaurus.browser import Driver
from random import randint, choice
from loguru import logger


class Crawler(CaptchaMixin):
    def __init__(self, pocket_pass: str, pocket_login: str):
        self.login = pocket_login
        self.password = pocket_pass
        self.driver = Driver()
        self.url = "https://pocketoption.com/ru/cabinet/demo-quick-high-low/"

    def login_pocket(self):
        logger.info("The beginning of filling out the login form...")
        self.driver.get(self.url)

        self.driver.type('input[type="email"]', self.login, wait=10)
        self.driver.type('input[type="password"]', self.password)
        logger.info("The account login fields are filled in")
        self.driver.click('button.btn.btn-green-light')
        self.driver.sleep(5)
        logger.success("The parser logged into the account!")

    def check_balance(self):
        self.driver.get("https://pocketoption.com/ru/cabinet/demo-quick-high-low/")
        logger.info("Go to the demo account")
        balance = self.driver.select('div.balance-info-block__balance', wait=10).text.replace("$\n", '')
        logger.info(f"The balance is {balance}")
        if int(balance.split('.')[0]) <= 1000:
            logger.warning("The balance less than 1000")
            self.driver.click('div.balance-info-block__balance', wait=3)
            self.driver.click("span.btn-bl__text", wait=3)
            self.driver.type("input#dbm-balance", '50000', wait=3)
            self.driver.click("button.btn.btn-green-light.deposit-demo-btn.btn-block", wait=3)
            logger.success("The balance has been replenished by 50,000")
        else:
            logger.success("The balance is normal")

    def create_bid(self):
        self.driver.run_js(f'document.querySelector("#put-call-buttons-chart-1 > div > div.blocks-wrap > div.block.block--bet-amount > div.block__control.control.js-tour-block--bet-amount > div.control__value.value.value--several-items > div > input[type=text]").value = {1000}')
        logger.info(f'Bid == {1000}')
        low = self.driver.select("a.btn.btn-call")
        high = self.driver.select("a.btn.btn-put")

        button = choice([low, high])
        button.click()
        logger.success('Create bid!')

    def make_screenshot(self):
        self.driver.sleep(20)

        self.driver.save_screenshot()


if __name__ == '__main__':
    per = Crawler(
        pocket_pass="asdQWE1234532",
        pocket_login="randomnik122i94948@gmail.com",
    )
    per.login_pocket()
    per.check_balance()
    per.create_bid()
    per.make_screenshot()