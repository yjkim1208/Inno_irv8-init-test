from playwright.sync_api import Page
from utils.ui_selectors import BTN_TEXT_CONFIRM, BTN_TEXT_ADD

class UserPage:
    def __init__(self, page: Page):
        self.page = page
        
        # 메뉴 및 다이얼로그
        self.resource_menu = page.locator("#a_mng_res")
        self.user_mng_menu = page.locator("#a_manage_user_option_user")
        self.user_mng_dialog = page.locator("#div_manage_user_pop")
        self.user_add_dialog = page.locator("#div_manage_add_user_pop")
        
        # 사용자 추가 폼 입력 필드
        self.input_user_id = self.user_add_dialog.locator("#in_add_user_id")
        self.input_user_name = self.user_add_dialog.locator("#in_add_user_name")
        self.input_user_pw = self.user_add_dialog.locator("#in_add_user_pw")
        self.input_user_pw_check = self.user_add_dialog.locator("#in_add_user_pw_check")
        
        # 검색 필드
        self.search_input = self.user_mng_dialog.locator("#in_search_manage_users")
        self.search_button = self.user_mng_dialog.locator("#btn_search_manage_users")

    def open_user_management(self):
        """자원 관리 -> 사용자 관리 메뉴로 이동"""
        self.resource_menu.wait_for(state="visible", timeout=10000)
        self.resource_menu.hover()
        
        self.user_mng_menu.wait_for(state="attached", timeout=5000)
        self.user_mng_menu.click(force=True)
        
        self.user_mng_dialog.wait_for(state="visible", timeout=10000)

    def open_add_user_popup(self):
        """사용자 추가 팝업 생성"""
        add_button = self.user_mng_dialog.get_by_role("button", name=BTN_TEXT_ADD, exact=True)
        add_button.click()
        self.user_add_dialog.wait_for(state="visible", timeout=5000)

    def fill_user_info(self, user_id: str, user_name: str, user_pw: str, roles: list = None):
        """사용자 정보 입력 및 지정된 권한 역할 체크"""
        self.input_user_id.fill(user_id)
        self.input_user_name.fill(user_name)
        self.input_user_pw.fill(user_pw)
        self.input_user_pw_check.fill(user_pw)
        
        if roles:
            for role_name in roles:
                role_row = self.user_add_dialog.locator("tr", has_text=role_name)
                role_row.locator("input[type='checkbox']").check(force=True)

    def click_confirm_and_get_alert(self):
        """1차 확인 버튼 클릭 및 생성된 성공 알림 팝업 객체 닫기"""
        confirm_button = self.user_add_dialog.get_by_role("button", name=BTN_TEXT_CONFIRM, exact=True)
        confirm_button.click()
        
        success_alert = self.page.locator("#ir_message .ir-confirm.dialog.is-visible").last
        success_alert.wait_for(state="visible", timeout=10000)
        return success_alert

    def close_success_alert(self, success_alert):
        """알림 팝업 확인 클릭 및 팝업들이 닫힐 때까지 대기"""
        alert_confirm_btn = success_alert.get_by_role("button", name=BTN_TEXT_CONFIRM, exact=True)
        alert_confirm_btn.click()
        
        success_alert.wait_for(state="hidden", timeout=5000)
        #self.user_add_dialog.wait_for(state="hidden", timeout=5000)
        if self.user_add_dialog.is_visible():
            close_btn = self.user_add_dialog.locator(".dialog_button-close")
            if close_btn.is_visible():
                close_btn.click()
            self.user_add_dialog.wait_for(state="hidden", timeout=5000)

    def search_user(self, user_id: str):
        """사용자 ID로 검색하고 검색된 셀 요소를 반환"""
        self.search_input.fill(user_id)
        self.search_button.click()
        
        user_cell = self.user_mng_dialog.locator("span", has_text=user_id).first
        user_cell.wait_for(state="visible", timeout=10000)
        return user_cell