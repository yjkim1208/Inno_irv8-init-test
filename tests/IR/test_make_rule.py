from conftest import REPEAT_COUNT
from pages.IR.main_page.rule_tree.make_rule import MakeRulePage
from pages.IR.main_page.folder_tree.top_folder import TopFolderPage
from pages.IR.main_page.folder_tree.folder import FolderPage
from test_login import initialize_test
import pytest

class TestMakeRule:

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_27_add_rule_without_name(self, page):
        """TC-27: 룰 이름 입력 없이 룰 추가 (오류)"""
        db, make_rule_page = get_rule_page(page, 27)
        make_rule_page.open_add_rule_popup(db['folder_name'])
        assert make_rule_page.is_confirm_button_disabled()
        make_rule_page.close_rule_add_popup()
        FolderPage(page).delete_folder(db['top_folder_name'])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_28_add_rule_without_return_item(self, page):
        """TC-28: 리턴 항목 입력 없이 룰 추가 (오류)"""
        db, make_rule_page = get_rule_page(page, 28)
        make_rule_page.open_add_rule_popup(db['folder_name'])
        make_rule_page.select_rule_template(db["rule_template"])
        make_rule_page.input_rule_name(db["rule_name"])
        make_rule_page.click_confirm()
        assert db["expected_result"] in make_rule_page.get_alert_message()
        make_rule_page.close_error_dialog()
        make_rule_page.close_rule_add_popup()
        FolderPage(page).delete_folder(db['top_folder_name'])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_29_add_rule_after_delete_all_return_items(self, page):
        """TC-29: 리턴 항목 모두 삭제 후 룰 추가 (오류)"""
        db, make_rule_page = get_rule_page(page, 29)
        make_rule_page.open_add_rule_popup(db['folder_name'])
        make_rule_page.select_rule_template(db["rule_template"])
        make_rule_page.input_rule_name(db["rule_name"])
        make_rule_page.input_return_item(db["return_content"])
        make_rule_page.check_all_delete_checkboxes()
        make_rule_page.click_confirm()
        assert db["expected_result"] in make_rule_page.get_alert_message()
        make_rule_page.close_error_dialog()
        make_rule_page.close_rule_add_popup()
        FolderPage(page).delete_folder(db['top_folder_name'])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_30_add_valid_rule(self, page):
        """TC-30: 정상적인 룰 추가"""
        db, make_rule_page = get_rule_page(page, 30)
        make_rule_page.create_rule(db['folder_name'], db["rule_name"], db["return_content"], db["rule_template"])
        assert make_rule_page.is_rule_in_tree(db["expected_result"])
        TopFolderPage(page).delete_folder_with_rules(db['top_folder_name'])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_31_add_duplicate_rule(self, page):
        """TC-31: 중복된 룰 이름으로 룰 추가 (오류)"""
        db, make_rule_page = get_rule_page(page, 31)
        make_rule_page.create_rule(db['folder_name'],db["rule_name"], db["return_content"], db["rule_template"])
        make_rule_page.create_rule(db['folder_name'],db["rule_name"], db["return_content"], db["rule_template"])
        assert db["expected_result"] in make_rule_page.get_alert_message()
        make_rule_page.close_error_dialog()
        make_rule_page.close_rule_add_popup()
        TopFolderPage(page).delete_folder_with_rules(db['top_folder_name'])


def get_rule_page(page, test_id):
    _, db = initialize_test(page, test_id)
    TopFolderPage(page).create_top_folder(db["top_folder_name"])
    FolderPage(page).create_folder(db["top_folder_name"], db["folder_name"])
    return db, MakeRulePage(page)
