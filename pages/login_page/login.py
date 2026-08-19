from playwright.sync_api import Page
from utils.ui_selectors import (
    LOGIN_BTN_TEXT,
    INNOPRODUCT_BTN_NAME,
    INNORULES_BTN_NAME,
    INPUT_ID_SELECTOR,
    INPUT_PW_SELECTOR,
    ERROR_TOAST_SELECTOR,
)
from utils.ui_helpers import safe_click

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.innoproduct_button = page.get_by_role("button", name=INNOPRODUCT_BTN_NAME)
        self.innorules_button = page.get_by_role("button", name=INNORULES_BTN_NAME)
        self.input_id = page.locator(INPUT_ID_SELECTOR)
        self.input_pw = page.locator(INPUT_PW_SELECTOR)
        self.login_button = page.locator(f"button:has-text('{LOGIN_BTN_TEXT}')")

    # def login(self, user_id: str, user_pw: str):
    #     self.input_id.fill(user_id)
    #     self.input_pw.fill(user_pw)
    #     safe_click(self.login_button)

    # def ir_login(self, user_id: str, user_pw: str, url: str):
    #     safe_click(self.innorules_button)
    #     self.login(user_id, user_pw)

    # def pf_login(self, user_id: str, user_pw: str, url: str):
    #     safe_click(self.innoproduct_button)
    #     self.login(user_id, user_pw)

    def login(
        self,
        user_id: str | None,
        user_pw: str | None
    ):
        safe_user_id = "" if user_id is None else str(user_id)
        safe_user_pw = "" if user_pw is None else str(user_pw)

        self.input_id.fill(safe_user_id)
        self.input_pw.fill(safe_user_pw)
        safe_click(self.login_button)

    def ir_login(
        self,
        user_id: str | None,
        user_pw: str | None,
        url: str
    ):
        safe_click(self.innorules_button)
        self.login(user_id, user_pw)

    def pf_login(
        self,
        user_id: str | None,
        user_pw: str | None,
        url: str
    ):
        safe_click(self.innoproduct_button)
        self.login(user_id, user_pw)

    def get_error_message(self):
        locator = self.page.locator(ERROR_TOAST_SELECTOR)
        locator.wait_for(state="visible", timeout=3000)
        return locator.inner_text()
