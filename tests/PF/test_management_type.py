import pytest
from pages.PF.type_management.management_type import ManagementTypePage
from tests.IR.test_login import initialize_test
from pages.login_page.login import LoginPage
from utils.test_loader import load_test_data
from conftest import REPEAT_COUNT

class TestManagementType:

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_048_add_management_type_successfully(self, page):
        """TC-048: 신규 오브젝트유형 추가 후 저장"""

        db, page_obj = initialize_test(page, 48)

        page_obj.add_management_type(db["object_content"])
        page_obj.assert_success_and_confirm(db["expected_result"])
        page_obj.assert_has_type_names(db["object_content"])
        page_obj.cleanup_management_type(db["object_content"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_049_add_code_rule_to_type_successfully(self, page):
        """TC-049: 관리유형에 채번규칙 추가"""

        db, page_obj = initialize_test(page, 49)

        page_obj.add_management_type(db["object_content"])
        page_obj.assert_success_and_confirm(db["expected_result"])

        type_name = page_obj.get_first_type_name(db["object_content"])

        page_obj.add_code_rule_to_type(type_name, db["code_rule_content"])
        page_obj.assert_success_and_confirm(db["expected_result"])

        page_obj.cleanup_management_type(db["object_content"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_050_add_object_group_successfully(self, page):
        """TC-050: 신규 오브젝트 그룹 생성"""

        db, page_obj = initialize_test(page, 50)
        
        page_obj.go_to_page()
        page_obj.add_object_group(db["object_group_content"])
        page_obj.assert_success_and_confirm(db["expected_result"])
        page_obj.assert_has_group_names(db["object_group_content"])

        page_obj.cleanup_object_group(db["object_group_content"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_051_add_detail_type_successfully(self, page):
        """TC-051: 신규 오브젝트 세부유형 추가"""

        db, page_obj = initialize_test(page, 51)

        page_obj.add_management_type(db["object_content"])
        page_obj.assert_success_and_confirm(db["expected_result"])
        type_name = page_obj.get_first_type_name(db["object_content"])

        page_obj.add_detail_type(type_name, db["object_detail_content"])
        page_obj.assert_success_and_confirm(db["expected_result"])
        page_obj.assert_has_detail_type_names(db["object_detail_content"])

        page_obj.cleanup_detail_types(type_name)
        page_obj.cleanup_management_type(db["object_content"])

    @pytest.mark.repeat(REPEAT_COUNT)
    def test_TC_052_add_group_types_successfully(self, page):
        """TC-052: 신규 오브젝트 그룹별 유형이 추가되는지 확인한다."""

        db, page_obj = initialize_test(page, 52)

        page_obj.add_management_type(db["object_content"])
        page_obj.assert_success_and_confirm(db["expected_result"])

        page_obj.add_object_group(db["object_group_content"])
        page_obj.assert_success_and_confirm(db["expected_result"])
        group_name = page_obj.get_first_type_name(db["object_group_content"])

        page_obj.add_group_type(group_name, db["object_group_type_content"])
        page_obj.assert_success_and_confirm(db["expected_result"])
        page_obj.assert_has_group_type_names(db["object_group_type_content"])

        page_obj.cleanup_group_types()
        page_obj.cleanup_object_group(db["object_group_content"])
        page_obj.cleanup_management_type(db["object_content"])

def initialize_test(page, test_id):
    db_data = load_test_data(test_id, "pilot_pf_data")
    page.goto(db_data["target_url"])
    login_page = LoginPage(page)
    login_page.pf_login(db_data['user_id'], db_data['user_pw'], db_data['target_url'])
    return db_data, ManagementTypePage(page)
