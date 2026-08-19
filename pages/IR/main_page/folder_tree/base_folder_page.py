from playwright.sync_api import Page
from pages.components.dialog import Dialog
from utils.ui_selectors import *
from utils.ui_helpers import safe_click

class BaseFolderPage:
    def __init__(self, page: Page):
        self.page = page
        self.dialog = Dialog(page)

        # 공통 버튼
        self.name_input = page.locator(BASE_FOLDER_NAME_INPUT)
        self.add_button = page.locator(BASE_FOLDER_ADD_LIST_BTN)
        self.save_button = page.locator(BASE_FOLDER_SAVE_BTN)
        self.delete_rule_button = page.locator(BASE_FOLDER_DELETE_RULE_BTN)
        self.final_delete_button = page.locator(BASE_FOLDER_FINAL_DELETE_BTN)
        self.duplicate_confirm_button = page.locator(BASE_FOLDER_DUPLICATE_DIALOG_CONFIRM_BTN)
        self.popup_close_button = page.locator(BASE_FOLDER_POPUP_CLOSE_BTN)

    def add_folder_name(self, name: str):
        self.name_input.fill(name)

    def click_add_button(self):
        safe_click(self.add_button)

    def click_save_button(self):
        safe_click(self.save_button)

    def click_delete_rule_button(self):
        safe_click(self.delete_rule_button)

    def click_final_delete_button(self):
        safe_click(self.final_delete_button)

    def confirm_dialog(self, repeat: int = 1):
        for _ in range(repeat):
            safe_click(self.page.get_by_role("button", name=BTN_TEXT_YES, exact=True))

    def get_treeitem(self, name: str):
        return self.page.get_by_role(BASE_FOLDER_TREEITEM_ROLE, name=name)

    def delete_folder(self, name: str):
        self._initiate_folder_action(name, BASE_FOLDER_DELETE_BTN_NAME)
        self.confirm_dialog()
        self.get_treeitem(name).wait_for(state="hidden", timeout=5000)

    def delete_folder_with_rules(self, name: str):
        self._initiate_folder_action(name, BASE_FOLDER_DELETE_BTN_NAME)
        self.confirm_dialog()
        self.click_delete_rule_button()
        self.confirm_dialog(2)
        self.click_final_delete_button()
        self.get_treeitem(name).wait_for(state="hidden", timeout=5000)

    def _initiate_folder_action(self, name: str, action_name: str):
        treeitem = self.get_treeitem(name)
        treeitem.wait_for(state="visible", timeout=5000)
        treeitem.scroll_into_view_if_needed()
        treeitem.click(button="right")
        safe_click(self.page.locator(POPOVER_CONTAINER).get_by_role("button", name=action_name, exact=True))

    def get_error_message(self) -> str:
        return self.dialog.get_message()

    def is_folder_present(self, name: str, timeout: int = 5000) -> bool:
        try:
            self.get_treeitem(name).wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False

    def assert_error_message(self, expected: str):
        actual = self.get_error_message()
        assert expected in actual, f"Expected error message to include '{expected}', but got '{actual}'"

    def assert_folder_is_present(self, name: str):
        assert self.is_folder_present(name), f"Expected folder '{name}' to be present."

    def close_duplicate_folder_dialog(self):
        safe_click(self.duplicate_confirm_button)
        safe_click(self.popup_close_button)
