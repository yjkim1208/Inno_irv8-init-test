from pages.components.iframe_dialog import IframeDialog
from utils.ui_helpers import safe_click
from utils.ui_selectors import (
    BTN_MENU_TYPE_MGMT_NAME, 
    BTN_MANAGEMENT_TYPE_NAME, 
    ROW_TEXT_FOR_ADD
)

class ManagementTypeSection:
    def __init__(self, page):
        self.page = page
        self.iframe = page.frame_locator("iframe").nth(1)
        self.dialog = IframeDialog(page)

    def click_button(self, selector: str):
        button = self.iframe.locator(selector)
        safe_click(button)

    def paste_to_add_row(self, content: str):
        from utils.ui_helpers import paste_to_cell
        row = self.iframe.locator("tr").filter(has_text=ROW_TEXT_FOR_ADD).first
        paste_to_cell(self.page, content, row)

    def get_grid_span(self, grid_selector: str, text: str):
        grid = self.iframe.locator(grid_selector)
        return grid.locator("span").filter(has_text=text).first

    def go_to_management_page(self):
        main_frame = self.page.frame_locator("iframe")
        safe_click(main_frame.get_by_role("list").get_by_role("button", name=BTN_MENU_TYPE_MGMT_NAME))
        safe_click(main_frame.get_by_role("button", name=BTN_MANAGEMENT_TYPE_NAME))