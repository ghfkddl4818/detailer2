# DeskMaster 설치 가이드

## 단계별 설치

### 1. Python 환경 준비

Python 3.8 이상이 설치되어 있어야 합니다.

```bash
# Python 버전 확인
python --version

# pip 업그레이드
python -m pip install --upgrade pip
```

### 2. 프로젝트 다운로드

```bash
cd E:\VSC\1016
# 이미 deskmaster 폴더가 있음
```

### 3. Python 패키지 설치

```bash
cd deskmaster
pip install -r requirements.txt
```

설치되는 패키지:
- `mcp-ocr` - Tesseract OCR MCP 서버
- `google-generativeai` - Gemini API
- `pywinauto` - Windows UI Automation
- `pytesseract` - Tesseract Python wrapper
- `pyyaml` - YAML 설정 파일
- `python-dotenv` - 환경 변수 관리

### 4. Node.js MCP 서버 설치

```bash
# Node.js 버전 확인 (18+ 필요)
node --version

# MCP 서버 설치
npm install
npm run install-mcp-servers
```

설치되는 MCP 서버:
- **mcp-windows-desktop-automation**: Windows UIA 제어
  - 위치: `mcp-servers/mcp-windows-desktop-automation/`
  - 빌드 완료 후 사용 가능

- **mcp-server-gemini**: Gemini Vision API
  - npx로 실행 (자동 다운로드)

- **mcp-ocr**: Tesseract OCR
  - Python 패키지로 설치됨

### 5. 환경 변수 설정

`.env` 파일이 이미 생성되어 있습니다. Gemini API Key만 입력하세요:

```bash
# .env 파일 열기
notepad .env
```

**필수 입력:**
```
GEMINI_API_KEY=AIza...  # 여기에 실제 Gemini API Key 입력
```

### 6. Gemini API Key 발급

1. https://aistudio.google.com/app/apikey 접속
2. "Get API key" 클릭
3. 새 API 키 생성
4. `.env` 파일에 붙여넣기

### 7. Tesseract 경로 확인

Tesseract가 `E:\tesseract\tesseract.exe`에 설치되어 있는지 확인:

```bash
E:\tesseract\tesseract.exe --version
```

출력 예시:
```
tesseract 5.x.x
```

만약 다른 위치라면 `config.yaml` 수정:

```yaml
ocr:
  tesseract_path: "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # 실제 경로로 변경
```

### 8. Chrome 경로 확인

Chrome이 기본 경로에 설치되어 있는지 확인:

```bash
dir "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

다른 위치라면 `config.yaml` 수정:

```yaml
chrome:
  path: "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"  # 실제 경로
```

### 9. 디스플레이 설정 확인

**필수 설정:**

1. **디스플레이 해상도**: 1920×1080
   - 설정 → 시스템 → 디스플레이 → 해상도

2. **디스플레이 배율**: 100%
   - 설정 → 시스템 → 디스플레이 → 배율 및 레이아웃 → **100% (권장)**

3. **다중 모니터**: 주 모니터에서만 실행
   - 설정 → 시스템 → 디스플레이 → 주 디스플레이 선택

4. **Chrome 줌**: 100%
   - Chrome에서 Ctrl+0 (줌 리셋)

⚠️ 위 조건 불일치 시 프로그램 자동 중단

### 10. Chrome 접근성 활성화 (권장)

```
chrome://accessibility
```

"접근성 모드 활성화" 클릭

### 11. 설치 확인

```bash
# Python 패키지 확인
python -c "import mcp_ocr; import google.generativeai; import pywinauto; print('OK')"

# Node MCP 서버 확인
dir mcp-servers\mcp-windows-desktop-automation\build\index.js

# Gemini API Key 확인
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OK' if os.getenv('GEMINI_API_KEY') else 'FAIL')"
```

모두 "OK" 출력되면 설치 완료!

## 테스트 실행

### 간단한 테스트

```bash
cd E:\VSC\1016\deskmaster
python src/main.py 테스트
```

### 실제 사용 테스트

1. Chrome 열기
2. 네이버 쇼핑 접속: https://shopping.naver.com/
3. 검색창에 "캠핑텐트" 입력
4. 검색 결과에서 "가격비교" 탭 클릭
5. 프로그램 실행:

```bash
python src/main.py 캠핑텐트
```

6. 로그 확인:

```bash
dir logs
type logs\deskmaster_*.jsonl
```

## 문제 해결

### pip install 오류

```
error: Microsoft Visual C++ 14.0 is required
```

**해결:** https://visualstudio.microsoft.com/downloads/ 에서 "Build Tools for Visual Studio" 설치

### npm install 오류

```
error: ENOENT: no such file or directory
```

**해결:** Node.js 재설치 후 재시도

### MCP 서버 빌드 오류

```bash
cd mcp-servers/mcp-windows-desktop-automation
npm install
npm run build
```

### Tesseract 언어팩 누락

```
error: Error opening data file
```

**해결:** Tesseract 재설치 시 한국어 언어팩 선택

### Gemini API 오류

```
error: 401 Unauthorized
```

**해결:**
1. API Key 재확인
2. https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com 에서 API 활성화

## 다음 단계

설치 완료 후 [README.md](README.md)의 "사용 방법" 섹션 참고.
