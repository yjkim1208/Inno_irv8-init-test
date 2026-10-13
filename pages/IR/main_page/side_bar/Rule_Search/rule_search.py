import re
from pages.components.dialog import Dialog

class RuleSearchPage:
    def __init__(self, page):
        self.page = page
        self.dialog = Dialog(page)

    def open_rule_search_tab(self):
        """좌측 메뉴에서 '룰 찾기' 탭 클릭"""
        self.page.get_by_role("link", name="룰 찾기").click()

    def search_rule(self, rule_name: str):
        """룰 이름을 입력하고 검색 버튼 클릭"""
        self.page.locator("#in_search_keyword").click()
        self.page.locator("#in_search_keyword").fill(rule_name)
        self.page.locator("#btn_searchDetail").click()

    def is_rule_found(self, rule_name: str) -> bool:
        """룰 검색 결과에 해당 룰이 존재하는지 확인"""
        self.page.wait_for_load_state("networkidle")
        try:
            locator = self.page.get_by_role("cell", name=re.compile(rule_name))
            return locator.wait_for(state="visible", timeout=5000) is None
        except:
            return False


    def click_rule(self, rule_name: str):
        """검색된 룰 클릭"""
        self.page.get_by_role("cell", name=re.compile(rule_name)).locator("span, div").click()

    def delete_rule(self, rule_name: str):
        """룰 우클릭 후 삭제 메뉴 클릭"""
        self.page.get_by_role("cell", name=re.compile(rule_name)).click(button="right")
        self.page.get_by_role("menuitem", name="룰 삭제").click()

    def confirm_delete_popup(self):
        """삭제 확인 팝업에서 '예' 클릭"""
        self.page.get_by_role("button", name="예").click()

    def get_popup_message_text(self) -> str:
        """팝업 메시지 내용 반환"""
        self.page.wait_for_timeout(500)
        return self.dialog.get_message()

    def confirm_popup(self):
        """팝업 확인 버튼 클릭"""
        self.dialog.confirm()

    def close_search_dialog(self):
        """룰 찾기 검색창 닫기"""
        self.page.locator(
            "#div_rule_find_layer > .dialog__wrapper > .dialog__header > .dialog__header-actions > .dialog__button-close"
        ).click()
