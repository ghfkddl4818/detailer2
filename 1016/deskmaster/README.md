# DeskMaster MCP

Windows UI Automation 기반 네이버 쇼핑 가격비교 리스트업 자동화 시스템.

## 개요

DeskMaster는 네이버 쇼핑 가격비교 페이지에서 리뷰 수 범위에 부합하는 상품을 자동으로 스캔하여 백그라운드 탭으로 쌓고, 내부몰(스마트스토어)만 유지하는 자동화 프로그램입니다.

### 주요 기능

- ✅ **UIA 기반 리스트 스캔** - Windows UI Automation으로 봇 탐지 회피
- ✅ **리뷰 수 필터링** - 설정된 범위(기본 100-5000) 자동 필터
- ✅ **백그라운드 탭 생성** - `chrome.exe --new-tab`으로 탭 쌓기
- ✅ **내부몰/외부몰 구분** - 관심고객수 시그널 자동 탐지
- ✅ **외부몰 자동 닫기** - 11st, 쿠팡 등 외부몰 탭 즉시 제거
- ✅ **Gemini 캡차 자동 해결** - Vision API로 캡차 자동 풀이
- ✅ **휴먼라이크 동작** - 랜덤 딜레이 및 스크롤 패턴

### 금지 기술

❌ CDP (Chrome DevTools Protocol)
❌ Playwright / Selenium
❌ 원격 디버깅 포트
❌ 물리 키보드/마우스 입력
❌ 프록시

## 시스템 요구사항

### 필수

- **Windows 10/11** (UIA 필수)
- **Chrome 브라우저** (최신 버전)
- **Python 3.8+**
- **Node.js 18+**
- **Tesseract OCR** (E:\tesseract에 설치됨)
- **Gemini API Key**

### 디스플레이 요구사항

- 해상도: **1920×1080** (필수)
- 디스플레이 스케일: **100%** (필수)
- Chrome 줌: **100%** (필수)
- Chrome 창: **최대화** (필수)

⚠️ 위 조건 불일치 시 프로그램 자동 중단

## 설치

### 1. Python 패키지 설치

```bash
cd deskmaster
pip install -r requirements.txt
```

### 2. MCP 서버 설치

```bash
npm install
npm run install-mcp-servers
```

설치되는 MCP 서버:
- `mcp-windows-desktop-automation` - Windows UIA 제어
- `mcp-server-gemini` - Gemini Vision API
- `mcp-ocr` - Tesseract OCR

### 3. 환경 변수 설정

`.env` 파일에 Gemini API Key 입력:

```bash
GEMINI_API_KEY=AIza...
```

### 4. Tesseract 경로 확인

`config.yaml`에서 Tesseract 경로 확인:

```yaml
ocr:
  tesseract_path: "E:\\tesseract\\tesseract.exe"
```

## 사용 방법

### 1. 수동 준비

1. Chrome 브라우저 열기
2. 네이버 쇼핑 가격비교 페이지 접속
3. 키워드 검색 (예: "캠핑텐트")
4. 프로그램 실행 ← **여기서부터 자동화**

### 2. 프로그램 실행

```bash
cd deskmaster
python src/main.py 캠핑텐트 백팩 등산화
```

키워드를 공백으로 구분하여 여러 개 입력 가능.

### 3. 자동화 시작

프로그램이 자동으로:
1. 환경 검증 (해상도, 스케일, 줌)
2. 정렬/표시 프리셋 확인 ("리뷰 많은순", "80개 보기")
3. 리스트 스캔 시작 (8-12회 랜덤 스크롤)
4. 조건 맞는 상품 → 백그라운드 탭 오픈
5. 각 탭 확인 → 내부몰 유지, 외부몰 닫기
6. 캡차 감지 시 Gemini로 자동 해결
7. 페이지 이동 (최대 3페이지)

### 4. 결과 확인

**탭 구조:**
- **탭1**: 가격비교 리스트 (그대로 유지)
- **탭2~N**: 내부몰 상세페이지 (리스트업 결과)

**로그 확인:**
```bash
cd logs
type deskmaster_<timestamp>.jsonl
```

**스크린샷 확인:**
```bash
cd artifacts
dir
```

## 설정

### config.yaml

주요 설정 항목:

