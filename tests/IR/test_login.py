import re
import pytest
from playwright.sync_api import expect
from pages.login_page.login import LoginPage
from utils.test_loader import load_test_data
from utils.ui_selectors import INPUT_ID_SELECTOR, INPUT_PW_SELECTOR

class TestLogin:

    def test_TC_1_no_input(self, page):
        """TC-1: 아이디와 비밀번호 모두 입력하지 않은 경우 → 아이디 입력란이 invalid 상태여야 함"""
        login_page, _ = initialize_test(page, 1)
        assert login_page.page.locator(f"{INPUT_ID_SELECTOR}:invalid").is_visible()

    def test_TC_2_id_only(self, page):
        """TC-2: 아이디만 입력하고 비밀번호 미입력 → 비밀번호 입력란이 invalid 상태여야 함"""
        login_page, _ = initialize_test(page, 2)
        assert login_page.page.locator(f"{INPUT_PW_SELECTOR}:invalid").is_visible()

    def test_TC_3_wrong_password(self, page):
        """TC-3: 유효한 ID + 틀린 비밀번호 입력 → 오류 메시지 확인"""
        login_page, db = initialize_test(page, 3)
        assert login_page.get_error_message() == db['expected_result']

    def test_TC_4_invalid_id(self, page):
        """TC-4: 존재하지 않는 ID 입력 → 비밀번호 입력란이 invalid 상태여야 함"""
        login_page, _ = initialize_test(page, 4)
        assert login_page.page.locator(f"{INPUT_PW_SELECTOR}:invalid").is_visible()

    def test_TC_5_invalid_id_pw(self, page):
        """TC-5: ID와 비밀번호 모두 잘못된 값 입력 → 오류 메시지 확인"""
        login_page, db = initialize_test(page, 5)
        assert login_page.get_error_message() == db['expected_result']

    def test_TC_6_success(self, page):
        """TC-6: 정상 로그인 → 예상 URL로 이동 완료 확인"""
        login_page, db = initialize_test(page, 6)
        # page.wait_for_timeout(200)  
        login_page.page.wait_for_url(
        f"{db['expected_result']}*",
        timeout=10000
    )
        assert db['expected_result'] in login_page.page.url
        





# def initialize_test(page, test_id):
#     db_data = load_test_data(test_id)
#     page.goto(db_data["target_url"])
#     login_page = LoginPage(page)
#     login_page.ir_login(db_data['user_id'], db_data['user_pw'], db_data['target_url'])
#     return login_page, db_data


def initialize_test(page, test_id):
    db_data = load_test_data(test_id)

    print(f"TEST_ID={test_id}")
    print(f"테스트 URL={db_data['target_url']}")

    page.goto(db_data["target_url"])

    login_page = LoginPage(page)
    login_page.ir_login(
        db_data["user_id"],
        db_data["user_pw"],
        db_data["target_url"]
    )

    return login_page, db_data