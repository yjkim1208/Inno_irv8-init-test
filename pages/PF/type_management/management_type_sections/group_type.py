from .management_type_section import ManagementTypeSection
from utils.ui_selectors import (
    GROUP_TYPE_ADD_BTN,
    GROUP_TYPE_SAVE_BTN,
    GROUP_TYPE_DELETE_BTN,
    GROUP_TYPE_GRID_XPATH,
    GROUP_TYPE_NAME_CELL_SELECTOR,
    GROUP_TYPE_GRID_AREA,
    GROUP_GRID_SELECTOR,
)
from playwright.sync_api import Page
from utils.ui_helpers import safe_click

class GroupType(ManagementTypeSection):
    def __init__(self, page: Page):
        super().__init__(page)
        self.grid = self.iframe.locator(GROUP_TYPE_GRID_XPATH)
        self.grid_area = self.iframe.locator(GROUP_TYPE_GRID_AREA)
        self.get_name_cells = lambda: self.grid.locator(GROUP_TYPE_NAME_CELL_SELECTOR).all()

    def click_add(self):
        self.click_button(GROUP_TYPE_ADD_BTN)

    def input(self, content: str):
        self.paste_to_add_row(content)

    def save(self):
        self.click_button(GROUP_TYPE_SAVE_BTN)

    def extract_names(self, content: str) -> list[str]:
        lines = content.strip().split("\\n")
        return [line.split("\\t")[0].strip() for line in lines if "\\t" in line]

    def has(self, expected_names: list[str]) -> bool:
        self.page.wait_for_timeout(500)
        for name in expected_names:
            el = self.grid_area.locator("span").filter(has_text=name).first
            try:
                el.wait_for(state="visible", timeout=3000)
            except:
                return False
        return True

    def delete_all(self):
        for cell in self.get_name_cells():
            if cell.is_visible():
                safe_click(cell)
                self.page.wait_for_timeout(200)
                self.click_button(GROUP_TYPE_DELETE_BTN)
                self.page.wait_for_timeout(200)

        self.page.wait_for_timeout(200)
        self.save()
        self.dialog.get_message(timeout=5000)

    def click_group(self, name: str):
        safe_click(self.get_grid_span(GROUP_GRID_SELECTOR, name))
