# ─────────────────────────────────────────────
#IR

# BaseFolder 공통 Selectors
BASE_FOLDER_NAME_INPUT = "#in_add_biz_name"
BASE_FOLDER_ADD_LIST_BTN = "#btn_add_biz_list"
BASE_FOLDER_SAVE_BTN = "#btn_save_add_biz_list"
BASE_FOLDER_DELETE_RULE_BTN = "#btn_del_rule_in_biz"
BASE_FOLDER_FINAL_DELETE_BTN = "#btn_del_biz"
BASE_FOLDER_DUPLICATE_DIALOG_CONFIRM_BTN = "#ir_message >> role=button[name='확인']"
BASE_FOLDER_POPUP_CLOSE_BTN = "#div_add_biz_pop .dialog__button-close"
BASE_FOLDER_TREEITEM_ROLE = "treeitem"
BASE_FOLDER_DELETE_BTN_NAME = "폴더 삭제"

# TopFolder 전용
TOP_FOLDER_ADD_BTN = "#btn_add_biz_top"

# Folder 전용
FOLDER_LIST_AREA = "#bizList"
FOLDER_ADD_BTN_NAME = "폴더 추가"
FOLDER_RENAME_BTN_NAME = "폴더 이름 변경"
FOLDER_RENAME_INPUT = "#in_modify_biz_name"
FOLDER_RENAME_SAVE_BTN = "#btn_save_modify_biz"
FOLDER_NAME_DUPLICATE_POPUP_CLOSE = "#st_modify_biz_name >> xpath=../../.. >> .dialog__button-close"

# ItemPage 관련 Selectors
ITEM_MANAGE_BUTTON = "항목 관리"
ITEM_ADD_BUTTON = "#btn_add_item"
ITEM_SAVE_BUTTON = "#btn_save_item"
ITEM_SEARCH_BOX = "#in_keyword"
ITEM_SEARCH_BUTTON = "#btn_search_item"
ITEM_NAME_CELL = "td[data-row='1'][data-col='3']"
ITEM_RENAME_BUTTON = "#btn_modify_item"
ITEM_DELETE_BUTTON = "#btn_delete_item"
ITEM_CONFIRM_BUTTON = "#btn_save_item"
ITEM_ALERT_OK_BUTTON = "#ir_message >> role=button[name='확인']"
ITEM_POPUP_CLOSE_BUTTON = "#st_item_top >> xpath=../../.. >> .dialog__button-close"
ITEM_POPUP_DIALOG_CLOSE_BTN = "#st_item_top >> xpath=../../.. >> .dialog__button-close"  

# 참조값
REF_MANAGE_BUTTON_NAME = "참조값 관리"  
REF_EDIT_BUTTON = "#btn_edit_ref"
REF_GRID_CELL = "#div_refGrid td[data-row='1'][data-col='1']"
REF_GRID_CONTAINER = "#div_refGrid"  
REF_DELETE_ROW_BUTTON = "#btn_ref_delete_row"
REF_SAVE_BUTTON = "button:has-text('저장')"
REF_DIALOG_CLOSE_BTN = "#st_ref_top >> xpath=../../.. >> .dialog__button-close"
REF_SIDE_PANEL_ROWS = "#div_ref_list tr[data-row]"

# 검색 결과 셀
ITEM_GRID_ROW = "#div_item_list_table td[data-col='1'] span"

# RulePage 관련 Selectors
RULE_BTN_ADD = "#btn_add_rule_top"
RULE_BTN_CONFIRM = "#btn_save"
RULE_INPUT_NAME = "input#in_rule_name"
RULE_RETURN_CELL = "#div_addrule_grid td[data-row='1'][data-col='1']"
RULE_DELETE_CHECKBOXES = "#div_addrule_grid td[data-col='4'] input[type='checkbox']"
RULE_RADIO_SINGLE_RETURN = "input#in_returngb_s"
RULE_RADIO_MULTI_RETURN = "span#sp_returngb_m"
RULE_TREE_ITEMS = "#ruleTree >> role=treeitem"
RULE_ADD_POPUP = "div.dialog__wrapper >> text=룰 추가"
RULE_ADD_POPUP_CLOSE_BTN = "div.dialog__wrapper button.dialog__button-close"
RULE_ERROR_CONFIRM_BTN = "#ir_message >> role=button[name='확인']"
RULE_ADD_POPUP_TITLE = "룰 추가"
RULE_ADD_POPUP_CLOSE_BTN = "button.dialog__button-close"
RULE_ADD_POPUP_WRAPPER = "div.dialog__wrapper"



# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
#PF

