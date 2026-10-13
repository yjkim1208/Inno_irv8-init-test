import os
from playwright.sync_api import Page
from dotenv import load_dotenv
from pages.login.login import LoginPage
from pages.folder.top_folder import TopFolderPage
from utils.test_loader import load_test_data
from utils.ui_selectors import BTN_TEXT_CONFIRM, FOLDER_NAME_ALERT

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


def setup_top_folder_test(page: Page, account_id: int):
    _, account_data = initialize_test(page, account_id)
    top_folder = TopFolderPage(page)
    return top_folder, account_data


def test_auto_ir8_tc_012_add_TF(page: Page):
    # 1. 공통 Setup (계정 ID: 1)
    top_folder, _ = setup_top_folder_test(page, account_id=1)

    # 2. 최상위 폴더 추가 팝업 열기
    top_folder.open_add_folder_popup()

    # 3. 폴더명을 입력하지 않은 상태로 [추가] 버튼 클릭
    top_folder.click_add_button()

    # [캡처 1] 스텝 2번: 경고 알림 노출 화면
    page.screenshot(path="artifacts/folder/capture_TC_012_STEP02.png")

    # 4. 필수 입력 경고 알림 확인 및 [확인] 버튼 클릭
    warning_alert = page.locator(FOLDER_NAME_ALERT).last
    warning_alert.wait_for(state="visible", timeout=10000)
    warning_alert.get_by_role("button", name=BTN_TEXT_CONFIRM, exact=True).click()