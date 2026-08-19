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
        self.manage_link = page.get_by_role("link", name=ITEM_MANAGE_BUTTON)

    def add_item(self, name):
        safe_click(self.add_button)
        if name:
            paste_to_cell(self.page, name, self.name_cell)
        safe_click(self.save_button)

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
        names = [line.split(TAB)[0] for line in content.strip().split(NEWLINE) if line.strip()]
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
        # expect(target).to_be_visible(timeout=3000)
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
