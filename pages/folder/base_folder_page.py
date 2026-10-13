from playwright.sync_api import Page
from pages.components.dialog import Dialog
from utils.ui_selectors import *
from utils.ui_helpers import safe_click
from playwright.sync_api import Error

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

        popover = self.page.locator(POPOVER_CONTAINER)

        # 기존 방식: button 역할로 메뉴 찾기
        # 기존 테스트에 미치는 영향을 줄이기 위해 그대로 유지
        role_buttons = popover.get_by_role("button", name=action_name, exact=True)

        for index in range(role_buttons.count()):
            role_button = role_buttons.nth(index)

            if role_button.is_visible():
                safe_click(role_button)
                return

        # 보완 방식: 화면에 표시된 텍스트로 메뉴 찾기
        text_buttons = popover.get_by_text(action_name,exact=True)

        for index in range(text_buttons.count()):
            text_button = text_buttons.nth(index)

            if not text_button.is_visible():
                continue

            # 텍스트 span이 아니라 실제 클릭 가능한 부모 요소 검색
            clickable_parent = text_button.locator(
                "xpath=ancestor::*["
                "self::button or "
                "self::a or "
                "self::li or "
                "@role='button' or "
                "@role='menuitem'"
                "][1]"
            )

            if (
                clickable_parent.count() > 0
                and clickable_parent.is_visible()
            ):
                safe_click(clickable_parent)
                return

            # 클릭 가능한 부모 요소가 없는 구조라면 기존 방식 사용
            safe_click(text_button)
            return

        raise AssertionError(
            f"화면에 표시된 '{action_name}' 메뉴를 찾지 못했습니다."
        )     

    def get_error_message(self) -> str:
        return self.dialog.get_message()

    def is_folder_present(self, name: str, timeout: int = 5000) -> bool:
        try:
            self.get_treeitem(name).wait_for(state="visible", timeout=timeout)
            return True
        except Error:
            return False

    def assert_error_message(self, expected: str):
        actual = self.get_error_message()
        assert expected in actual, f"Expected error message to include '{expected}', but got '{actual}'"

    def assert_folder_is_present(self, name: str):
        assert self.is_folder_present(name), f"Expected folder '{name}' to be present."

    def close_duplicate_folder_dialog(self):
        safe_click(self.duplicate_confirm_button)
        safe_click(self.popup_close_button)
