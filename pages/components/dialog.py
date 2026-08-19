from pages.components.BaseDialog import BaseDialog
from playwright.sync_api import Page


class Dialog(BaseDialog):
    def __init__(self, page: Page):
        super().__init__(page)

