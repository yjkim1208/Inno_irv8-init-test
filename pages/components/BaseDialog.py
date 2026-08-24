from utils.ui_selectors import DIALOG_CONFIRM_BTN_SELECTOR, DIALOG_MESSAGE_SELECTOR
from utils.ui_helpers import safe_click

class BaseDialog:
    def __init__(self, frame):
        self.frame = frame

    def get_visible_dialog(self):
        """
        폴더 삭제 확인 등 현재 화면에 표시된
        일반 다이얼로그를 반환한다.
        """
        return self.frame.locator(
            "div.dialog.is-visible"
        ).last

    def get_visible_message_dialog(self):
        """
        #ir_message 영역에 표시된
        오류·안내 메시지 다이얼로그를 반환한다.
        """
        return self.frame.locator(
            "#ir_message .ir-confirm.dialog.is-visible"
        ).last

    def get_message(self, timeout: int = 5000) -> str:
        """
        오류·안내 메시지 팝업의 텍스트를 반환한다.
        """
        dialog = self.get_visible_message_dialog()

        dialog.wait_for(
            state="visible",
            timeout=timeout
        )

        return dialog.inner_text().strip()

    def confirm(self, timeout: int = 5000):
        """
        폴더 삭제 등 현재 표시된 일반 다이얼로그의
        확인 버튼을 클릭한다.
        """
        dialog = self.get_visible_dialog()

        dialog.wait_for(
            state="visible",
            timeout=timeout
        )

        confirm_button = dialog.get_by_role(
            "button",
            name="확인",
            exact=True
        )

        safe_click(
            confirm_button,
            timeout
        )