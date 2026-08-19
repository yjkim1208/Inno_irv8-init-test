# pages/rule_test_page.py

import ast
from playwright.sync_api import Page
from utils.ui_helpers import paste_to_cell, wait_for_cell_in_iframe
from pages.components.dialog import Dialog


class RuleTestPage:
    def __init__(self, page: Page):
        self.page = page
        self.dialog = Dialog(page)

    def iframe(self):
        return self.page.locator("iframe").first.element_handle().content_frame()

    def open_test_tab(self, folder_name: str, rule_name: str):
        """룰 더블클릭하여 테스트 탭 열기"""
        self.iframe().locator("button#btn_rule_test").click()

    def input_test_data(self, test_data: str):
        """테스트 항목 입력"""
        target_cell = wait_for_cell_in_iframe(self.page, "#div_test_all_area td[data-row='1'][data-col='4']")
        paste_to_cell(self.page, test_data, target_cell)

    def click_test_run(self):
        self.iframe().locator("#btn_test_run").click()

    def verify_test_result(self, expected_result: str) -> bool:
        """
        테스트 결과값이 기대값과 일치하는지 확인하고, True/False 반환
        """
        parsed_str = ast.literal_eval(f"'''{expected_result}'''")
        parsed_expected = [row.split('\t') for row in parsed_str.strip().split('\n')]
        actual_result = []

        frame = self.iframe()
        start_row = 3  # 결과가 시작되는 row 번호

        for r, row in enumerate(parsed_expected):
            result_row = []
            for c in range(1, len(row) + 1):
                selector = f'td[data-row="{start_row + r}"][data-col="{c}"] span'
                try:
                    cell = frame.locator(selector)
                    cell.wait_for(timeout=3000)
                    cell_text = cell.inner_text().strip()
                except Exception:
                    cell_text = ""
                result_row.append(cell_text)
            actual_result.append(result_row)

        return actual_result == parsed_expected

    def get_alert_message(self) -> str:
        return self.dialog.get_message()

    def close_alert_dialog(self):
        self.dialog.confirm()

    def get_error_message_from_dialog(self, timeout=3000) -> str:
        """테스트 실행 후 뜨는 에러 메시지를 반환한다."""
        locator = self.iframe().locator("div.dialog__content div[class*='css-gmrzsa45']")
        try:
            locator.wait_for(state="visible", timeout=timeout)
            return locator.inner_text().strip()
        except TimeoutError:
            return ""

    def close_error_dialog(self):
        iframe = self.iframe()
        button = iframe.locator("div.dialog__content button.button--primary:has-text('아니오')")
        if button.is_visible():
            button.click()
    
    def click_error_popup_ok_button(self):
        """iframe 안의 에러 팝업에서 '확인' 버튼 클릭"""
        iframe = self.page.frame_locator("iframe").first
        # popup-content가 포함된 div 내부의 '확인' 버튼만 선택
        popup = iframe.locator("div.dialog__content")
        ok_button = popup.get_by_role("button", name="확인")
        ok_button.wait_for(state="visible", timeout=5000)
        ok_button.click()



