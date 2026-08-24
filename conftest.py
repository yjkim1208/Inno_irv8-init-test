import pytest
from playwright.sync_api import sync_playwright
from pages.login_page.login import LoginPage
import os
import datetime
import pytest

# 최초 실행 실패 시 추가 재실행 횟수
MAX_RERUN_COUNT = 2

# 재실행 전 대기 시간(초)
RERUN_DELAY_SECONDS = 1

report_time = datetime.datetime.now().strftime("%Y%m%d_%H%M")
report_dir = "reports"
os.makedirs(report_dir, exist_ok=True)
txt_report_path = os.path.join(report_dir, f"test_report_{report_time}.txt")

def pytest_runtest_logreport(report):
    if report.when == "call":
        parts = report.nodeid.split("::")
        if len(parts) >= 3:
            test_id = f"{parts[1]} > {parts[2]}"
        else:
            test_id = " > ".join(parts[1:])

        outcome = report.outcome.upper()

        symbol = {
            "PASSED": "✔",
            "FAILED": "✖",
            "SKIPPED": "➖"
        }.get(outcome, "?")

        reason = ""
        if outcome == "FAILED":
            try:
                reason = str(report.longrepr.reprcrash.message)
            except Exception:
                reason = str(report.longrepr)
            line = f"{symbol} {test_id} - {outcome}: {reason}"
        else:
            line = f"{symbol} {test_id} - {outcome}"

        with open(txt_report_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")



# 실패 시 캡처용
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            try:
                # 새 탭까지 포함한 마지막 탭 캡처
                last_page = page.context.pages[-1]  # 가장 최근에 열린 탭
            except Exception:
                last_page = page

            # 페이지가 존재하는지, 이미 닫히지는 않았는지 먼저 확인
            if last_page and not last_page.is_closed():
                try:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    test_name = item.name.replace("/", "_")
                    screenshot_dir = "screenshots"
                    os.makedirs(screenshot_dir, exist_ok=True)

                    path = f"{screenshot_dir}/{test_name}_{timestamp}.png"
                    
                    last_page.screenshot(path=path, full_page=True)
                    print(f"\n📸 Screenshot saved: {path}")
                except Exception as e:
                    print(f"\n⚠️ 스크린샷 저장 실패 (페이지 오류): {e}")
            else:
                print("\n⚠️ 이미 페이지가 닫혀 있어 스크린샷을 건너뜁니다.")

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        # chromium
        # browser = p.chromium.launch(headless=False)
        # browser = p.chromium.launch(headless=False, slow_mo=500)

        # Chrome
        browser = p.chromium.launch(channel="chrome",headless=False)
        # browser = p.chromium.launch(channel="chrome",headless=False, slow_mo=500)

        # Edge 
        # browser = p.chromium.launch(channel="msedge", headless=False)
        # browser = p.chromium.launch(channel="msedge", headless=False, slow_mo=500)


        # Firefox
        # browser = p.firefox.launch(headless=True)
        # browser = p.firefox.launch(headless=False, slow_mo=500)

        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True,
        permissions=["clipboard-read", "clipboard-write"],
        locale="ko-KR",  # ✅ 한글 로케일 설정
            extra_http_headers={
                "Accept-Language": "ko-KR"  # ✅ HTTP 요청 시 언어 설정
        }
    )
    page = context.new_page()
    yield page
    context.close()