# === 메뉴 버튼 이름 ===
BTN_MENU_TYPE_MGMT_NAME = "유형관리"
BTN_MANAGEMENT_TYPE_NAME = "관리유형 등록/수정"

# DetailType 관련 Selectors
DETAIL_TYPE_ADD_BTN = "button:has-text('세부유형추가')"
DETAIL_TYPE_SAVE_BTN = "#btnSaveDType"
DETAIL_TYPE_DELETE_BTN = "#btnDelDType"
DETAIL_TYPE_GRID_ID = "#jgriddtype"
DETAIL_TYPE_GRID_XPATH = '//*[@id="jgriddtype"]/div/table/div[2]'
DETAIL_TYPE_NAME_CELL_SELECTOR = "td[data-col='2']"

# GroupType 관련 Selectors
GROUP_TYPE_ADD_BTN = "button[data-key='btn-add'][data-i18n='btnAddGType']"
GROUP_TYPE_SAVE_BTN = "#btnSave"
GROUP_TYPE_DELETE_BTN = "#btnDel"
GROUP_TYPE_GRID_XPATH = '//*[@id="jgridgrpmember"]/div/table/div[2]'
GROUP_TYPE_NAME_CELL_SELECTOR = "td[data-col='1']"
GROUP_TYPE_GRID_AREA = "#jgridgrpmemberarea"
GROUP_GRID_SELECTOR = "#jgridgrouparea"

# GroupType 관련 Selectors
OBJECT_GROUP_ADD_BTN = "button:has-text('그룹추가')"
OBJECT_GROUP_SAVE_BTN = "button:has-text('그룹저장')"
OBJECT_GROUP_DELETE_BTN = "button:has-text('그룹삭제')"
OBJECT_GROUP_GRID_SELECTOR = "#jgridgrouparea"

# ObjectType 관련 Selectors
OBJECT_TYPE_ADD_BTN = "button[data-key='btn-add'][data-i18n='btnAddType']"
OBJECT_TYPE_SAVE_BTN = "button[data-key='btn-save'][data-i18n='btnSaveType']"
OBJECT_TYPE_DELETE_BTN = "#btnDelType"
OBJECT_TYPE_CODE_RULE_SAVE_BTN = "div#coderule.dialog.is-visible >> button:has-text('저장')"
OBJECT_TYPE_GRID_SELECTOR = "#jgridtypearea"
OBJECT_TYPE_CODE_RULE_DIALOG = "div#coderule.dialog.is-visible"
OBJECT_TYPE_CODE_RULE_CELL = "[data-row='1'][data-col='1']"

# RelationType 관련 Selectors
BTN_MENU_TYPE_MGMT_NAME = "유형관리"
BTN_RELATION_TYPE_PAGE_NAME = "관계유형 등록/수정"
BTN_ADD_ROW_NAME = "행추가"
BTN_RELATION_SAVE_NAME = "관계저장"
GRID_RELATION_TABLE_XPATH = '//*[@id="right"]/div/div[2]/div/div[1]/div/table'
RELATION_DIALOG_CONTENT_SELECTOR = "div.dialog__content div.css-gmrzsa45 span"
RELATION_DELETE_BTN_SELECTOR = "button:has-text('행삭제')"

# ─────────────────────────────────────────────


# ─────────────────────────────────────────────
# 공통 

#  공통 버튼 텍스트
BTN_TEXT_YES = "예"
BTN_TEXT_NO = "아니오"
BTN_TEXT_CONFIRM = "확인"
BTN_TEXT_SAVE = "저장"

#  Dialog 관련 Selectors
DIALOG_MESSAGE_SELECTOR = "div.dialog__content div[class*='css-gmrzsa45']"
DIALOG_CONFIRM_BTN_SELECTOR = "div.dialog__content button.button--primary"
IFRAME_DIALOG_MESSAGE_SELECTOR = "div.dialog__content div.css-gmrzsa45 span"

#  로그인 관련 Selectors
LOGIN_BTN_TEXT = "로그인"
INNOPRODUCT_BTN_NAME = "InnoProduct InnoProduct"
INNORULES_BTN_NAME = "InnoRules InnoRules"
INPUT_ID_SELECTOR = "#err-input-id"
INPUT_PW_SELECTOR = "#err-input-pw"
ERROR_TOAST_SELECTOR = "div.toast-item--error span.ir-flex-1"

#  Grid / 테이블
ROW_TEXT_FOR_ADD = "추가"

#  팝업 / 포버
POPOVER_CONTAINER = "#ir_popover"

#  개행 문자
TAB = "\\t"
NEWLINE = "\\n"

