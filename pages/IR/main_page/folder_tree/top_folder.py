from pages.IR.main_page.folder_tree.base_folder_page import BaseFolderPage
from utils.ui_selectors import TOP_FOLDER_ADD_BTN
from utils.ui_helpers import safe_click

class TopFolderPage(BaseFolderPage):
    def __init__(self, page):
        super().__init__(page)
        self.add_top_folder_button = page.locator(TOP_FOLDER_ADD_BTN)

    def open_add_folder_popup(self):
        safe_click(self.add_top_folder_button)

    def create_top_folder(self, name: str):
        self.open_add_folder_popup()
        self.add_folder_name(name)
        self.click_add_button()
        self.click_save_button()
