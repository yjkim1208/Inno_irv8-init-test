import os
import pyautogui
from pages.login.login import LoginPage
from utils.test_loader import load_test_data
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

    page.goto(target_url)

    login_page = LoginPage(page)
    login_page.ir_login(
        user_id=account_data["user_id"],
        user_pw="1234"
    )

    return login_page, account_data

def test_AUTO_IR8_TC_007(page):
    """AUTO-IR8-TC-007: 존재하는 사용자의 사용자 ID를 입력하고 틀린 비밀번호 입력 후 로그인"""
    login_page, account_data = initialize_test(page,account_id=3)
    actual_message = login_page.get_error_message()
    assert actual_message == "[IRE-21130]사용자 ID 또는 비밀번호가 일치하지 않습니다."

    # 스크린샷 저장 폴더 생성
    capture_dir = Path("artifacts") / "login"
    capture_dir.mkdir(parents=True, exist_ok=True)

    # 스크린샷 경로 및 파일명 지정
    capture_path = (capture_dir /"capture_TC_007_STEP01_01.png")

    # 메인 화면 전체 캡처
    login_page.page.wait_for_timeout(500)

    # Playwright가 아닌 Windows 전체 화면 캡처
    pyautogui.screenshot(str(capture_path))

    print(f"스크린샷 저장 경로: {capture_path}")