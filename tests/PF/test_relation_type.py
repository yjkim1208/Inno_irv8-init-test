import pytest
from conftest import REPEAT_COUNT
from pages.PF.type_management.relation_type import RelationTypePage
from utils.test_loader import load_test_data
from pages.login_page.login import LoginPage

@pytest.mark.repeat(REPEAT_COUNT)
def test_TC_053_add_relation_type_successfully(page):
    """TC-053: 신규 관계 오브젝트 유형 구조가 추가되는지 확인한다."""

    db, page_obj = initialize_test(page, 53)

    page_obj.go_to_relation_type_page()
    # page_obj.add_relation_type(db["relation_content"])
    page_obj.click_A()
    page_obj.assert_success_and_confirm(db["expected_result"])
    page_obj.assert_has_relation_type(db["relation_content"])
    page_obj.cleanup_relation_type(db["relation_content"])

def initialize_test(page, test_id):
    db_data = load_test_data(test_id, "pilot_pf_data")
    page.goto(db_data["target_url"])
    login_page = LoginPage(page)
    login_page.pf_login(db_data['user_id'], db_data['user_pw'], db_data['target_url'])
    return db_data, RelationTypePage(page)
