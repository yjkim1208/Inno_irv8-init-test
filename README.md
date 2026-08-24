
```markdown

# 🚀 자동화 테스트 파일럿 프로젝트

  

>  **Playwright**와 **Pytest**를 기반으로 작성된 자동화 테스트 파일럿 프로젝트입니다.


## 🛠️ 실행 방법 (Setup & Execution)
  

### 1. 가상환경 생성 및 활성화

```bash

# 가상환경 생성

python  -m  venv  pilot_venv

  

# 가상환경 활성화 (Windows)

.\pilot_venv\Scripts\activate

  

# 가상환경 활성화 (Mac/Linux)

source  pilot_venv/bin/activate

  

```

  

### 2. 라이브러리 설치

  

```bash

pip  install  -r  requirements.txt

```

  

### 3. Playwright 전용 브라우저 설치
  

```bash

playwright  install

```

  

### 4. .env 파일 설정

  

프로젝트 루트에 `.env` 파일을 생성하고 연결할 DB 환경에 맞춰 설정하세요.

  

*  **참고:**  `.env_example` 파일 참고.

*  **주요 항목:**  `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `TARGET_URL` 등

  

### 5. 테스트 실행

  

```bash

# 터미널에서 실행 시

pytest

# 또는 VS Code 좌측 '테스트(Test Explorer)' 탭 활용 (Python/Playwright 확장 프로그램 필요)

```

  

---

  

## 📂 폴더 구조 설명

  

| 폴더명 | 설명 |

| **pages/** | 페이지 오브젝트 모델(POM) 클래스 정의 |

| **tests/** | 시나리오별 실제 테스트 케이스 코드 |

| **utils/** | DB 연결 및 공통 유틸리티 함수 |

| **reports/** | 테스트 결과 리포트 (실행 후 자동 생성) |

| **screenshots/** | 테스트 실패 시 스크린샷 저장 (실행 후 자동 생성) |

 
