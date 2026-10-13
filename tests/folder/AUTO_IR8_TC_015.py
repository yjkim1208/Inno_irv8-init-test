import os
from pathlib import Path
from utils.test_loader import load_test_data
from pages.login.login import LoginPage
from pages.folder.top_folder import TopFolderPage
from pages.folder.folder import FolderPage

def initialize_test(page, account_id):
    account_data = load_test_data(account_id,"TESTACCOUNT")
    target_url = os.getenv("TARGET_URL")

    if not target_url:
        raise EnvironmentError(
            ".env 파일에 TARGET_URL이 설정되어 있지 않습니다."
        )

    page.goto(target_url)

    login_page = LoginPage(page)
    login_page.ir_login(
        user_id=account_data["user_id"],
        user_pw=account_data["user_pw"]
    )
    return login_page, account_data

def setup_top_folder_test(page, account_id, data_key_order):
    _, account_data = initialize_test(page,account_id)
    test_data  = load_test_data(data_key_order,"TESTCASEDATA")
    top_folder = TopFolderPage(page)
    folder = FolderPage(page)
    return (top_folder, folder , account_data, test_data)

def test_AUTO_IR8_TC_015(page):
    """폴더 이름 입력 없이 폴더 추가"""
    (top_folder, folder ,  account_data, test_data) = (
        setup_top_folder_test(page,account_id=3,data_key_order=15))
    top_folder_name = test_data["data"]

    while folder.is_folder_present(top_folder_name,timeout=1000):
        folder.delete_folder(top_folder_name)   
    top_folder.create_top_folder(top_folder_name)
    created_top_folder = (folder.get_treeitem(top_folder_name))
    folder.open_add_folder_popup(top_folder_name)
    top_folder.click_add_button()  # 이름 없이 추가
    actual_message = (folder.get_error_message())
    assert actual_message == "폴더 이름을 입력하십시오.\n확인"

    # 스크린샷 저장 폴더 생성
    capture_dir = Path("artifacts") / "folder"
    capture_dir.mkdir(parents=True, exist_ok=True)

    # 스크린샷 경로 및 파일명 지정
    capture_path = (capture_dir /"capture_TC_015_STEP02_01.png")
    # 메인 화면 전체 캡처
    top_folder.page.wait_for_timeout(500)
    top_folder.page.screenshot(path=str(capture_path),full_page=True)
    print(f"스크린샷 저장 경로: {capture_path}")
