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


def setup_top_folder_test(page: Page, account_id: int, data_key_order: int):
    _, account_data = initialize_test(page, account_id)
    test_data = load_test_data(data_key_order, table="TESTCASEDATA")
    top_folder = TopFolderPage(page)
    return top_folder, account_data, test_data


def test_auto_ir8_tc_013_add_TF(page: Page):
    # 1. 공통 Setup 
    top_folder, _, test_data = setup_top_folder_test(page, account_id=1, data_key_order=13)
    folder_name = test_data.get("top_folder_name") or test_data.get("data")

    # 2. 1차 최상위 폴더 추가 팝업 열기 및 폴더명 입력 후 추가
    top_folder.open_add_folder_popup()
    top_folder.add_folder_name(folder_name)
    top_folder.click_add_button()

    # [캡처 1] 스텝 2번: 1차 추가 화면
    page.screenshot(path="artifacts/folder/capture_TC_013_STEP02.png")

    # 3. 1차 폴더 생성 및 저장
    top_folder.click_save_button()

    # [캡처 2] 스텝 3번: 1차 생성 후 폴더 리스트 화면
    page.screenshot(path="artifacts/folder/capture_TC_013_STEP03.png")

    # 4. 2차 최상위 폴더 추가 팝업 열기 및 동일한 폴더명 입력 후 추가
    top_folder.open_add_folder_popup()
    top_folder.add_folder_name(folder_name)
    top_folder.click_add_button()

    # [캡처 3] 스텝 5번: 2차 중복 입력 추가 화면
    page.screenshot(path="artifacts/folder/capture_TC_013_STEP05.png")

    # 5. 2차 저장 시도 (중복 생성 시도)
    top_folder.click_save_button()

    # [캡처 4] 스텝 6번: 중복 오류 메시지 노출 화면
    page.screenshot(path="artifacts/folder/capture_TC_013_STEP06.png")

    # 6. 중복 폴더명 경고 알림 확인 및 닫기
    warning_alert = page.locator(FOLDER_NAME_ALERT).last
    warning_alert.wait_for(state="visible", timeout=3000)
    warning_alert.get_by_role("button", name=BTN_TEXT_CONFIRM, exact=True).click()