import os
from playwright.sync_api import Page
from dotenv import load_dotenv
from pages.login.login import LoginPage
from pages.folder.top_folder import TopFolderPage
from pages.folder.folder import FolderPage
from utils.test_loader import load_test_data
from utils.ui_selectors import BASE_FOLDER_SAVE_BTN

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


def setup_folder_test(page: Page, account_id: int, data_key_order: int):
    _, account_data = initialize_test(page, account_id)
    test_data = load_test_data(data_key_order, table="TESTCASEDATA")
    top_folder = TopFolderPage(page)
    folder = FolderPage(page)
    return top_folder, folder, account_data, test_data


def test_auto_ir8_tc_011_add_TF(page: Page):
    # 1. 공통 Setup 
    top_folder, folder, _, test_data = setup_folder_test(page, account_id=1, data_key_order=11)

    # 2. DB에서 폴더명 및 권한 변경 대상 계정 조회
    folder_name = test_data["top_folder_name"]
    target_account = load_test_data(0, table="TESTACCOUNT")
    target_user_id = target_account["user_id"]

    # 3. 최상위 폴더 생성
    top_folder.open_add_folder_popup()
    top_folder.add_folder_name(folder_name)
    top_folder.click_add_button()
    top_folder.click_save_button()

    # 4. 화면 스크롤 후 폴더 우클릭 (수정 포인트)
    target_folder = page.get_by_text(folder_name, exact=True).first
    target_folder.scroll_into_view_if_needed()
    target_folder.click(button="right", force=True)

    page.get_by_text("폴더 권한 변경", exact=True).last.click()

    # 5. 사용자 권한 목록 추가 및 전체 선택
    folder.add_user_to_permission_list(target_user_id)
    folder.select_checked_users()

    # [캡처 3] 전체 선택 적용 후 화면
    page.screenshot(path="artifacts/folder/capture_TC_011_STEP03.png")

    # 6. 하단 [확인] 저장 버튼 클릭
    page.locator(BASE_FOLDER_SAVE_BTN).click()