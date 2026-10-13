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


def test_auto_ir8_tc_014_add_TF(page: Page):
    # 1. 공통 Setup (계정 ID: 3, 최상위 폴더 데이터 Key SEQ: 14)
    top_folder, _, test_data = setup_top_folder_test(page, account_id=3, data_key_order=14)
    top_folder_name = test_data.get("top_folder_name") or test_data.get("data")

    # 2. 최상위 폴더 생성
    top_folder.open_add_folder_popup()
    top_folder.add_folder_name(top_folder_name)
    top_folder.click_add_button()
    top_folder.click_save_button()

    # 3. 추가한 상위 폴더 우클릭 -> '폴더 추가' 선택
    target_folder = page.get_by_role("treeitem", name=top_folder_name)
    target_folder.scroll_into_view_if_needed()
    target_folder.click(button="right")
    page.get_by_text("폴더 추가", exact=True).last.click()

    # 4. 하위 폴더 데이터 조회 (Key SEQ: 15) 및 입력
    sub_folder_data = load_test_data(15, table="TESTCASEDATA")
    sub_folder_name = (
        sub_folder_data.get("folder_name")
        or sub_folder_data.get("top_folder_name")
        or sub_folder_data.get("data")
    )

    top_folder.add_folder_name(sub_folder_name)
    top_folder.click_add_button()

    # [캡처 1] 스텝 5번: 하위 폴더 목록 추가 화면
    page.screenshot(path="artifacts/folder/capture_TC_014_STEP05.png")

    # 5. 하위 폴더 최종 저장
    top_folder.click_save_button()

    # [캡처 2] 스텝 6번: 하위 폴더 추가 완료 화면
    page.screenshot(path="artifacts/folder/capture_TC_014_STEP06.png")