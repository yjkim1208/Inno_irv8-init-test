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

def test_AUTO_IR8_TC_017(page):
    """신규 폴더 이름을 입력하여 폴더 이름 변경"""
    (top_folder, folder ,  account_data, test_data) = (
        setup_top_folder_test(page, account_id=3, data_key_order=17)
    )
    original_folder_name = test_data["data"]
    change_data = load_test_data(18,"TESTCASEDATA")
    changed_folder_name = change_data["data"]
    cleanup_folder_names = [original_folder_name,changed_folder_name]
    for folder_name in cleanup_folder_names:
            while folder.is_folder_present(folder_name,timeout=1000):
                folder.delete_folder(folder_name) 
    top_folder.create_top_folder(original_folder_name)
    created_top_folder = (folder.get_treeitem(original_folder_name))
    # 스크린샷 저장 폴더 생성
    capture_dir = Path("artifacts") / "folder"
    capture_dir.mkdir(parents=True, exist_ok=True)
    # 스크린샷 경로 및 파일명 지정
    first_capture_path  = (capture_dir /"capture_TC_017_STEP01_01.png")
    # 메인 화면 전체 캡처
    top_folder.page.wait_for_timeout(500)
    top_folder.page.screenshot(path=str(first_capture_path ),full_page=True)
    print(f"스크린샷 저장 경로: {first_capture_path }")

    #기존 폴더 이름을 변경
    folder.rename_folder(name=original_folder_name,change_name=changed_folder_name)
    renamed_folder = folder.get_treeitem(changed_folder_name)
    assert folder.is_folder_present(changed_folder_name)

     # 스크린샷 저장 폴더 생성
    capture_dir = Path("artifacts") / "folder"
    capture_dir.mkdir(parents=True, exist_ok=True)
    # 스크린샷 경로 및 파일명 지정
    second_capture_path  = (capture_dir /"capture_TC_017_STEP02_01.png")
    # 메인 화면 전체 캡처
    top_folder.page.wait_for_timeout(500)
    top_folder.page.screenshot(path=str(second_capture_path ),full_page=True)
    print(f"스크린샷 저장 경로: {second_capture_path }")