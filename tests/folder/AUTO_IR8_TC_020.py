import os
from playwright.sync_api import Page
from dotenv import load_dotenv
from pages.login.login import LoginPage
from pages.folder.top_folder import TopFolderPage
from utils.test_loader import load_test_data
from utils.ui_selectors import (
    FOLDER_NAME_ALERT,
    BASE_FOLDER_DELETE_BTN_NAME,
    BTN_TEXT_NO,
)

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


def test_auto_ir8_tc_020_add_TF(page: Page):
    # 1. 공통 Setup 
    top_folder, _, test_data = setup_top_folder_test(page, account_id=2, data_key_order=22)
    folder_name = test_data.get("top_folder_name") or test_data.get("data")

    # 2. 최상위 폴더 추가 및 저장
    top_folder.open_add_folder_popup()
    top_folder.add_folder_name(folder_name)
    top_folder.click_add_button()
    top_folder.click_save_button()

    # 3. 추가된 폴더 우클릭 -> 삭제 선택
    target_folder = page.get_by_role("treeitem", name=folder_name)
    target_folder.scroll_into_view_if_needed()
    target_folder.click(button="right")
    page.get_by_text(BASE_FOLDER_DELETE_BTN_NAME, exact=True).last.click()

    # 4. 삭제 확인 팝업 대기 및 스크린샷
    confirm_dialog = page.locator(FOLDER_NAME_ALERT)
    confirm_dialog.wait_for(state="visible", timeout=3000)

    # [캡처 1] 스텝 2번: 삭제 확인 팝업 노출 화면
    page.screenshot(path="artifacts/folder/capture_TC_020_STEP02.png")

    # 5. '아니오' 버튼 클릭하여 삭제 취소
    confirm_dialog.get_by_role("button", name=BTN_TEXT_NO, exact=True).click()

    # [캡처 2] 스텝 3번: 삭제 취소 후 화면
    page.screenshot(path="artifacts/folder/capture_TC_020_STEP03.png")