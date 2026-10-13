import os
from pages.login.login import LoginPage
from utils.test_loader import load_test_data
from utils.ui_selectors import TOP_FOLDER_ADD_BTN
from playwright.sync_api import expect
from pathlib import Path

def initialize_test(page, account_id):
    account_data = load_test_data(
        account_id,
        "TESTACCOUNT"
    )

    target_url = os.getenv("TARGET_URL")

    if not target_url:
        raise EnvironmentError(
            ".env 파일에 TARGET_URL이 설정되어 있지 않습니다."
        )

    print(f"ACCOUNT_ID={account_id}")
    print(f"테스트 URL={target_url}")

    page.goto(target_url)

    login_page = LoginPage(page)
    login_page.ir_login(
        account_data["user_id"],
        account_data["user_pw"]
    )

    return login_page, account_data


def test_AUTO_IR8_TC_004(page):
    """AUTO-IR8-TC-004: 존재하는 사용자 ID와 등록된 비밀번호로 로그인"""

    login_page, account_data = initialize_test(page,account_id=3)

    # 메인 화면 진입 여부 확인
    top_folder_add_button = login_page.page.locator(TOP_FOLDER_ADD_BTN)
    expect(top_folder_add_button).to_be_visible(timeout=10000)

    # 스크린샷 저장 폴더 생성
    capture_dir = Path("artifacts") / "login"
    capture_dir.mkdir(parents=True, exist_ok=True)

    # 스크린샷 경로 및 파일명 지정
    capture_path = (capture_dir /"capture_TC_004_STEP01_01.png")

    # 메인 화면 전체 캡처
    login_page.page.screenshot(path=str(capture_path),full_page=True)

    print(f"사용 계정: {account_data['user_id']}")
    print(f"스크린샷 저장 경로: {capture_path}")