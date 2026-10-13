# tests/test_table_rule.py
import pytest
from conftest import REPEAT_COUNT
from pages.IR.main_page.rule_tree.make_rule import MakeRulePage
from pages.IR.main_page.folder_tree.top_folder import TopFolderPage
from pages.IR.main_page.folder_tree.folder import FolderPage
from pages.IR.rule_page.contetnt_page.table_rule import TableRulePage
from pages.IR.rule_page.test_page.rule_test import RuleTestPage
from pages.IR.main_page.side_bar.item.item import ItemPage
from pages.IR.main_page.side_bar.Rule_Search.rule_search import RuleSearchPage
from test_login import initialize_test
from utils.ui_helpers import wait_for_cell_in_iframe


class TestTableRule:

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_34_single_value_returns_result(self, page):
        """TC-34: 단일값을 리턴하는 테이블 룰 저장 - 만족하는 조건"""
        db, _ = setup_rule_with_item(page, 34)

        TableRulePage(page).fill_rule_content_and_save(db['rule_content'])
        run_test_and_verify(page, db)
        clean_up(page, db)

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_35_single_value_error_multiple(self, page):
        db, _ = setup_rule_with_item(page, 35)

        TableRulePage(page).fill_rule_content_and_save(db['rule_content'])
        test_page = RuleTestPage(page)
        test_page.open_test_tab(db["folder_name"], db["rule_name"])
        test_page.input_test_data(db["test_data"])
        test_page.click_test_run()

        assert db["expected_result"] in test_page.get_error_message_from_dialog()
        test_page.close_error_dialog()
        clean_up(page, db)

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_36_single_value_rule_error_on_multiple_matching_conditions(self, page):
        """TC-36: 조건이 2개 이상 매칭될 경우 오류"""
        db, _ = setup_rule_with_item(page, 36)
        table_rule_page = TableRulePage(page)

        table_rule_page.fill_rule_content_and_click_save(db['rule_content'])
        assert "룰 표현식에 문법오류가 존재합니다." in table_rule_page.get_error_message_from_dialog()

        RuleTestPage(page).click_error_popup_ok_button()
        assert db["expected_result"] in table_rule_page.get_error_message_from_grid()
        clean_up(page, db)

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_37_single_value_rule_error_invalid_condition_type(self, page):
        """TC-37: 조건 데이터 타입 불일치"""
        db, _ = setup_rule_with_item(page, 37)
        table_rule_page = TableRulePage(page)

        table_rule_page.fill_rule_content_and_click_save(db['rule_content'])
        assert "룰 표현식에 문법오류가 존재합니다." in table_rule_page.get_error_message_from_dialog()

        RuleTestPage(page).click_error_popup_ok_button()
        assert db["expected_result"] in table_rule_page.get_error_message_from_grid()
        clean_up(page, db)

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_38_multiple_value_rule_with_all_condition_match(self, page):
        """TC-38: 다중값 리턴 - 모든 만족조건 체크"""
        db, _ = setup_multi_rule_with_item(page, 38)
        table_rule_page = TableRulePage(page)

        table_rule_page.check_all_condition_checkbox()
        table_rule_page.fill_rule_content_and_save(db['rule_content'])
        run_test_and_verify(page, db)
        clean_up(page, db)

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_39_multiple_value_rule_without_all_condition_match(self, page):
        """TC-39: 다중값 리턴 - 모든 만족조건 미체크"""
        db, _ = setup_multi_rule_with_item(page, 39)

        TableRulePage(page).fill_rule_content_and_save(db['rule_content'])
        run_test_and_verify(page, db)
        clean_up(page, db)

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_40_multiple_value_rule_error_without_all_condition_and_empty_condition_row(self, page):
        """TC-40: 조건 미지정 오류"""
        db, _ = setup_multi_rule_with_item(page, 40)
        table_rule_page = TableRulePage(page)

        table_rule_page.fill_rule_content_and_click_save(db['rule_content'])
        assert "룰 표현식에 문법오류가 존재합니다." in table_rule_page.get_error_message_from_dialog()

        RuleTestPage(page).click_error_popup_ok_button()
        assert db["expected_result"] in table_rule_page.get_error_message_from_grid()
        clean_up(page, db)

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_41_return_type_mismatch_single_value_rule(self, page):
        """TC-41: 리턴 타입 불일치 - 값 입력"""
        db, _ = setup_rule_with_item(page, 41)
        table_rule_page = TableRulePage(page)

        table_rule_page.fill_rule_content_and_click_save(db['rule_content'])
        assert "룰 표현식에 문법오류가 존재합니다." in table_rule_page.get_error_message_from_dialog()

        RuleTestPage(page).click_error_popup_ok_button()
        assert db["expected_result"] in table_rule_page.get_error_message_from_grid()
        clean_up(page, db)

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_42_delete_table_rule(self, page):
        """TC-42: 테이블 룰 삭제"""
        db, _ = setup_rule_with_item(page, 42)
        search_page = RuleSearchPage(page)

        search_page.open_rule_search_tab()
        search_page.search_rule(db["rule_name"])
        assert search_page.is_rule_found(db["rule_name"])
        search_page.close_search_dialog()

        clean_up(page, db)

        search_page.open_rule_search_tab()
        search_page.search_rule(db["rule_name"])
        assert search_page.get_popup_message_text() == db['expected_result']

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_44_single_value_table_rule_calls_single_value_rule(self, page):
        """TC-44: 단일값 테이블 룰 내 단일값 룰 호출"""
        run_nested_rule_test(page, 44)

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_46_multi_value_table_rule_calls_single_value_rule(self, page):
        """TC-46: 다중값 테이블 룰 내 단일값 룰 호출"""
        run_nested_rule_test(page, 46, multi=True)

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_47_string_condition_calls_string_rule(self, page):
        """TC-47: 문자형 전체 리턴 항목 룰 호출"""
        run_nested_rule_test(page, 47, multi=True)

