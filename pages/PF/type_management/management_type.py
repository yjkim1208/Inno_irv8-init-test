from pages.PF.type_management.management_type_sections.object_type import ObjectType
from pages.PF.type_management.management_type_sections.object_group import ObjectGroup
from pages.PF.type_management.management_type_sections.detail_type import DetailType
from pages.PF.type_management.management_type_sections.group_type import GroupType
from pages.PF.type_management.management_type_sections.management_type_section import ManagementTypeSection
from pages.components.iframe_dialog import IframeDialog

class ManagementTypePage:
    def __init__(self, page):
        self.page = page
        self.dialog = IframeDialog(page)
        self.object_type = ObjectType(page)
        self.object_group = ObjectGroup(page)
        self.detail_type = DetailType(page)
        self.group_type = GroupType(page)
        self.manage_type_section = ManagementTypeSection(page)

    # --- 공통 Dialog ---
    def get_success_message(self, timeout=5000):
        return self.dialog.get_message(timeout)

    def confirm_success(self, timeout=5000):
        self.dialog.confirm(timeout)

    def assert_success_and_confirm(self, expected_message):
        actual_message = self.get_success_message()
        assert actual_message == expected_message, f"[❌] 메시지 불일치\n기대한 값: {expected_message}\n실제 값: {actual_message}"
        self.confirm_success()


    # --- 네비게이션 ---
    def go_to_page(self):
        self.manage_type_section.go_to_management_page()

    # ---  시나리오 메서드 ---
    def add_management_type(self, content):
        self.go_to_page()
        self.object_type.create(content)

    def add_code_rule_to_type(self, type_name, content):
        self.object_type.click_code_rule_button(type_name)
        self.object_type.input_code_rule(content)
        self.object_type.save_code_rule()

    def add_object_group(self, content):
        self.object_group.click_add()
        self.object_group.input(content)
        self.object_group.save()

    def add_detail_type(self, type_name, content):
        self.object_type.click_name(type_name)
        self.detail_type.click_add()
        self.detail_type.input(content)
        self.detail_type.save()

    def add_group_type(self, group_name, content):
        self.group_type.click_group(group_name)
        self.group_type.click_add()
        self.group_type.input(content)
        self.group_type.save()

    # --- 이름 추출 ---
    def get_first_type_name(self, content):
        return self.object_type.extract_names(content)[0]

    def get_type_names(self, content):
        return self.object_type.extract_names(content)

    def get_group_names(self, content):
        return self.object_group.extract_names(content)

    def get_group_type_names(self, content):
        return self.group_type.extract_names(content)

    def get_detail_type_names(self, content):
        return self.detail_type.extract_names(content)

    # --- 존재 여부 확인 ---
    def has_type_names(self, names):
        return self.object_type.has(names)

    def has_group_names(self, names):
        return self.object_group.has(names)

    def has_detail_type_names(self, names):
        return self.detail_type.has(names)

    def has_group_type_names(self, names):
        return self.group_type.has(names)

    def assert_has_type_names(self, content):
        names = self.get_type_names(content)
        assert self.has_type_names(names)

    def assert_has_group_names(self, content):
        names = self.get_group_names(content)
        assert self.has_group_names(names)

    def assert_has_detail_type_names(self, content):
        names = self.get_detail_type_names(content)
        assert self.has_detail_type_names(names)

    def assert_has_group_type_names(self, content):
        names = self.get_group_type_names(content)
        assert self.has_group_type_names(names)

    # --- 삭제 시나리오 ---
    def cleanup_management_type(self, content):
        self.object_type.delete(self.object_type.extract_names(content))
        self.dialog.confirm()

    def cleanup_object_group(self, content):
        self.object_group.delete(self.object_group.extract_names(content))
        self.dialog.confirm()

    def cleanup_detail_types(self, type_name):
        self.object_type.click_name(type_name)
        self.detail_type.delete_all()
        self.dialog.confirm()

    def cleanup_group_types(self):
        self.group_type.delete_all()
        self.dialog.confirm()
