from playwright.sync_api import Page
from pages.components.dialog import Dialog
from utils.ui_helpers import paste_to_cell, safe_click, safe_dblclick
from utils.ui_selectors import *
import re

class MakeRulePage:
    def __init__(self, page: Page):
        self.page = page
        self.dialog = Dialog(page)

        # 버튼/필드
        self.add_rule_button = page.locator(RULE_BTN_ADD)
        self.confirm_button = page.locator(RULE_BTN_CONFIRM)
        self.rule_name_field = page.locator(RULE_INPUT_NAME)

        # 템플릿 라디오 라벨
        self.template_radio_label = lambda value: page.locator(f"label:has(input#in_template_{value}) span")

        # 셀 및 체크박스
        self.return_cell = page.locator(RULE_RETURN_CELL).first
        self.delete_checkboxes = page.locator(RULE_DELETE_CHECKBOXES)

        # 반환값 단일/다중 선택
        self.radio_single_return = page.locator(RULE_RADIO_SINGLE_RETURN)
        self.radio_multi_return = page.locator(RULE_RADIO_MULTI_RETURN)

        # 룰 트리
        self.rule_tree_items = page.locator(RULE_TREE_ITEMS)

        # "룰 추가" 팝업 닫기 버튼
        self.rule_add_popup = page.locator(
            RULE_ADD_POPUP_WRAPPER,
            has=page.locator("strong.dialog__header-title", has_text=RULE_ADD_POPUP_TITLE)
        )
        self.rule_add_popup_close_button = self.rule_add_popup.locator(RULE_ADD_POPUP_CLOSE_BTN)

        # 에러 팝업 확인 버튼
        self.error_confirm_button = page.locator(RULE_ERROR_CONFIRM_BTN)

    # ===== 페이지 진입 =====
    def go_to_rule_page(self, folder_name: str, rule_name: str):
        folder_treeitem = self.page.get_by_role(BASE_FOLDER_TREEITEM_ROLE, name=folder_name)
        safe_click(folder_treeitem.get_by_text(folder_name, exact=True))
        safe_dblclick(self.page.get_by_text(rule_name, exact=True))

    # ===== 룰 추가 =====
    def open_add_rule_popup(self, folder_name: str):
        treeitem = self.page.locator(f"div[role='{BASE_FOLDER_TREEITEM_ROLE}']").filter(
            has=self.page.locator("span", has_text=re.compile(rf"^{re.escape(folder_name)}$"))
        ).first
        span = treeitem.locator("span", has_text=re.compile(rf"^{re.escape(folder_name)}$"))
        span.scroll_into_view_if_needed(timeout=2000)
        safe_click(span)
        self.page.wait_for_timeout(300)
        safe_click(self.add_rule_button)

    def select_rule_template(self, template_value: int):
        safe_click(self.template_radio_label(template_value))

    def input_rule_name(self, name: str):
        safe_click(self.rule_name_field)
        self.page.keyboard.type(name)

    def input_return_item(self, value: str):
        paste_to_cell(self.page, value, self.return_cell)

    def check_all_delete_checkboxes(self):
        self.page.wait_for_timeout(500)
        count = self.delete_checkboxes.count()
        for i in range(count):
            checkbox = self.delete_checkboxes.nth(i)
            checkbox.wait_for(state="visible", timeout=3000)
            self.page.wait_for_timeout(200)
            if not checkbox.is_checked():
                safe_click(checkbox)
                self.page.wait_for_timeout(200)

    def click_confirm(self):
        safe_click(self.confirm_button)

    def select_single_return_value(self):
        safe_click(self.radio_single_return)

    def select_multiple_return_value(self):
        safe_click(self.radio_multi_return)

    def create_rule(self, folder_name: str, name: str, return_value: str, template_value: int):
        self.open_add_rule_popup(folder_name)
        self.input_rule_name(name)
        self.select_rule_template(template_value)
        self.input_return_item(return_value)
        self.click_confirm()

    def create_multiple_ruturn_rule(self, folder_name: str, name: str, return_value: str, template_value: int):
        self.open_add_rule_popup(folder_name)
        self.input_rule_name(name)
        self.select_rule_template(template_value)
        self.input_return_item(return_value)
        self.select_multiple_return_value()
        self.click_confirm()

    def is_rule_in_tree(self, rule_name: str) -> bool:
        self.page.wait_for_load_state("networkidle")
        locator = self.rule_tree_items.filter(
            has=self.page.locator("span", has_text=rule_name)
        )
        try:
            locator.wait_for(state="visible", timeout=7000)
            return True
        except:
            return False

    def close_rule_add_popup(self):
        safe_click(self.rule_add_popup_close_button)

    # ===== 에러/알림 처리 =====
    def get_alert_message(self) -> str:
        return self.dialog.get_message()

    def close_alert_dialog(self):
        self.dialog.confirm()

    def is_confirm_button_disabled(self) -> bool:
        return self.confirm_button.is_disabled()

    def close_error_dialog(self):
        safe_click(self.error_confirm_button)
