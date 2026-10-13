from playwright.sync_api import Page
from pages.components.dialog import Dialog
from utils.ui_helpers import paste_to_cell,safe_click
import re

class EditRulePage:
    def __init__(self, page: Page):
        self.page = page
        self.dialog = Dialog(page)
        self.rule_name_input = page.locator("input#in_rule_name")
        self.confirm_button = page.locator("button#btn_save")
        self.rule_grid = page.locator("#ruleTree")

    def open_edit_rule_popup(self, folder_name: str, rule_name: str):
        """정확한 폴더와 룰을 선택하여 룰 정보 변경 팝업을 연다"""
        
        # 1. 정확한 폴더 클릭 (중복 방지 위해 정규식 + filter 사용)
        folder_item = self.page.locator("div[role='treeitem']").filter(
            has=self.page.locator("span", has_text=re.compile(rf"^{re.escape(folder_name)}$"))
        ).first

        folder_span = folder_item.locator("span", has_text=re.compile(rf"^{re.escape(folder_name)}$"))
        folder_span.scroll_into_view_if_needed()
        # folder_span.click(force=True)
        safe_click(folder_span)

        self.page.wait_for_timeout(500)  # 네트워크 안정화용

        # 2. 룰 이름이 정확히 일치하는 항목 우클릭
        rule_item = self.page.locator("div[role='treeitem']").filter(
            has=self.page.locator("span", has_text=re.compile(rf"^{re.escape(rule_name)}$"))
        ).first

        rule_span = rule_item.locator("span", has_text=re.compile(rf"^{re.escape(rule_name)}$"))
        rule_span.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)  # 네트워크 안정화용
        rule_span.click(button="right", force=True)
        
        self.page.wait_for_timeout(500)  # 네트워크 안정화용
        # 3. 팝업 메뉴에서 '룰 정보 변경' 클릭
        self.page.get_by_role("button", name="룰 정보 변경").click()


    def change_rule_name(self, new_name: str):
        self.rule_name_input.fill(new_name)

    def click_confirm(self):
        self.confirm_button.click()

    def get_alert_message(self) -> str:
        return self.dialog.get_message()

    def is_rule_in_tree(self, rule_name: str) -> bool:
            """
            룰 트리 내에 해당 이름의 룰이 존재하는지 확인합니다.
            """
            self.page.wait_for_load_state("networkidle")
            locator = self.page.locator("#ruleTree").get_by_role("treeitem").filter(
                has=self.page.locator("span", has_text=rule_name)
            )
            try:
                locator.wait_for(state="visible", timeout=7000)  # 최대 7초 기다림
                return True
            except:
                return False
            
    
    def close_error_dialog(self):
        self.page.locator("#ir_message").get_by_role("button", name="확인").click()

    def close_rule_dialog(self):
        self.page.locator("strong.dialog__header-title", has_text="룰 정보 변경").locator("xpath=../../..").locator(".dialog__button-close").click()
