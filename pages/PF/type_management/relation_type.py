from pages.components.iframe_dialog import IframeDialog
from utils.ui_selectors import (
    BTN_MENU_TYPE_MGMT_NAME,
    BTN_RELATION_TYPE_PAGE_NAME,
    BTN_ADD_ROW_NAME,
    BTN_RELATION_SAVE_NAME,
    BTN_TEXT_CONFIRM,
    GRID_RELATION_TABLE_XPATH,
    RELATION_DELETE_BTN_SELECTOR,
    ROW_TEXT_FOR_ADD,
)
from playwright.sync_api import Page
from utils.ui_helpers import paste_to_cell
import re
from utils.ui_helpers import safe_click


class RelationTypePage:
    def __init__(self, page: Page):
        self.page = page
        self.iframe = page.frame_locator("iframe").nth(1)
        self.main_frame = page.frame_locator("iframe")
        self.dialog = IframeDialog(page) 

        # 메뉴 이동 관련 버튼
        self.menu_type_mgmt_btn = self.main_frame.get_by_role("list").get_by_role("button", name=BTN_MENU_TYPE_MGMT_NAME)
        self.relation_type_page_btn = self.main_frame.get_by_role("button", name=BTN_RELATION_TYPE_PAGE_NAME, exact=True)

        # 관계유형 등록 관련 버튼
        self.add_row_btn = self.iframe.get_by_role("button", name=BTN_ADD_ROW_NAME)
        self.save_btn = self.iframe.get_by_role("button", name=BTN_RELATION_SAVE_NAME)
        self.confirm_btn = self.iframe.get_by_role("button", name=BTN_TEXT_CONFIRM)
        self.delete_btn = self.iframe.locator(RELATION_DELETE_BTN_SELECTOR)

        # 테이블
        self.grid_table = self.iframe.locator(GRID_RELATION_TABLE_XPATH)

    def go_to_relation_type_page(self):
        safe_click(self.menu_type_mgmt_btn)
        safe_click(self.relation_type_page_btn)

    def click_add_relation_row(self):
        safe_click(self.add_row_btn)


    def input_relation_info(self, relation_content: str):
        row = self.iframe.locator("tr").filter(has_text=ROW_TEXT_FOR_ADD).first
        paste_to_cell(self.page, relation_content, row)

    def save_relation(self):
        safe_click(self.save_btn)


    def get_success_message_from_dialog(self, timeout=5000) -> str:
        return self.dialog.get_message(timeout=timeout)

    def click_success_dialog_confirm(self):
        self.dialog.confirm()

    def has_relation_type(self, expected_text: str) -> bool:
        object_names = re.findall(r'\[(.*?)\]\[(.*?)\]\[(.*?)\]', expected_text)
        names_to_check = [match[2] for match in object_names]

        for name in names_to_check:
            element = self.grid_table.locator("span").filter(has_text=name).first
            if not element.is_visible():
                return False
        return True

    def delete_relation_types(self, relation_content: str):
        object_names = re.findall(r'\[(.*?)\]\[(.*?)\]\[(.*?)\]', relation_content)
        if not object_names:
            raise ValueError("relation_content에서 오브젝트명을 추출하지 못했습니다.")

        target_name = object_names[0][2]
        span = self.grid_table.locator("span", has_text=target_name).first
        span.wait_for(state="visible", timeout=5000)
        target_cell = span.locator("xpath=ancestor::td[1]")
        safe_click(target_cell)

        self.delete_btn.wait_for(state="attached", timeout=3000)
        safe_click(self.delete_btn)
        
        safe_click(self.save_btn)

        self.dialog.get_message(timeout=5000)

    def add_relation_type(self, content: str):
        self.click_add_relation_row()
        self.input_relation_info(content)
        self.save_relation()

    def assert_success_and_confirm(self, expected: str):
        assert self.get_success_message_from_dialog() == expected
        self.click_success_dialog_confirm()

    def assert_has_relation_type(self, expected: str):
        assert self.has_relation_type(expected)

    def cleanup_relation_type(self, content: str):
        self.delete_relation_types(content)

    def click_A(self):
        frame = self.page.frame_locator("iframe").nth(1)

        expand_btn = frame.locator("#btn-expand")
        expand_btn.click()

        frame.locator('xpath=//*[@id="right"]/div/div[3]/div[1]/button[1]').click()

        source = frame.locator('xpath=//*[@id="left"]/div[2]/div/div/ul/li[7]/ul/li/div/div')
        target = frame.locator('xpath=//*[@id="right"]/div/div[2]/div/div[1]/div/table/div[2]/tr[3]/td[1]')

        # 가시성 보장
        source.wait_for(state="visible")
        target.wait_for(state="visible")

        # 필요 시 스크롤
        source.scroll_into_view_if_needed()
        target.scroll_into_view_if_needed()

        # drag_to 사용 (dataTransfer 포함)
        source.drag_to(
            target,
            source_position={"x": 5, "y": 5},     # 드래그 핸들이 좌측 상단 등 특정 위치일 때 도움이 됨
            target_position={"x": 10, "y": 10},
            force=True,                            # 약간의 오버레이가 있어도 밀어붙임
            timeout=5000
        )


