import pytest
from conftest import REPEAT_COUNT
from pages.IR.main_page.folder_tree.top_folder import TopFolderPage
from test_login import initialize_test

class TestTopFolder:

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_007_add_without_name(self, page):
        """TC-007: 폴더명 없이 추가 → 오류 메시지 확인"""
        top_folder, db = setup_top_folder_test(page, 7)

        top_folder.open_add_folder_popup()
        top_folder.click_add_button()  # 이름 없이 추가

        top_folder.assert_error_message(db["expected_result"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_008_add_valid_folder(self, page):
        """TC-008: 정상적인 폴더명 입력 → 추가 성공 여부 확인"""
        top_folder, db = setup_top_folder_test(page, 8)

        top_folder.create_top_folder(db["top_folder_name"])
        top_folder.assert_folder_is_present(db["expected_result"])
        top_folder.delete_folder(db["top_folder_name"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_009_add_duplicate_folder(self, page):
        """TC-009: 동일한 폴더명 두 번 입력 → 오류 메시지 확인"""
        top_folder, db = setup_top_folder_test(page, 9)

        top_folder.create_top_folder(db["top_folder_name"])
        top_folder.create_top_folder(db["top_folder_name"])

        top_folder.assert_error_message(db["expected_result"])
        top_folder.close_duplicate_folder_dialog()
        top_folder.delete_folder(db["top_folder_name"])


def setup_top_folder_test(page, test_id):
    _, db = initialize_test(page, test_id)
    top_folder = TopFolderPage(page)
    return top_folder, db