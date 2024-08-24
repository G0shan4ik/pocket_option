from os import environ

from .captcha import CaptchaMixin
from botasaurus.browser import Driver
from random import choice
from loguru import logger
from random import randint


AUTH_LOGIN = environ.get("AUTH_LOGIN", "randomnik122i94948@gmail.com")
AUTH_PASSWORD = environ.get("AUTH_PASSWORD", "asdQWE1234532")
MIN_BALANCE = environ.get("MIN_BALANCE", 1000)
BID = environ.get("BID", 50)  # sum


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
        self.driver.click("button.btn.btn-green-light")
        self.driver.sleep(5)
        logger.success("The parser logged into the account!")

    def check_balance(self):
        self.driver.get(
            "https://pocketoption.com/ru/cabinet/demo-quick-high-low/")
        logger.info("Go to the demo account")
        balance = self.driver.select(
            "div.balance-info-block__balance", wait=10
        ).text.replace("$\n", "")
        logger.info(f"The balance is {balance}")

        if int(balance.split(".")[0]) <= MIN_BALANCE:
            logger.warning("The balance less than 1000")
            self.driver.click("div.balance-info-block__balance", wait=10)
            self.driver.click("span.btn-bl__text", wait=10)
            self.driver.type("input#dbm-balance", "50000", wait=10)
            self.driver.click(
                "button.btn.btn-green-light.deposit-demo-btn.btn-block", wait=10
            )
            logger.success("The balance has been replenished by 50,000")
            self.driver.run_js(
                "document.querySelector('.assets-block').style.display = 'none'"
            )
        else:
            logger.success("The balance is normal")

    def set_time(self) -> int:
        """
        Set bid time, and return time in seconds
        """
        time_element = self.driver.select(".block--expiration-inputs", wait=10)
        while time_element.select(".block__title").text.strip().lower() != "время":
            # Если стоит неправильный формат времени, в тайтеле "Время UTC+3"
            time_element.select(".buttons > a", wait=5).click()
        # Нажимаем на блок с временем, чтобы появилось всплывающее окно
        time_element.select(".value__val", wait=5).click()
        # Set time
        time = randint(10, 59)
        logger.info(f"Set {time}sec")
        # Выбираем `rw` с секундами
        input = self.driver.select(
            ".trading-panel-modal__in>.rw:nth-of-type(3)", wait=10
        )
        val = int(input.select("input").get_attribute("value"))
        # Нажимаем либо плюс, либо минус
        if val > time:
            for _ in range(val - time):
                input.select(".btn-minus").click()
        if val < time:
            for _ in range(time - val):
                input.select(".btn-plus").click()
        time_element.select(".value__val").click()
        return time

    def create_bid(self):
        while not self.driver.select_all(
            "li.alist__item:not(.alist__item--no-active)", wait=1
        ):
            self.driver.click("i.fa.fa-caret-down", wait=10)
        all_stocks = [
            item.select("a.alist__link")
            for item in self.driver.select_all(
                "li.alist__item:not(.alist__item--no-active)", wait=10
            )
        ]
        btn_stocks = choice(all_stocks)
        pair = btn_stocks.select(".alist__label").text
        btn_stocks.click()
        logger.success(f"Select {pair}")
        time = self.set_time()

        self.driver.run_js(
            f'document.querySelector("#put-call-buttons-chart-1 > div > div.blocks-wrap > div.block.block--bet-amount > div.block__control.control.js-tour-block--bet-amount > div.control__value.value.value--several-items > div > input[type=text]").value = {
                BID}'
        )
        logger.info(f"Bid == {BID}")
        low = self.driver.select("a.btn.btn-call")
        high = self.driver.select("a.btn.btn-put")

        self.driver.run_js(
            "document.querySelector('.assets-block').style.display = 'none'"
        )

        self.driver.sleep(1)

        btn_bid = choice([low, high])
        btn_bid.click()
        self.driver.sleep(1)
        self.driver.save_screenshot("screen1.png")
        logger.success("Create bid!")
        return {
            "time": time,
            "pair": pair,
            "call": "call" in btn_bid.get_attribute("class"),
        }

    def make_screenshot(self):
        self.driver.select("div.no-deals", wait=100)
        self.driver.sleep(1)
        self.driver.save_screenshot("screen2.png")
        logger.success("Save screenshot")

    def step(self):
        self.check_balance()
        data = self.create_bid()
        self.make_screenshot()
        return data


if __name__ == "__main__":
    per = Crawler(
        pocket_pass=AUTH_PASSWORD,
        pocket_login=AUTH_LOGIN,
    )
    per.login_pocket()
    per.step()
