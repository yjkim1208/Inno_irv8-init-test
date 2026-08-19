from utils.ui_helpers import paste_to_cell, wait_for_cell_in_iframe, wait_until_button_disabled_in_iframe

class TableRulePage:
    def __init__(self, page):
        self.page = page

    def iframe(self):
        return self.page.locator("iframe").first.element_handle().content_frame()

    def fill_rule_content_and_save(self, content: str):
        """룰 내용 입력 후 저장"""
        target_cell = wait_for_cell_in_iframe(self.page, "td[data-row='1'][data-col='2']")
        paste_to_cell(self.page, content, target_cell)

        self.page.locator("iframe").content_frame.locator("button#btn_rule_save").click()
        wait_until_button_disabled_in_iframe(self.page, "btn_rule_save")
        
    def fill_rule_content_and_click_save(self, content: str):
        """룰 내용 입력 후 저장"""
        target_cell = wait_for_cell_in_iframe(self.page, "td[data-row='1'][data-col='2']")
        paste_to_cell(self.page, content, target_cell)

        self.page.locator("iframe").content_frame.locator("button#btn_rule_save").click()

    def get_error_popup(self) -> str:
        """iframe 안에 있는 에러 팝업 메시지 텍스트를 반환"""
        locator = self.iframe().locator(".popup-content")
        locator.wait_for(state="visible", timeout=5000)
        return locator.inner_text()
    
    def get_error_message_from_dialog(self, timeout=3000) -> str:
        """테스트 실행 후 뜨는 에러 메시지를 반환한다."""
        locator = self.iframe().locator("div.dialog__content div[class*='css-gmrzsa45']")
        try:
            locator.wait_for(state="visible", timeout=timeout)
            return locator.inner_text().strip()
        except TimeoutError:
            return ""
        
    def get_error_message_from_grid(self) -> str:
        """에러 리스트 그리드에서 (1,1) 셀의 텍스트를 추출"""
        iframe = self.page.frame_locator("iframe").first
        cell = iframe.locator('div#div_error_list td.ir_grid_cell[data-row="1"][data-col="1"]')
        cell.wait_for(state="visible", timeout=3000)
        return cell.inner_text()
    
    def check_all_condition_checkbox(self):
        checkbox = self.iframe().locator("#in_all_condition")
        if not checkbox.is_checked():
            checkbox.check()




    def delete_rule(self, rule_name):
        self.page.get_by_text(rule_name).click(button="right")
        self.page.get_by_role("menuitem", name="룰 삭제").click()
        self.page.get_by_role("button", name="예").click()

    def close_rule_tab(self):
        """열려 있는 룰 탭을 닫는다."""
        self.page.click('i[data-ir-tooltip-text="닫기"]')
    
    def yes_button(self):
        dialog = self.page.locator("div.dialog__content")
        dialog.get_by_role("button", name="예", exact=True).click()

    
    # def drag_drop(self, target, source):
    #     source.click()
    #     target.click()
    #     source.click()
    #     target.click()
    #     source.drag_to(target)