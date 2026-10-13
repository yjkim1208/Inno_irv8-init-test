import os
import pyautogui
from pages.login.login import LoginPage
from utils.test_loader import load_test_data
from utils.ui_selectors import INPUT_PW_SELECTOR
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
        user_pw=None
    )

    return login_page, account_data

def test_AUTO_IR8_TC_006(page):
    """AUTO-IR8-TC-006: 사용자 ID 만 입력한 후 로그인"""
    
    login_page, account_data = initialize_test(page,account_id=3)
    pw_input = login_page.page.locator(INPUT_PW_SELECTOR)
    expect(pw_input).to_be_visible()

    invalid_pw_input = login_page.page.locator(f"{INPUT_PW_SELECTOR}:invalid")
    expect(invalid_pw_input).to_be_visible()
    assert invalid_pw_input, ("이 입력란을 작성하세요.")

     # 스크린샷 저장 폴더 생성
    capture_dir = Path("artifacts") / "login"
    capture_dir.mkdir(parents=True, exist_ok=True)

    # 스크린샷 경로 및 파일명 지정
    capture_path = (capture_dir /"capture_TC_006_STEP01_01.png")

    # 메인 화면 전체 캡처
    login_page.page.wait_for_timeout(500)

    # Playwright가 아닌 Windows 전체 화면 캡처
    pyautogui.screenshot(str(capture_path))

    print(f"스크린샷 저장 경로: {capture_path}")