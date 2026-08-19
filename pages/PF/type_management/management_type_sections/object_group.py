from .management_type_section import ManagementTypeSection
from utils.ui_selectors import (
    OBJECT_GROUP_ADD_BTN,
    OBJECT_GROUP_SAVE_BTN,
    OBJECT_GROUP_DELETE_BTN,
    OBJECT_GROUP_GRID_SELECTOR,
)
from playwright.sync_api import Page
from utils.ui_helpers import safe_click


class ObjectGroup(ManagementTypeSection):
    def __init__(self, page: Page):
        super().__init__(page)
        self.grid_area = self.iframe.locator(OBJECT_GROUP_GRID_SELECTOR)

    def click_add(self):
        self.click_button(OBJECT_GROUP_ADD_BTN)

    def input(self, content: str):
        self.paste_to_add_row(content)

    def save(self):
        self.click_button(OBJECT_GROUP_SAVE_BTN)

    def delete(self, names: str | list[str]):
        names = [names] if isinstance(names, str) else names
        for name in names:
            span = self.get_grid_span(OBJECT_GROUP_GRID_SELECTOR, name)
            safe_click(span)
            self.page.wait_for_timeout(200)
            self.click_button(OBJECT_GROUP_DELETE_BTN)
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
