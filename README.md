# 🚀 자동화 테스트 파일럿 프로젝트

> **Playwright**와 **Pytest**를 기반으로 작성된 InnoRules UI 자동화 테스트 파일럿 프로젝트입니다.

기능별 Page Object와 테스트 코드를 분리하고, Oracle DB에서 테스트 데이터를 불러와 테스트를 수행합니다.

테스트 케이스의 주요 검증 결과는 스크린샷으로 저장하여 테스트 수행 증빙과 실패 원인 분석에 활용합니다.

---

## 🛠️ 실행 방법

### 1. 가상환경 생성 및 활성화

가상환경 생성:

```bash
python -m venv pilot_venv
```

가상환경 활성화(Windows PowerShell):

```powershell
.\pilot_venv\Scripts\Activate
```

가상환경 활성화(Windows CMD):

```cmd
pilot_venv\Scripts\activate
```

가상환경 활성화(Mac/Linux):

```bash
source pilot_venv/bin/activate
```

### 2. 라이브러리 설치

```bash
python -m pip install -r requirements.txt
```

### 3. Playwright 전용 브라우저 설치

```bash
python -m playwright install
```

### 4. `.env` 파일 설정

프로젝트 루트에 `.env` 파일을 생성하고 테스트 환경에 맞는 정보를 설정합니다.

작성 항목은 `.env_example` 파일을 참고합니다.

주요 환경변수는 다음과 같습니다.

```text
DB_HOST
DB_PORT
DB_USER
DB_PASSWORD
DB_SERVICE_NAME
TARGET_URL
```


### 5. 테스트 실행

전체 테스트 실행:

```bash
python -m pytest -v -s
```

영역별 테스트 전체 실행:

```bash
python -m pytest tests/[폴더] -v -s
```

특정 테스트 파일 실행:

```bash
python -m pytest tests/item/[AUTO_IR8_TC_*].py -v -s
```

---

## 📂 프로젝트 구조

```text
irv8-init-test/
├─ pages/
│  ├─ components/
│  ├─ login/
│  ├─ user/
│  ├─ folder/
│  └─ item/
├─ tests/
│  ├─ login/
│  ├─ user/
│  ├─ folder/
│  └─ item/
├─ utils/
├─ artifacts/
│  ├─ user/
│  ├─ folder/
│  └─ item/
├─ screenshots/
├─ reports/
├─ conftest.py
├─ requirements.txt
└─ .env

```

| 경로                  | 설명                                      |
| ------------------- | --------------------------------------- |
| `pages/`            | 화면별 Page Object와 UI 동작 함수               |
| `pages/components/` | 다이얼로그 등 여러 화면에서 사용하는 공통 컴포넌트            |
| `tests/`            | 기능 및 시나리오별 자동화 테스트 케이스                  |
| `utils/`            | DB 연결, 테스트 데이터 조회, UI helper 및 selector |
| `artifacts/`        | 테스트 케이스의 주요 검증 결과 스크린샷                  |
| `screenshots/`      | 테스트 실패 시 생성되는 디버깅용 스크린샷                 |
| `reports/`          | 설정된 경우 생성되는 테스트 실행 결과 리포트               |
| `conftest.py`       | pytest 공통 fixture 및 테스트 실행 설정           |
| `.env`      | 환경변수 설정                              |
| `requirements.txt`  | 테스트 실행에 필요한 Python 라이브러리 목록             |


## 🗃️ 테스트 데이터 관리

### 테스트 케이스 관리 페이지

[테스트 케이스 관리 페이지](https://172.16.21.10:55802/test-case-manager/cases)

테스트 케이스 관리 페이지는 Oracle DB의 테스트 데이터와 연동된 내부 도구입니다.


### 테스트 데이터 테이블 구분

| 테이블                | 관리 페이지 선택 항목  | 용도                          | 
| ------------------ | ------------- | --------------------------- | 
| `TestCaseMain`     | 테스트 케이스 기본 정보 | 테스트 케이스 ID와 기본 정보 관리        | 
| `TestCaseData`     | 일반 데이터        | 그리드 형태가 아닌 일반 입력 데이터 관리     | 
| `GridTestCaseData` | 그리드 데이터       | 여러 컬럼 또는 여러 행으로 구성되는 데이터 관리 | 


## 📸 테스트 결과 및 스크린샷 관리

자동화 테스트의 주요 검증 결과를 확인할 수 있도록 단계별 화면을 스크린샷으로 저장합니다.

| 경로             | 용도                              |
| -------------- | ------------------------------- |
| `artifacts/`   | 테스트 케이스의 정상 수행 결과를 증빙하기 위한 스크린샷 |
| `screenshots/` | 테스트 실패 원인을 분석하기 위한 디버깅용 스크린샷    |


## 📚 참고 문서

자동화 테스트 케이스는 표준화 기준, 테스트 시나리오, 기능별 우선순위 및 개발 일정을 참고하여 작성합니다.

### 1. 자동화 테스트 표준화 대상

[자동화 테스트 표준화 대상 문서](https://docs.google.com/spreadsheets/d/1Tp1HKJXLxmevfnqpiFq4O-NruIeRF4Tzvg_V8ig449w/edit?gid=0#gid=0)

자동화 코드와 테스트 데이터를 일관된 형태로 관리하기 위한 표준화 기준 문서입니다.

### 2. 테스트 시나리오 및 테스트 케이스

[테스트 시나리오 및 테스트 케이스 문서](https://docs.google.com/spreadsheets/d/180Km6wn_Os35FXEKkSaO0OpsIyDoxgvjqE12ckhQXy0/edit?gid=65831526#gid=65831526)

제품 기능별 테스트 시나리오와 상세 테스트 케이스를 관리하는 문서입니다.


### 3. 자동화 테스트 개발 일정

[자동화 테스트 개발 일정 문서](https://docs.google.com/spreadsheets/d/19wLb1S4cQsBvtqStAtZGqpE8r2xDNv-wS0i0G7KAoOw/edit?gid=1954857101#gid=1954857101)

자동화 개발 범위와 진행 일정을 관리하는 문서입니다.

