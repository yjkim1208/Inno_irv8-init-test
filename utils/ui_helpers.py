import ast
from playwright.sync_api import expect

def paste_to_cell(page, paste_text, target_cell):
    # 문자열 리터럴 안전 처리
    formatted_text = ast.literal_eval(f"'''{paste_text}'''")
    target_cell.wait_for(state="visible", timeout=3000)

    # 1. textarea 생성 및 값 설정
    page.evaluate(f"""
        () => {{
            const ta = document.createElement('textarea');
            ta.id = 'temp-clipboard';
            ta.style.position = 'fixed';
            ta.style.top = '0';
            ta.style.left = '0';
            ta.style.opacity = '0';
            ta.value = `{formatted_text}`;
            document.body.appendChild(ta);
            ta.focus();
            ta.select();
            document.execCommand('copy');  // <-- 명시적 복사
        }}
    """)

    # 2. textarea 제거
    page.evaluate("document.getElementById('temp-clipboard')?.remove()")

    # 3. 붙여넣기 수행
    safe_click(target_cell)
    page.keyboard.press("Control+V")

def wait_for_cell_in_iframe(page, td_selector: str, timeout=5000):
    iframe_element = page.locator("iframe").first
    frame = iframe_element.element_handle().content_frame()
    frame.locator(td_selector).first.wait_for(state="visible", timeout=timeout)
    return frame.locator(td_selector).first

def wait_until_button_disabled_in_iframe(page, button_id: str, timeout=5000):
    iframe = page.locator("iframe").first.element_handle().content_frame()
    button = iframe.locator(f"button#{button_id}")
    expect(button).to_have_attribute("disabled", "", timeout=timeout)

def safe_click(locator, timeout: int = 5000):
    locator.wait_for(state="visible", timeout=timeout)
    locator.click()

def safe_dblclick(locator, timeout: int = 5000):
    locator.wait_for(state="visible", timeout=timeout)
    locator.dblclick()


