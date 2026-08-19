from .item_section import ItemSection
from .reference_section import ReferenceSection
from pages.components.dialog import Dialog

class ItemPage:
    def __init__(self, page):
        self.page = page
        self.item_section = ItemSection(page)
        self.reference_section = ReferenceSection(page)
        self.dialog = Dialog(page)

    # 항목 관련 위임
    def add_item(self, name):
        self.item_section.add_item(name)

    def add_item_and_close(self, name: str):
        self.add_item(name)
        self.close_alert_dialog()
        
    def rename_item(self, name, new_name):
        self.item_section.rename_item(name, new_name)

    def delete_item(self, name):
        self.item_section.delete_item(name)

    def delete_items(self, content):
        self.item_section.delete_items(content)

    def search_and_select_item(self, name, dblclick=False):
        self.item_section.search_and_select_item(name, dblclick)

    def open_item_manage_page(self):
        return self.item_section.open_popup()

    def close_item_dialog(self):
        self.item_section.close_popup()




    # 참조값 관련 위임
    def add_reference(self, name, ref):
        self.reference_section.add_reference(self.item_section, name, ref)

    def add_reference_and_close(self, item_name: str, ref_value: str):
        self.add_reference(item_name, ref_value)
        self.page.wait_for_timeout(200)
        self.close_alert_dialog()

    def delete_reference(self, name, target):
        self.reference_section.delete_reference(self.item_section, name, target)

    def delete_all_references(self, name):
        self.reference_section.delete_all_references(self.item_section, name)

    def get_reference_sidepanel_text(self):
        return self.reference_section.get_reference_sidepanel_text()

    def close_ref_dialog(self):
        self.reference_section.close_dialog()

    # 공통
    def get_alert_message(self):
        return self.dialog.get_message()

    def close_alert_dialog(self):
        self.dialog.confirm()

    # assert
    def assert_alert_message(self, expected: str):
        actual = self.get_alert_message()
        assert expected in actual, f"[❌] 메시지 불일치\n기대한 값: {expected}\n실제 값: {actual}"

    def assert_reference_text(self, item_name: str, expected: str):
        self.search_and_select_item(item_name, dblclick=True)
        actual = self.get_reference_sidepanel_text()
        assert actual == expected, f"[❌] 참조 텍스트 불일치\n기대한 값: {expected}\n실제 값: {actual}"
