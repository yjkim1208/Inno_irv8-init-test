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

def test_AUTO_IR8_TC_016(page):
    """상위 폴더 지정후 동일한 상위에 중복되는 이름을 1개 입력하여 폴더 추가"""
    (top_folder, folder ,  account_data, test_data) = (
        setup_top_folder_test(page,account_id=3,data_key_order=16)
    )
    top_folder_name = test_data["data"]

    while folder.is_folder_present(top_folder_name,timeout=1000):
        folder.delete_folder(top_folder_name)   
    top_folder.create_top_folder(top_folder_name)
    created_top_folder = (folder.get_treeitem(top_folder_name))

    # 스크린샷 저장 폴더 생성
    capture_dir = Path("artifacts") / "folder"
    capture_dir.mkdir(parents=True, exist_ok=True)
    # 스크린샷 경로 및 파일명 지정
    first_capture_path  = (capture_dir /"capture_TC_016_STEP03_01.png")
    # 메인 화면 전체 캡처
    top_folder.page.wait_for_timeout(500)
    top_folder.page.screenshot(path=str(first_capture_path ),full_page=True)
    print(f"스크린샷 저장 경로: {first_capture_path }")

    # 동일한 상위폴더명 2번 입력
    top_folder.create_top_folder(top_folder_name)
    created_top_folder = (folder.get_treeitem(top_folder_name))
    actual_message = (folder.get_error_message())
    assert actual_message == "[IRE-21304]폴더 이름이 중복됩니다. [AUTO_최상위폴더16]\n확인"

     # 스크린샷 저장 폴더 생성
    capture_dir = Path("artifacts") / "folder"
    capture_dir.mkdir(parents=True, exist_ok=True)
    # 스크린샷 경로 및 파일명 지정
    second_capture_path  = (capture_dir /"capture_TC_016_STEP06_01.png")
    # 메인 화면 전체 캡처
    top_folder.page.wait_for_timeout(500)
    top_folder.page.screenshot(path=str(second_capture_path ),full_page=True)
    print(f"스크린샷 저장 경로: {second_capture_path }")
    top_folder.close_duplicate_folder_dialog()
    top_folder.delete_folder(top_folder_name)

