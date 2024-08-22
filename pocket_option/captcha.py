from botasaurus.browser import Driver
from typing import TYPE_CHECKING


__all__ = ["CaptchaMixin"]


class CaptchaMixin:
    if TYPE_CHECKING:
        driver: Driver

    def solve_captcha(self): ...
