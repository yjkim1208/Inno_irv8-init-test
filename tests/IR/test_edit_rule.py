import pytest
from conftest import REPEAT_COUNT
from pages.IR.main_page.rule_tree.edit_rule import EditRulePage
from pages.IR.main_page.folder_tree.top_folder import TopFolderPage
from pages.IR.main_page.folder_tree.folder import FolderPage
from pages.IR.main_page.rule_tree.make_rule import MakeRulePage
from test_login import initialize_test

class TestEditRule:

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_32_edit_rule_with_duplicate_name(self, page):
        """TC-32: 이미 존재하는 룰 이름으로 변경 시도 (오류)"""
        db, make_rule_page = get_edit_rule_page(page, 32)

        make_rule_page.create_rule(db["folder_name"], db["rule_name"], db["return_content"], db["rule_template"])
        make_rule_page.create_rule(db["folder_name"], db["change_content"], db["return_content"], db["rule_template"])

        edit = EditRulePage(page)
        edit.open_edit_rule_popup(db["folder_name"], db["change_content"])
        page.wait_for_timeout(500)
        edit.change_rule_name(db["rule_name"])
        edit.click_confirm()

        assert db["expected_result"] in edit.get_alert_message()
        edit.close_error_dialog()
        edit.close_rule_dialog()
        FolderPage(page).delete_folder_with_rules(db['top_folder_name'])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_33_edit_rule_successfully(self, page):
        """TC-33: 룰 정보 정상 변경"""
        db, make_rule_page = get_edit_rule_page(page, 33)

        make_rule_page.create_rule(db["folder_name"], db["rule_name"]+" 변경 A 0", db["return_content"], db["rule_template"])
        # make_rule_page.create_rule(db["folder_name"], db["rule_name"]+" 변경 B 0", db["return_content"], db["rule_template"])

        edit = EditRulePage(page)
        for i in range(0,1000):
            edit.open_edit_rule_popup(db["folder_name"], db["change_content"] + " A "+str(i))
            page.wait_for_timeout(500)
            edit.change_rule_name(db["change_content"]+ " A "+str(i+1))
            page.wait_for_timeout(500)
            edit.click_confirm()
            page.wait_for_timeout(500)

            # edit.open_edit_rule_popup(db["folder_name"], db["change_content"] + " B "+str(i))
            # page.wait_for_timeout(500)
            # edit.change_rule_name(db["change_content"]+ " B "+str(i+1))
            # page.wait_for_timeout(500)
            # edit.click_confirm()
            # page.wait_for_timeout(500)

        assert edit.is_rule_in_tree(db["expected_result"])
        FolderPage(page).delete_folder_with_rules(db['top_folder_name'])



def get_edit_rule_page(page, test_id):
    _, db = initialize_test(page, test_id)
    TopFolderPage(page).create_top_folder(db["top_folder_name"])
    FolderPage(page).create_folder(db["top_folder_name"], db["folder_name"])
    return db, MakeRulePage(page)