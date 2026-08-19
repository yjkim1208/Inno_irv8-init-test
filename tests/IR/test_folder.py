import pytest
from conftest import REPEAT_COUNT
from pages.IR.main_page.folder_tree.folder import FolderPage
from pages.IR.main_page.folder_tree.top_folder import TopFolderPage
from test_login import initialize_test

class TestFolder:

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_10_add_folder_without_name(self, page):
        """TC-010: 폴더 이름 없이 폴더 추가"""
        folder, db = setup_folder_test(page, 10)

        folder.open_add_folder_popup(db['top_folder_name'])
        folder.click_add_button()
        folder.assert_error_message(db["expected_result"])

        folder.close_duplicate_folder_dialog()
        folder.delete_folder(db["top_folder_name"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_11_add_valid_folder(self, page):
        """TC-011: 정상적인 폴더 이름으로 추가"""
        folder, db = setup_folder_test(page, 11)

        folder.create_folder(db["top_folder_name"], db['folder_name'])
        folder.assert_folder_is_present(db['expected_result'])

        folder.delete_folder(db["top_folder_name"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_12_add_duplicate_folder(self, page):
        """TC-012: 중복된 폴더 이름으로 추가"""
        folder, db = setup_folder_test(page, 12)

        folder.create_folder(db["top_folder_name"], db['folder_name'])
        folder.create_folder(db["top_folder_name"], db['folder_name'])

        folder.assert_error_message(db["expected_result"])

        folder.close_duplicate_folder_dialog()
        folder.delete_folder(db["top_folder_name"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_13_rename_folder(self, page):
        """TC-013: 폴더 이름 변경 (정상)"""
        folder, db = setup_folder_test(page, 13)

        folder.create_folder(db["top_folder_name"], db['folder_name'])
        folder.rename_folder(db["folder_name"], db["change_content"])

        folder.assert_folder_is_present(db['expected_result'])

        folder.delete_folder(db["top_folder_name"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_14_rename_folder_blank(self, page):
        """TC-014: 폴더 이름을 공백으로 변경"""
        folder, db = setup_folder_test(page, 14)

        folder.create_folder(db["top_folder_name"], db['folder_name'])
        folder.rename_folder(db["folder_name"], "")

        folder.assert_error_message(db["expected_result"])

        folder.close_duplicate_folder_name_dialog()
        folder.delete_folder(db["top_folder_name"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_15_rename_folder_duplicate(self, page):
        """TC-015: 폴더 이름을 중복으로 변경"""
        folder, db = setup_folder_test(page, 15)

        folder.create_folder(db["top_folder_name"], db['folder_name'])
        folder.create_folder(db["top_folder_name"], db["change_content"])
        folder.rename_folder(db["folder_name"], db["change_content"])

        folder.assert_error_message(db["expected_result"])

        folder.close_duplicate_folder_name_dialog()
        folder.delete_folder(db["top_folder_name"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_16_rename_folder_same_name(self, page):
        """TC-016: 동일한 이름으로 변경"""
        folder, db = setup_folder_test(page, 16)

        folder.create_folder(db["top_folder_name"], db['folder_name'])
        folder.rename_folder(db["folder_name"], db["folder_name"])

        folder.assert_folder_is_present(db['expected_result'])
        folder.delete_folder(db["top_folder_name"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_17_cancel_delete_folder(self, page):
        """TC-017: 폴더 삭제 취소"""
        folder, db = setup_folder_test(page, 17)

        folder.create_folder(db["top_folder_name"], db['folder_name'])
        folder.cancel_delete_folder(db["folder_name"])

        folder.assert_folder_is_present(db['expected_result'])

        folder.delete_folder(db["top_folder_name"])

def setup_folder_test(page, test_id):
    _, db = initialize_test(page, test_id)
    TopFolderPage(page).create_top_folder(db["top_folder_name"])
    folder = FolderPage(page)
    return folder, db