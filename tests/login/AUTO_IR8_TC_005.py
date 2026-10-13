import os
import pyautogui
from pages.login.login import LoginPage
from utils.ui_selectors import INPUT_ID_SELECTOR
from playwright.sync_api import expect
from pathlib import Path

def initialize_test(page):

    target_url = os.getenv("TARGET_URL")

    if not target_url:
        raise EnvironmentError(
            ".env 파일에 TARGET_URL이 설정되어 있지 않습니다."
        )

    page.goto(target_url)

    login_page = LoginPage(page)
    login_page.ir_login(
        user_id=None,
        user_pw=None
    )

    return login_page

def test_AUTO_IR8_TC_005(page):
    """AUTO-IR8-TC-005: 사용자 ID, 비밀번호 입력 없이 로그인"""
    
    login_page = initialize_test(page)
    id_input = login_page.page.locator(INPUT_ID_SELECTOR)
    expect(id_input).to_be_visible()

    invalid_id_input = login_page.page.locator(f"{INPUT_ID_SELECTOR}:invalid")
    expect(invalid_id_input).to_be_visible()
    validation_message = id_input.evaluate("element => element.validationMessage")
    assert validation_message, ("이 입력란을 작성하세요.")

     # 스크린샷 저장 폴더 생성
    capture_dir = Path("artifacts") / "login"
    capture_dir.mkdir(parents=True, exist_ok=True)

    # 스크린샷 경로 및 파일명 지정
    capture_path = (capture_dir /"capture_TC_005_STEP01_01.png")

    # 메인 화면 전체 캡처
    login_page.page.wait_for_timeout(500)

    # Playwright가 아닌 Windows 전체 화면 캡처
    pyautogui.screenshot(str(capture_path))

    print(f"스크린샷 저장 경로: {capture_path}")