def run_test_and_verify(page, db):
    test_page = RuleTestPage(page)
    test_page.open_test_tab(db["folder_name"], db["rule_name"])
    test_page.input_test_data(db["test_data"])
    test_page.click_test_run()
    assert test_page.verify_test_result(db['expected_result'])

def clean_up(page, db):
    FolderPage(page).delete_folder_with_rules(db['top_folder_name'])
    item_tab = ItemPage(page)
    popup = item_tab.open_item_manage_page()
    ItemPage(popup).delete_items(db['item_content'])
    popup.close()

def run_nested_rule_test(page, test_id, multi=False):
    setup_fn = setup_multi_rule_with_item if multi else setup_rule_with_item
    db, _ = setup_fn(page, test_id)

    TableRulePage(page).close_rule_tab()
    TableRulePage(page).yes_button()

    MakeRulePage(page).create_rule(
        folder_name=db["folder_name"],
        name=db["temp_rule_name"],
        return_value=db["return_content"],
        template_value=db["rule_template"]
    )

    TableRulePage(page).fill_rule_content_and_save(db['temp_rule_content'])
    TableRulePage(page).close_rule_tab()
    MakeRulePage(page).go_to_rule_page(db["folder_name"], db["rule_name"])
    # TableRulePage(page).drag_drop(page.get_by_role("treeitem", name="Z 테이블 룰 44", exact=True).locator("span"), wait_for_cell_in_iframe(page, "td[data-row='1'][data-col='2']"))
    TableRulePage(page).fill_rule_content_and_save(db['rule_content'])

    run_test_and_verify(page, db)
    clean_up(page, db)

def get_rule_page(page, test_id):
    _, db = initialize_test(page, test_id)
    TopFolderPage(page).create_top_folder(db["top_folder_name"])
    FolderPage(page).create_folder(db["top_folder_name"], db["folder_name"])
    return db, MakeRulePage(page)

def setup_rule_with_item(page, test_id):
    db, make_rule_page = get_rule_page(page, test_id)
    item_tab = ItemPage(page)
    popup = item_tab.open_item_manage_page()
    ItemPage(popup).add_item(db["item_content"])
    popup.close()

    make_rule_page.create_rule(
        folder_name=db["folder_name"],
        name=db["rule_name"],
        return_value=db["return_content"],
        template_value=db["rule_template"]
    )
    assert make_rule_page.is_rule_in_tree(db["rule_name"])
    return db, make_rule_page

def setup_multi_rule_with_item(page, test_id):
    db, make_rule_page = get_rule_page(page, test_id)
    item_tab = ItemPage(page)
    popup = item_tab.open_item_manage_page()
    ItemPage(popup).add_item(db["item_content"])
    popup.close()

    make_rule_page.create_multiple_ruturn_rule(
        folder_name=db["folder_name"],
        name=db["rule_name"],
        return_value=db["return_content"],
        template_value=db["rule_template"]
    )
    assert make_rule_page.is_rule_in_tree(db["rule_name"])
    return db, make_rule_page

