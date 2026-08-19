from pages.components.iframe_dialog import IframeDialog
from .management_type_section import ManagementTypeSection
from utils.ui_helpers import paste_to_cell
from utils.ui_selectors import (
    OBJECT_TYPE_ADD_BTN,
    OBJECT_TYPE_SAVE_BTN,
    OBJECT_TYPE_DELETE_BTN,
    OBJECT_TYPE_CODE_RULE_SAVE_BTN,
    OBJECT_TYPE_GRID_SELECTOR,
    OBJECT_TYPE_CODE_RULE_DIALOG,
    OBJECT_TYPE_CODE_RULE_CELL,
)
from playwright.sync_api import Page
from utils.ui_helpers import safe_click


class ObjectType(ManagementTypeSection):
    def __init__(self, page: Page):
        super().__init__(page)
        self.grid_area = self.iframe.locator(OBJECT_TYPE_GRID_SELECTOR)
        self.popup = self.iframe.locator(OBJECT_TYPE_CODE_RULE_DIALOG)
        

    def create(self, content: str):
        self.click_button(OBJECT_TYPE_ADD_BTN)
        self.paste_to_add_row(content)
        self.click_button(OBJECT_TYPE_SAVE_BTN)

    def delete(self, names: str | list[str]):
        names = [names] if isinstance(names, str) else names
        for name in names:
            span = self.get_grid_span(OBJECT_TYPE_GRID_SELECTOR, name)
            safe_click(span)
            self.page.wait_for_timeout(200)
            self.click_button(OBJECT_TYPE_DELETE_BTN)
            self.page.wait_for_timeout(200)
        self.page.wait_for_timeout(200)
        self.click_button(OBJECT_TYPE_SAVE_BTN)
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
        return [line.split("\\t")[1].strip() for line in lines if "\\t" in line]

    def click_code_rule_button(self, name: str):
        span = self.grid_area.locator("span").filter(has_text=name).first
        span.wait_for(state="visible")
        td = span.locator("xpath=ancestor::td")
        data_row = td.get_attribute("data-row")
        if not data_row:
            raise ValueError(f"data-row not found for span: {name}")
        safe_click(self.iframe.locator(f'td[data-row="{data_row}"][data-col="9"] button'))

    def input_code_rule(self, value: str):
        cell = self.popup.locator(OBJECT_TYPE_CODE_RULE_CELL).first
        paste_to_cell(self.page, value, cell)

    def save_code_rule(self):
        self.click_button(OBJECT_TYPE_CODE_RULE_SAVE_BTN)

    def click_name(self, name: str):
        safe_click(self.get_grid_span(OBJECT_TYPE_GRID_SELECTOR, name))
