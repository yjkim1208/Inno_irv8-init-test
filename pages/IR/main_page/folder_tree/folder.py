from pages.IR.main_page.folder_tree.base_folder_page import BaseFolderPage
from utils.ui_selectors import *
from utils.ui_helpers import safe_click

class FolderPage(BaseFolderPage):
    def __init__(self, page):
        super().__init__(page)

        # 폴더 관련 요소
        self.folder_list_area = page.locator(FOLDER_LIST_AREA)
        self.add_folder_button = page.get_by_role("button", name=FOLDER_ADD_BTN_NAME)
        self.rename_button = page.get_by_role("button", name=FOLDER_RENAME_BTN_NAME)
        self.rename_input = page.locator(FOLDER_RENAME_INPUT)
        self.rename_save_button = page.locator(FOLDER_RENAME_SAVE_BTN)
        self.cancel_delete_button = page.get_by_role("button", name=BTN_TEXT_NO, exact=True)
        self.duplicate_name_confirm_button = page.locator(BASE_FOLDER_DUPLICATE_DIALOG_CONFIRM_BTN)
        self.duplicate_name_popup_close = page.locator(FOLDER_NAME_DUPLICATE_POPUP_CLOSE)

    def open_add_folder_popup(self, top_folder_name: str):
        self.folder_list_area.get_by_text(top_folder_name).click(button="right")
        safe_click(self.add_folder_button)

    def create_folder(self, top_folder: str, name: str):
        self.open_add_folder_popup(top_folder)
        self.add_folder_name(name)
        self.click_add_button()
        self.click_save_button()

    def rename_folder(self, name: str, change_name: str):
        self.folder_list_area.get_by_text(name, exact=True).click(button="right")
        safe_click(self.rename_button)
        self.rename_input.fill(change_name)
        safe_click(self.rename_save_button)

    def cancel_delete_folder(self, name: str):
        self._initiate_folder_action(name, BASE_FOLDER_DELETE_BTN_NAME)
        safe_click(self.cancel_delete_button)

    def close_duplicate_folder_name_dialog(self):
        safe_click(self.duplicate_name_confirm_button)
        safe_click(self.duplicate_name_popup_close)
