from botasaurus.browser import Driver
from typing import TYPE_CHECKING
from re import sub
from twocaptcha import TwoCaptcha
from os import environ
from loguru import logger


__all__ = ["CaptchaMixin"]


class CaptchaMixin:
    if TYPE_CHECKING:
        driver: Driver

    def __init__(self):
        if "RUCAPTCHA_TOKEN" not in environ:
            raise ValueError("No RUCAPTCHA_TOKEN in environment")
        self.__solver = TwoCaptcha(environ.get("RUCAPTCHA_TOKEN"))

    def solve_captcha(self) -> bool:
        """
        Solves a captcha
        """
        try:
            captcha_iframe = self.driver.select(".g-recaptcha iframe", wait=10)
        except:
            return True
        url = captcha_iframe.src
        key = sub(r".*k=([a-zA-Z0-9]*)&.*", "\1", url)
        try:
            solved_key = self.__solver.recaptcha(
                sitekey=key, url=self.driver.current_url
            )
        except Exception as e:
            logger.exception(e)
            return False
        self.driver.run_js(
            f"document.querySelector('#g-recaptcha-response').text = {solved_key}"
        )
        self.driver.select(".submit-btn-wrap button").click()
        return True
