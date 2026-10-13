import os
from playwright.sync_api import Page
from dotenv import load_dotenv
from pages.login.login import LoginPage
from pages.folder.top_folder import TopFolderPage
from utils.test_loader import load_test_data
from utils.ui_selectors import (
    BASE_FOLDER_MODIFY_BIZ_POP,
    FOLDER_RENAME_INPUT,
    FOLDER_RENAME_SAVE_BTN,
    FOLDER_NAME_ALERT,
    BTN_TEXT_CONFIRM,
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


def setup_top_folder_test(page: Page, account_id: int):
    _, account_data = initialize_test(page, account_id)
    top_folder = TopFolderPage(page)
    return top_folder, account_data


def test_auto_ir8_tc_019_add_TF(page: Page):
    # 1. 공통 Setup (계정 ID: 2)
    top_folder, _ = setup_top_folder_test(page, account_id=2)

    # 2. 첫 번째 최상위 폴더 데이터 조회 (Key SEQ: 20) 및 생성
    test_data1 = load_test_data(20, table="TESTCASEDATA")
    folder_name1 = test_data1.get("top_folder_name") or test_data1.get("data")

    top_folder.open_add_folder_popup()
    top_folder.add_folder_name(folder_name1)
    top_folder.click_add_button()
    top_folder.click_save_button()

    # 3. 두 번째 최상위 폴더 데이터 조회 (Key SEQ: 21) 및 생성
    test_data2 = load_test_data(21, table="TESTCASEDATA")
    folder_name2 = test_data2.get("top_folder_name") or test_data2.get("data")

    top_folder.open_add_folder_popup()
    top_folder.add_folder_name(folder_name2)
    top_folder.click_add_button()
    top_folder.click_save_button()

    # 4. 두 번째 폴더 우클릭 -> '폴더 이름 변경' 선택
    target_folder = page.get_by_role("treeitem", name=folder_name2)
    target_folder.scroll_into_view_if_needed()
    target_folder.click(button="right")
    page.get_by_text("폴더 이름 변경", exact=True).last.click()

    # 5. 기존 생성한 첫 번째 폴더명(folder_name1)으로 변경 시도 (중복 이름)
    modify_pop = page.locator(BASE_FOLDER_MODIFY_BIZ_POP)
    modify_pop.wait_for(state="visible", timeout=3000)

    modify_pop.locator(FOLDER_RENAME_INPUT).fill(folder_name1)
    modify_pop.locator(FOLDER_RENAME_SAVE_BTN).click()

    # [캡처] 폴더 이름 중복 알림 노출 화면
    page.screenshot(path="artifacts/folder/capture_TC_019_STEP02.png")

    # 6. 이름 중복 경고 알림 확인 및 닫기
    alert_dialog = page.locator(FOLDER_NAME_ALERT)
    alert_dialog.wait_for(state="visible", timeout=3000)
    alert_dialog.get_by_role("button", name=BTN_TEXT_CONFIRM, exact=True).click()