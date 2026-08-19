import pytest
from conftest import REPEAT_COUNT
from pages.IR.main_page.side_bar.item.item import ItemPage
from test_login import initialize_test

class TestItem:

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_19_add_item_without_name(self, page):
        """TC-019: 항목 이름 없이 항목 추가 (오류)"""
        item, db = setup_item_test(page, 19)
        item.add_item(db['item_content'])
        item.assert_alert_message(db["expected_result"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_20_add_valid_item(self, page):
        """TC-020: 정상적인 항목 이름으로 항목 추가"""
        item, db = setup_item_test(page, 20)
        item.add_item(db["item_content"])

        item.assert_alert_message(db["expected_result"])

        item.close_alert_dialog()
        item.delete_items(db["item_content"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_21_add_duplicate_item(self, page):
        """TC-021: 중복된 항목 이름 입력 시도 (오류)"""
        item, db = setup_item_test(page, 21)
        item.add_item_and_close(db["item_content"])

        item.add_item(db["item_content"])
        page.wait_for_timeout(500)  # 대기
        item.assert_alert_message(db["expected_result"])

        item.close_alert_dialog()
        item.close_item_dialog()
        item.delete_items(db["item_content"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_22_rename_item(self, page):
        """TC-022: 기존 항목 이름 수정"""
        item, db = setup_item_test(page, 22)
        item.add_item_and_close(db["item_content"])

        item.rename_item(db["item_name"], db["change_content"])
        page.wait_for_timeout(500)  # 대기
        item.assert_alert_message(db["expected_result"])

        item.close_alert_dialog()
        item.delete_item(db["change_content"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_23_delete_item(self, page):
        """TC-023: 항목 삭제"""
        item, db = setup_item_test(page, 23)
        item.add_item_and_close(db["item_content"])

        item.delete_item(db["item_name"])

        item.assert_alert_message(db["expected_result"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_24_add_reference_without_data(self, page):
        """TC-024: 참조항목 데이터 없이 등록 시도 (오류)"""
        item, db = setup_item_test(page, 24)
        item.add_item_and_close(db["item_content"])

        item.add_reference(db["item_name"], "")
        item.assert_alert_message(db["expected_result"])

        item.close_alert_dialog()
        item.close_ref_dialog()
        item.delete_item(db["item_name"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_25_add_multiple_references(self, page):
        """TC-025: 여러 참조 항목을 한 번에 등록"""
        item, db = setup_item_test(page, 25)
        item.add_item_and_close(db["item_content"])

        item.add_reference_and_close(db["item_name"], db["ref_content"])

        item.assert_reference_text(db["item_name"], db["expected_result"])

        item.delete_all_references(db["item_name"])
        item.delete_item(db["item_name"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_26_edit_and_delete_references(self, page):
        """TC-026: 참조 항목 수정 및 삭제"""
        item, db = setup_item_test(page, 26)
        item.add_item_and_close(db["item_content"])

        item.add_reference_and_close(db["item_name"], db["ref_content"])
        item.add_reference_and_close(db["item_name"], db["change_content"])
        item.delete_reference(db["item_name"], db["delete_target"])

        item.assert_reference_text(db["item_name"], db["expected_result"])

        item.delete_all_references(db["item_name"])
        item.delete_item(db["item_name"])


def setup_item_test(page, test_id):
    _, db = initialize_test(page, test_id)
    item_page = ItemPage(page)
    item_tab = item_page.open_item_manage_page()
    return ItemPage(item_tab), db