```yaml
# 리뷰 범위 필터
review_range:
  min: 100
  max: 5000

# 탭 제한
chrome:
  max_tabs_total: 25
  max_tabs_per_page: 20

# 내부몰 시그널
internal_signals:
  - "관심고객수"
  - "관심 고객 수"
  - "스토어 찜"

# 허용 도메인 (내부몰)
allowed_domains:
  - "smartstore.naver.com"
  - "brand.naver.com"

# 차단 도메인 (외부몰)
blocked_domains:
  - "11st"
  - "gmarket"
  - "coupang"
  - "aliexpress"

# 캡차 설정
captcha:
  enabled: true
  auto_solver:
    enabled: true
    provider: "gemini"
    max_attempts: 3
  min_confidence: 0.6
```

## 로그 이벤트

HUD 로그는 JSON Lines 형식으로 `logs/` 디렉토리에 저장됩니다.

### 주요 이벤트

```jsonl
{"ts": "2025-01-15T10:00:00", "event": "session-start"}
{"ts": "2025-01-15T10:00:01", "event": "preset-verify", "phase": "ok", "extra": {"type": "sorting"}}
{"ts": "2025-01-15T10:00:05", "event": "list-scan-start", "keyword": "캠핑텐트", "page": 1}
{"ts": "2025-01-15T10:00:08", "event": "candidate-found", "keyword": "캠핑텐트", "page": 1, "extra": {"method": "uia", "reviews": 1234, "idx": 5}}
{"ts": "2025-01-15T10:00:09", "event": "open-new-tab-ok", "keyword": "캠핑텐트", "page": 1, "extra": {"url": "https://..."}}
{"ts": "2025-01-15T10:00:12", "event": "detail-check-start", "tab": 2, "extra": {"url": "https://..."}}
{"ts": "2025-01-15T10:00:13", "event": "internal-signal-ok", "tab": 2, "extra": {"signal": "관심고객수"}}
{"ts": "2025-01-15T10:00:20", "event": "internal-signal-missing", "tab": 3}
{"ts": "2025-01-15T10:00:20", "event": "tab-closed", "tab": 3, "extra": {"reason": "external-mall"}}
{"ts": "2025-01-15T10:01:00", "event": "captcha-detected", "extra": {"type": "text"}}
{"ts": "2025-01-15T10:01:05", "event": "captcha-solve-ok", "extra": {"confidence": 0.85}}
{"ts": "2025-01-15T10:05:00", "event": "session-end", "extra": {"total_tabs": 21, "internal_count": 18}}
```

## 문제 해결

### 환경 검증 실패

```
error(display-scale-mismatch)
```

**해결:** Windows 설정 → 디스플레이 → 배율을 100%로 변경

### MCP 서버 시작 실패

```
error(mcp-server-start-failed)
```

**해결:**
```bash
npm run install-mcp-servers
```

### Tesseract 오류

```
error(tesseract-not-found)
```

**해결:** `config.yaml`에서 `tesseract_path` 확인

### Gemini API 오류

```
error(gemini-api-key-missing)
```

**해결:** `.env` 파일에 `GEMINI_API_KEY` 입력

### 캡차 자동 해결 실패

```
event: pause, reason: captcha-auto-solve-failed
```

**해결:** 수동으로 캡차 입력 후 프로그램 재실행

## 개발 상태

### ✅ 완료

- 프로젝트 구조 및 설정
- HUD 로거 (JSON Lines)
- Chrome 프로세스 관리
- MCP 클라이언트 인터페이스
- 핵심 모듈 구조 (Scanner, TabProcessor, CaptchaSolver)
- 메인 오케스트레이터 워크플로우

### 🚧 구현 필요 (TODO)

- **UIA 통합**: Windows UI Automation 실제 연동
  - 요소 탐색 (ListItem, Name 속성)
  - 클릭/스크롤/텍스트 입력
  - 탭 카운트 및 제어
- **OCR 폴백**: 화면 캡처 및 Tesseract 처리
- **페이지 네비게이션**: 하단 페이징 UIA 탐색
- **환경 검증**: 해상도/스케일/줌 자동 체크
- **Pause/Resume**: 캡차 수동 해결 대기 메커니즘

## 라이센스

MIT

## 참고 문서

- [DeskMaster_MCP_Master_Prompt_v2.1.md](../DeskMaster_MCP_Master_Prompt_v2.1.md) - 상세 사양서
- [CLAUDE.md](../CLAUDE.md) - Claude Code 가이드
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP 공식 문서
