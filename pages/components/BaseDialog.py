from utils.ui_selectors import DIALOG_CONFIRM_BTN_SELECTOR, DIALOG_MESSAGE_SELECTOR
from utils.ui_helpers import safe_click

class BaseDialog:
    def __init__(self, frame):
        self.frame = frame
        self.message = self.frame.locator(DIALOG_MESSAGE_SELECTOR).first
        self.confirm_button = self.frame.locator(DIALOG_CONFIRM_BTN_SELECTOR)

    def get_message(self, timeout: int = 5000) -> str:
        self.message.wait_for(state="visible", timeout=timeout)
        return self.message.inner_text().strip()

    def confirm(self, timeout: int = 5000):
        safe_click(self.confirm_button, timeout)
        
