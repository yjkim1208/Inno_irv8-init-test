from pages.components.BaseDialog import BaseDialog
from playwright.sync_api import Page

class IframeDialog(BaseDialog):
    def __init__(self, page: Page, iframe_index: int = 1):
        frame = page.frame_locator("iframe").nth(iframe_index)
        super().__init__(frame)