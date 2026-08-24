from pages.IR.main_page.folder_tree.base_folder_page import BaseFolderPage
from utils.ui_selectors import *
from utils.ui_helpers import safe_click


class FolderPage(BaseFolderPage):
    def __init__(self, page):
        super().__init__(page)

        # 폴더 관련 요소
        self.folder_list_area = page.locator(FOLDER_LIST_AREA)
        self.add_folder_button = page.locator(POPOVER_CONTAINER).get_by_role("button",name=FOLDER_ADD_BTN_NAME)
        self.rename_button = page.get_by_role("button",name=FOLDER_RENAME_BTN_NAME)
        self.rename_input = page.locator(FOLDER_RENAME_INPUT)
        self.rename_save_button = page.locator(FOLDER_RENAME_SAVE_BTN)
        self.cancel_delete_button = page.get_by_role("button",name=BTN_TEXT_NO,exact=True)
        self.duplicate_name_confirm_button = page.locator(BASE_FOLDER_DUPLICATE_DIALOG_CONFIRM_BTN)
        self.duplicate_name_popup_close = page.locator(FOLDER_NAME_DUPLICATE_POPUP_CLOSE)

    def open_add_folder_popup(self,top_folder_name: str):
        self.folder_list_area.get_by_text(top_folder_name,exact=True).click(button="right")
        safe_click(self.add_folder_button)
    def create_folder(self,top_folder: str,name: str):
        self.open_add_folder_popup(top_folder)
        self.add_folder_name(name)
        self.click_add_button()
        self.click_save_button()

        # 폴더가 실제로 생성될 때까지 대기
        self.get_treeitem(name).wait_for(state="visible",timeout=5000)

    def rename_folder(self,name: str,change_name: str):
        self.folder_list_area.get_by_text(name,exact=True).click(button="right")
        safe_click(self.rename_button)
        self.rename_input.fill(change_name)
        safe_click(self.rename_save_button)

    def cancel_delete_folder(self,name: str):
        """폴더 삭제를 시도한 뒤 삭제 확인 팝업에서 취소한다."""

        self._initiate_folder_action(name,BASE_FOLDER_DELETE_BTN_NAME)
        delete_dialog = self.page.locator("#ir_message .ir-confirm.dialog.is-visible").last
        delete_dialog.wait_for(state="visible",timeout=5000)
        cancel_button = delete_dialog.get_by_role("button",name=BTN_TEXT_NO,exact=True)
        safe_click(cancel_button)

        # 삭제 확인 팝업이 완전히 닫힌 후 다음 단계 수행
        delete_dialog.wait_for(state="hidden",timeout=5000)

    def close_duplicate_folder_name_dialog(self):
        """폴더 이름 중복 오류와 이름 변경 팝업을 닫는다."""
        safe_click(self.duplicate_name_confirm_button)
        safe_click(self.duplicate_name_popup_close)

    def close_rename_error_dialog(self):
        """이름 변경 오류 메시지와 폴더 이름 변경 팝업을 닫는다."""
        error_dialog = self.page.locator("#ir_message .ir-confirm.dialog.is-visible").last
        error_dialog.wait_for(state="visible",timeout=5000)
        confirm_button = error_dialog.get_by_role("button",name=BTN_TEXT_CONFIRM,exact=True)

        # 오류 메시지 확인
        safe_click(confirm_button)

        # 오류 메시지가 사라질 때까지 대기
        error_dialog.wait_for(state="hidden",timeout=5000)

        # rename_input을 포함하는 실제 외부 dialog 선택
        rename_dialog = self.rename_input.locator(
            "xpath=ancestor::div["
            "contains("
            "concat(' ', normalize-space(@class), ' '), "
            "' dialog '"
            ")"
            "][1]"
        )
        rename_dialog.wait_for(state="visible",timeout=5000)
        # 현재 이름 변경 팝업 내부의 닫기 버튼만 선택
        popup_close_button = rename_dialog.locator(FOLDER_NAME_DUPLICATE_POPUP_CLOSE)
        popup_close_button.wait_for(state="attached",timeout=5000)
            # 화면 좌표가 아닌 DOM 이벤트로 닫기 버튼 클릭
        popup_close_button.evaluate("element => element.click()")
            # 이름 변경 팝업이 완전히 닫힐 때까지 대기
        rename_dialog.wait_for(state="hidden",timeout=5000)

    def close_add_folder_error_dialog(self):
        """폴더 추가 오류 메시지와 폴더 추가 팝업을 닫는다."""
        error_dialog = self.page.locator("#ir_message .ir-confirm.dialog.is-visible").last
        error_dialog.wait_for(state="visible",timeout=5000)
        confirm_button = error_dialog.get_by_role("button",name=BTN_TEXT_CONFIRM,exact=True)
        # 오류 메시지 확인
        safe_click(confirm_button)
        # 오류 메시지가 사라질 때까지 대기
        error_dialog.wait_for(state="hidden",timeout=5000)
        # 폴더 추가 팝업
        add_dialog = self.page.locator("#div_add_biz_pop.dialog.is-visible")
        add_dialog.wait_for(state="visible",timeout=5000)
        close_button = add_dialog.locator(".dialog__button-close")
        close_button.wait_for(state="attached",timeout=5000)
        # 화면 좌표 문제를 피하기 위해 DOM 클릭
        close_button.evaluate("element => element.click()")
        # 폴더 추가 팝업이 사라질 때까지 대기
        add_dialog.wait_for(state="hidden",timeout=5000)