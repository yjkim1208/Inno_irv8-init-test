import pytest
from conftest import (MAX_RERUN_COUNT,RERUN_DELAY_SECONDS)
from pages.IR.main_page.folder_tree.folder import FolderPage
from pages.IR.main_page.folder_tree.top_folder import TopFolderPage
from test_login import initialize_test

def setup_folder_test(page, test_id):
    """기존 폴더 데이터를 정리한 뒤 신규 최상위 폴더를 생성한다."""

    # 로그인 및 테스트 데이터 조회
    _, db = initialize_test(
        page,
        test_id
    )

    folder = FolderPage(page)
    top_folder = TopFolderPage(page)

    top_folder_name = db["top_folder_name"]

    # 폴더 트리 영역이 표시될 때까지 대기
    folder.folder_list_area.wait_for(
        state="visible",
        timeout=10000
    )

    # 테스트에서 사용할 수 있는 하위 폴더 이름
    child_folder_names = [
        db.get("folder_name"),
        db.get("change_content")
    ]

    # None 값과 중복된 이름 제거
    child_folder_names = list(
        dict.fromkeys(
            name
            for name in child_folder_names
            if name
        )
    )

    # 1. 기존 하위 폴더 삭제
    for child_folder_name in child_folder_names:
        while True:
            target_folder = (
                folder.folder_list_area
                .get_by_text(
                    child_folder_name,
                    exact=True
                )
            )

            # 해당 이름의 폴더가 없으면 반복 종료
            if target_folder.count() == 0:
                break

            target_folder.first.wait_for(
                state="visible",
                timeout=5000
            )

            folder.delete_folder(
                child_folder_name
            )

    # 2. 기존 최상위 폴더 삭제
    while True:
        target_top_folder = (
            folder.folder_list_area
            .get_by_text(
                top_folder_name,
                exact=True
            )
        )

        # 해당 이름의 최상위 폴더가 없으면 반복 종료
        if target_top_folder.count() == 0:
            break

        target_top_folder.first.wait_for(
            state="visible",
            timeout=5000
        )

        folder.delete_folder(
            top_folder_name
        )

    # 3. 신규 최상위 폴더 생성
    top_folder.create_top_folder(
        top_folder_name
    )

    # 4. 신규 생성 과정에서 오류가 발생했는지 먼저 확인
    error_dialog = page.locator(
        "#ir_message .ir-confirm.dialog.is-visible"
    )

    if error_dialog.count() > 0:
        error_message = (
            error_dialog
            .last
            .inner_text()
            .strip()
        )

        raise AssertionError(
            "최상위 폴더 생성 중 오류 메시지가 표시되었습니다: "
            f"{error_message}"
        )

    # 5. 오류가 없으면 신규 최상위 폴더 표시 확인
    created_top_folder = (
        folder.folder_list_area
        .get_by_text(
            top_folder_name,
            exact=True
        )
    )

    created_top_folder.wait_for(
        state="visible",
        timeout=5000
    )

    return folder, db

@pytest.mark.flaky(
    reruns=MAX_RERUN_COUNT,
    reruns_delay=RERUN_DELAY_SECONDS
)
class TestFolder:
    def test_TC_10_add_folder_without_name(self, page):
        """TC-010: 폴더 이름 없이 폴더 추가"""
        folder, db = setup_folder_test(page, 10)
        folder.open_add_folder_popup(db["top_folder_name"])
        folder.click_add_button()
        folder.assert_error_message(db["expected_result"])
        folder.close_add_folder_error_dialog()
        folder.delete_folder(db["top_folder_name"])
  
    def test_TC_11_add_valid_folder(self, page):
        """TC-011: 정상적인 폴더 이름으로 추가"""
        folder, db = setup_folder_test(page, 11)

        folder.create_folder(db["top_folder_name"], db['folder_name'])
        folder.assert_folder_is_present(db['expected_result'])

        folder.delete_folder(db["top_folder_name"])

    def test_TC_12_add_duplicate_folder(self, page):
        """TC-012: 중복된 폴더 이름으로 추가"""
        folder, db = setup_folder_test(page, 12)

        folder.create_folder(db["top_folder_name"], db['folder_name'])
        folder.create_folder(db["top_folder_name"], db['folder_name'])

        folder.assert_error_message(db["expected_result"])

        folder.close_duplicate_folder_dialog()
        folder.delete_folder(db["top_folder_name"])

    def test_TC_13_rename_folder(self, page):
        """TC-013: 폴더 이름 변경 (정상)"""
        folder, db = setup_folder_test(page, 13)

        folder.create_folder(db["top_folder_name"], db['folder_name'])
        folder.rename_folder(db["folder_name"], db["change_content"])

        folder.assert_folder_is_present(db['expected_result'])

        folder.delete_folder(db["top_folder_name"])
    
    def test_TC_14_rename_folder_blank(self, page):
        """TC-014: 폴더 이름을 공백으로 변경"""
        folder, db = setup_folder_test(page, 14)

        folder.create_folder(db["top_folder_name"],db["folder_name"])
        folder.rename_folder(db["folder_name"],"")
        folder.assert_error_message(db["expected_result"])
        folder.close_rename_error_dialog()
        folder.delete_folder(db["folder_name"])
        folder.delete_folder( db["top_folder_name"])

    def test_TC_15_rename_folder_duplicate(self, page):
        """TC-015: 폴더 이름을 중복으로 변경"""
        folder, db = setup_folder_test(page, 15)

        folder.create_folder(db["top_folder_name"], db['folder_name'])
        folder.create_folder(db["top_folder_name"], db["change_content"])
        folder.rename_folder(db["folder_name"], db["change_content"])

        folder.assert_error_message(db["expected_result"])

        folder.close_rename_error_dialog()
        folder.delete_folder(db["folder_name"])
        folder.delete_folder(db["change_content"])
        folder.delete_folder(db["top_folder_name"])

    def test_TC_16_rename_folder_same_name(self, page):
        """TC-016: 동일한 이름으로 변경"""
        folder, db = setup_folder_test(page, 16)

        folder.create_folder(db["top_folder_name"], db['folder_name'])
        folder.rename_folder(db["folder_name"], db["folder_name"])

        folder.assert_folder_is_present(db['expected_result'])
        folder.delete_folder(db["top_folder_name"])

    def test_TC_17_cancel_delete_folder(self, page):
        """TC-017: 폴더 삭제 취소"""
        folder, db = setup_folder_test(page, 17)

        folder.create_folder(db["top_folder_name"],db["folder_name"])
        folder.cancel_delete_folder(db["folder_name"])

        # 삭제 취소 후 폴더가 유지되는지 검증
        folder.assert_folder_is_present(db["expected_result"])

        # 다음 반복 실행에 영향을 주지 않도록 실제 삭제
        folder.delete_folder(db["folder_name"])
        folder.delete_folder(db["top_folder_name"])