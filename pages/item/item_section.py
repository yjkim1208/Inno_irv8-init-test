from utils.ui_helpers import paste_to_cell, safe_click, safe_dblclick
from utils.ui_selectors import *
from pages.components.dialog import Dialog
from playwright.sync_api import expect


class ItemSection:
    def __init__(self, page):
        self.page = page
        self.dialog = Dialog(page)
        self.add_button = page.locator(ITEM_ADD_BUTTON)
        self.save_button = page.locator(ITEM_SAVE_BUTTON)
        self.search_box = page.locator(ITEM_SEARCH_BOX)
        self.search_button = page.locator(ITEM_SEARCH_BUTTON)
        self.rename_button = page.locator(ITEM_RENAME_BUTTON)
        self.delete_button = page.locator(ITEM_DELETE_BUTTON)
        self.confirm_button = page.locator(ITEM_CONFIRM_BUTTON)
        self.alert_ok_button = page.locator(ITEM_ALERT_OK_BUTTON)
        self.name_cell = page.locator(ITEM_NAME_CELL)
        self.popup_close_button = page.locator(ITEM_POPUP_DIALOG_CLOSE_BTN)
        self.manage_link = page.locator("#a_manage_item")
        self.item_layer = page.locator(ITEM_MANAGE_LAYER)
        self.alert_dialog = page.locator(ITEM_NAME_ALERT)

    def add_item(self, name, expect_success=True):
        # safe_click(self.add_button)
        # if name:
        #     paste_to_cell(self.page, name, self.name_cell)
        # safe_click(self.save_button)
        """항목 추가 팝업 열기 -> 데이터 입력 -> 저장 -> 알림 확인 프로세스"""
        # 1. 추가 버튼 클릭 및 항목 추가 레이어 대기
        safe_click(self.add_button)
        self.item_layer.wait_for(state="visible", timeout=3000)

        # 2. 항목 이름 그리드 셀에 데이터 붙여넣기
        if name:
            paste_to_cell(self.page, name, self.name_cell)

        # 3. 저장 버튼 클릭
        safe_click(self.save_button)

        # 4. 저장 완료 알림 팝업 대기 및 확인 클릭
        self.alert_dialog.wait_for(state="visible", timeout=3000)
        safe_click(self.alert_ok_button)

        # 5. 성공 케이스일 때 팝업 레이어가 닫힐 때까지 대기
        if expect_success:
            self.item_layer.wait_for(state="hidden", timeout=3000)
            self.page.wait_for_timeout(1000)

    def rename_item(self, name, new_name):
        self.search_and_select_item(name)
        safe_click(self.rename_button)
        paste_to_cell(self.page, new_name, self.name_cell)
        safe_click(self.save_button)

    def delete_item(self, name):
        self.search_and_select_item(name)
        safe_click(self.delete_button)
        safe_click(self.confirm_button)
        self.dialog.confirm()

    def delete_items(self, content):
        names = [line.split(TAB)[0] 
                for line in content.strip().split(NEWLINE) 
                if line.strip()
        ]
        for name in names:
            try:
                self.delete_item(name)
            except Exception as e:
                print(f"[⚠️] 삭제 실패: {name} - {e}")

    def search_and_select_item(self, name, dblclick=False):
        self.search_box.fill(name)
        self.page.wait_for_timeout(200)
        safe_click(self.search_button)
        target = self.page.locator(ITEM_GRID_ROW, has_text=name)
        safe_dblclick(target) if dblclick else safe_click(target)

    def open_popup(self):
        self.page.wait_for_timeout(1000)
        with self.page.expect_popup() as popup:
            safe_click(self.manage_link)
        popup_page = popup.value
        popup_page.wait_for_load_state("networkidle")
        return popup_page

    def close_popup(self):
        safe_click(self.popup_close_button)
