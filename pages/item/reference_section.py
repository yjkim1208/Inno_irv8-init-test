from utils.ui_helpers import paste_to_cell, safe_click
from utils.ui_selectors import *
from pages.components.dialog import Dialog

class ReferenceSection:
    def __init__(self, page):
        self.page = page
        self.dialog = Dialog(page)
        self.edit_button = page.locator(REF_EDIT_BUTTON)
        self.cell = page.locator(REF_GRID_CELL)
        self.grid = page.locator(REF_GRID_CONTAINER)
        self.delete_button = page.locator(REF_DELETE_ROW_BUTTON)
        self.save_button = page.locator(REF_SAVE_BUTTON)
        self.panel_rows = page.locator(REF_SIDE_PANEL_ROWS)
        self.alert_ok_button = page.locator(ITEM_ALERT_OK_BUTTON)
        self.dialog_close_button = page.locator(REF_DIALOG_CLOSE_BTN)

    def add_reference(self, item_section, name, ref):
        item_section.search_and_select_item(name, dblclick=True)
        safe_click(self.edit_button)
        if ref:
            paste_to_cell(self.page, ref, self.cell)
        self.save_and_confirm()

    def delete_reference(self, item_section, item_name, delete_target):
        item_section.search_and_select_item(item_name, dblclick=True)
        safe_click(self.edit_button)
        safe_click(self.grid.get_by_role("cell", name=delete_target).locator("div"))
        safe_click(self.delete_button)
        self.save_and_confirm()
        safe_click(self.alert_ok_button)


    def delete_all_references(self, item_section, name):
        item_section.search_and_select_item(name, dblclick=True)
        safe_click(self.edit_button)
        while self.delete_button.is_enabled():
            safe_click(self.delete_button)
            self.page.wait_for_timeout(100)
        self.save_and_confirm()
        safe_click(self.alert_ok_button)

    def save_and_confirm(self):
        safe_click(self.save_button)
        try:
            btn = self.page.get_by_role("button", name=BTN_TEXT_YES)
            safe_click(btn)
        except:
            pass

    def close_dialog(self):
        safe_click(self.dialog_close_button)

    def get_reference_sidepanel_text(self):
        self.page.wait_for_timeout(500)
        self.panel_rows.first.wait_for(state="visible", timeout=3000)

        result = []
        for i in range(self.panel_rows.count()):
            try:
                code = self.panel_rows.nth(i).locator("td").nth(0).locator("span").inner_text(timeout=1000).strip()
                name = self.panel_rows.nth(i).locator("td").nth(1).locator("span").inner_text(timeout=1000).strip()
                if code or name:
                    result.append(f"{code}{TAB}{name}")
            except:
                continue
        return NEWLINE.join(result)