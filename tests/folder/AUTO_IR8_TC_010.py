import os
from playwright.sync_api import Page
from dotenv import load_dotenv
from pages.login.login import LoginPage
from pages.folder.top_folder import TopFolderPage
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


def setup_top_folder_test(page: Page, account_id: int, data_key_order: int):
    _, account_data = initialize_test(page, account_id)
    test_data = load_test_data(data_key_order, table="TESTCASEDATA")
    top_folder = TopFolderPage(page)
    return top_folder, account_data, test_data


def test_auto_ir8_tc_010_add_TF(page: Page):
    # 1. 공통 Setup (계정 ID: 2)
    top_folder, _, test_data = setup_top_folder_test(page, account_id=2, data_key_order=10)

    # 2. DB에서 top_folder_name 키값 추출 ('AUTO_최상위폴더10')
    folder_name = test_data["top_folder_name"]

    # 3. 최상위 폴더 추가 팝업 열기 및 폴더명 입력 후 추가
    top_folder.open_add_folder_popup()
    top_folder.add_folder_name(folder_name)
    top_folder.click_add_button()

    # [캡처 1] 스텝 2번: 추가 화면
    page.screenshot(path="artifacts/folder/capture_TC_010_STEP02.png")

    # 4. 저장 버튼 클릭
    top_folder.click_save_button()
    page.wait_for_timeout(1000)

    # [캡처 2] 스텝 3번: 확인 버튼 클릭 후 화면
    page.screenshot(path="artifacts/folder/capture_TC_010_STEP03.png")