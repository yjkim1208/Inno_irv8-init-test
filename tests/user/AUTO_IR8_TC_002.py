import os
from playwright.sync_api import Page
from dotenv import load_dotenv
from pages.login.login import LoginPage
from pages.user.user import UserPage
from utils.test_loader import load_test_data

load_dotenv()


def initialize_test(page: Page, account_id: int):
    account_data = load_test_data(account_id, table="TESTACCOUNT")
    target_url = os.getenv("TARGET_URL")
    if not target_url:
        raise EnvironmentError(".env 파일에 TARGET_URL이 설정되어 있지 않습니다.")

    page.goto(target_url)

    login_page = LoginPage(page)
    login_page.login(account_data["user_id"], account_data["user_pw"])
    return login_page, account_data


def setup_user_test(page: Page, account_id: int):
    _, account_data = initialize_test(page, account_id)
    user_page = UserPage(page)
    return user_page, account_data


def test_auto_ir8_tc_002(page: Page):
    user_page, _ = setup_user_test(page, account_id=1)
    test_data = load_test_data(2, table="TESTCASEDATA")
    test_user_id = test_data["user_id"]
    test_user_name = test_data["user_name"]
    test_user_pw = test_data["user_pw"]
    # DB의 쉼표 구분 권한 문자열("룰 시스템 접속,전체 기능 실행")을 파이썬 리스트로 변환
    target_roles = [role.strip() for role in test_data["target_roles"].split(",")]

    # 3. 사용자 관리 이동 및 추가 팝업 열기
    user_page.open_user_management()
    user_page.open_add_user_popup()

    # 4. 사용자 정보 입력 및 저장
    user_page.fill_user_info(test_user_id, test_user_name, test_user_pw, target_roles)

    # 5. 저장 확인 및 알림 처리
    success_alert = user_page.click_confirm_and_get_alert()

    # [캡처 1] 스텝 3번: 확인 버튼 클릭 후 화면
    page.screenshot(path="artifacts/user/capture_TC_002_STEP03.png")

    user_page.close_success_alert(success_alert)

    # 6. 추가한 사용자 ID 검색 및 결과 확인
    user_page.search_user(test_user_id)

    # [캡처 2] 스텝 4번: 검색 결과 화면
    page.screenshot(path="artifacts/user/capture_TC_002_STEP04.png")