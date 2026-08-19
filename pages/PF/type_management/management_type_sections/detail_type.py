from .management_type_section import ManagementTypeSection
from utils.ui_selectors import (
    DETAIL_TYPE_ADD_BTN,
    DETAIL_TYPE_SAVE_BTN,
    DETAIL_TYPE_DELETE_BTN,
    DETAIL_TYPE_GRID_ID,
    DETAIL_TYPE_GRID_XPATH,
    DETAIL_TYPE_NAME_CELL_SELECTOR,
)
from playwright.sync_api import Page
from utils.ui_helpers import safe_click


class DetailType(ManagementTypeSection):
    def __init__(self, page: Page):
        super().__init__(page)
        self.grid = self.iframe.locator(DETAIL_TYPE_GRID_XPATH)
        self.grid_area = self.iframe.locator(DETAIL_TYPE_GRID_ID)
        self.get_name_cells = lambda: self.grid.locator(DETAIL_TYPE_NAME_CELL_SELECTOR).all()

    def click_add(self):
        self.click_button(DETAIL_TYPE_ADD_BTN)

    def input(self, content: str):
        self.paste_to_add_row(content)

    def save(self):
        self.click_button(DETAIL_TYPE_SAVE_BTN)

    def delete_all(self):
        for cell in self.get_name_cells():
            if cell.is_visible():
                safe_click(cell)
                self.page.wait_for_timeout(200)
                self.click_button(DETAIL_TYPE_DELETE_BTN)
                self.page.wait_for_timeout(200)

        self.page.wait_for_timeout(200)
        self.save()
        self.dialog.get_message(timeout=5000)

    def has(self, expected_names: list[str]) -> bool:
        self.page.wait_for_timeout(500)
        for name in expected_names:
            el = self.grid_area.locator("span").filter(has_text=name).first
            try:
                el.wait_for(state="visible", timeout=3000)
            except:
                return False
        return True

    def extract_names(self, content: str) -> list[str]:
        lines = content.strip().split("\\n")
        return [line.split("\\t")[1] for line in lines if "\\t" in line]
