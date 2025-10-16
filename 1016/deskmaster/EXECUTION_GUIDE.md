# DeskMaster 실행 가이드 (Execution Guide)

## 1. 설치 (Installation)

### Python 의존성 설치
```bash
cd E:\VSC\1016\deskmaster
pip install -r requirements.txt
```

### Node.js 의존성 설치 (MCP 서버용)
```bash
npm install
```

### Tesseract OCR 설치
1. [Tesseract Windows installer](https://github.com/UB-Mannheim/tesseract/wiki) 다운로드
2. 설치 후 경로를 `.env` 파일에 추가:
```bash
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

## 2. 환경 설정 (Configuration)

### .env 파일 설정
`.env` 파일을 열어서 필수 값을 입력:

```bash
# 필수: Gemini API 키 (CAPTCHA 해결용)
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Chrome 경로 (기본값 사용 가능)
CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe

# Tesseract 경로 (설치 후 업데이트)
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

**Gemini API 키 발급 방법:**
1. https://makersuite.google.com/app/apikey 접속
2. "Create API Key" 클릭
3. 생성된 키를 `.env` 파일의 `GEMINI_API_KEY`에 입력

### config.yaml 확인
필요시 `config.yaml`에서 설정 조정:
- `review_range`: 리뷰 수 필터링 범위 (기본: 100-5000)
- `max_tabs_per_page`: 페이지당 최대 탭 수 (기본: 20)
- `max_total_tabs`: 전체 최대 탭 수 (기본: 25)

## 3. 실행 전 준비 (Pre-execution Setup)

### 필수 환경 요구사항
- **디스플레이 해상도**: 1920x1080 (필수)
- **Windows 배율**: 100% (필수)
- **Chrome 브라우저**: 최신 버전

### 수동 준비 단계
1. **Chrome 브라우저 열기**
2. **네이버 쇼핑 접속**: https://shopping.naver.com
3. **검색어 입력**: 원하는 상품 키워드 (예: "캠핑텐트")
4. **검색 실행**: Enter 키로 검색 결과 페이지로 이동
5. **프로그램 대기**: 검색 결과 페이지에서 프로그램 실행

## 4. 실행 (Execution)

### 기본 실행 (단일 키워드)
```bash
cd deskmaster
python src/main.py 캠핑텐트
```

### 여러 키워드 실행
```bash
cd deskmaster
python src/main.py 캠핑텐트 백팩 침낭
```

### 실행 시 동작
1. **환경 검증**: 디스플레이, Chrome 상태 확인
2. **프리셋 검증**: "리뷰 많은순", "80개 보기" 자동 적용
3. **페이지 스캔**:
   - 8-12회 랜덤 스크롤
   - 리뷰 100-5000 범위 상품 수집
   - 최대 20개 탭 자동 오픈
4. **탭 처리**:
   - 외부몰 자동 닫기
   - 내부몰만 유지
5. **CAPTCHA 처리**:
   - Gemini API 자동 해결 시도
   - 실패 시 수동 입력 대기
6. **다음 페이지**: 자동 이동 후 반복

## 5. 출력 결과 (Output)

### 로그 파일
```
logs/
└── deskmaster_YYYYMMDD_HHMMSS.jsonl
```

**로그 이벤트 예시:**
```json
{"timestamp": "2024-01-15T10:30:00", "event": "session_start", "keywords": ["캠핑텐트"]}
{"timestamp": "2024-01-15T10:30:05", "event": "preset_verify_start"}
{"timestamp": "2024-01-15T10:30:10", "event": "scan_start", "keyword": "캠핑텐트", "page": 1}
{"timestamp": "2024-01-15T10:30:45", "event": "candidate_found", "url": "...", "reviews": 523}
{"timestamp": "2024-01-15T10:31:00", "event": "tab_open", "keyword": "캠핑텐트", "page": 1, "index": 1}
```

### 스크린샷 (CAPTCHA 발생 시)
```
artifacts/
└── captcha_YYYYMMDD_HHMMSS.png
```

### Chrome 탭
- **내부몰 상품**: 열린 상태로 유지
- **외부몰 상품**: 자동으로 닫힘
- **리스트 페이지**: 첫 번째 탭에 유지

## 6. 동작 중 인터랙션 (Runtime Interaction)

### CAPTCHA 수동 입력
프로그램이 CAPTCHA를 자동으로 해결하지 못하면:

```
================================================================
⚠️  CAPTCHA 자동 해결 실패
================================================================
수동으로 CAPTCHA를 해결해주세요.
해결 후 아무 키나 누르면 계속됩니다...
================================================================

Press Enter to resume...
```

1. Chrome 창에서 CAPTCHA 입력
2. 터미널로 돌아와서 Enter 키 입력
3. 프로그램 자동 재개

### 중단 (Ctrl+C)
```bash
# 프로그램 중단
Ctrl + C

# 안전하게 종료됩니다:
# - MCP 서버 정리
# - 로그 파일 완료
# - 현재 상태 저장
```

## 7. 디버깅 (Debugging)

### 환경 검증 실패
```
Error: Display resolution is 1366x768, expected 1920x1080
```
**해결**: Windows 디스플레이 설정에서 1920x1080으로 변경

```
Error: Windows scaling is 125%, expected 100%
```
**해결**: Windows 디스플레이 설정에서 배율을 100%로 변경

### Chrome 연결 실패
```
Error: Could not connect to Chrome via UIA
```
**해결**:
1. Chrome 브라우저가 실행 중인지 확인
2. Chrome 창이 최대화되어 있는지 확인
3. Chrome 프로세스를 종료 후 재시작

### UIA 요소 찾기 실패
```
Error: Could not find element by name: '리뷰'
```
**해결**:
1. 네이버 쇼핑 검색 결과 페이지가 맞는지 확인
2. 페이지 로딩이 완료될 때까지 대기
3. Chrome UI 언어가 한국어인지 확인

### OCR 실패
```
Error: Tesseract not found
```
**해결**: Tesseract 설치 후 `.env`에서 `TESSERACT_CMD` 경로 확인

### Gemini API 오류
```
Error: Gemini API call failed
```
**해결**:
1. `.env` 파일에서 `GEMINI_API_KEY` 확인
2. API 키 할당량 확인
3. 네트워크 연결 확인

## 8. 성능 최적화 (Performance Tips)

### 빠른 실행
```yaml
# config.yaml 수정
list_scan:
  max_pages_per_keyword: 2  # 기본: 3

tabs:
  max_per_page: 10  # 기본: 20
```

### 더 많은 상품 수집
```yaml
# config.yaml 수정
list_scan:
  max_pages_per_keyword: 5  # 기본: 3

tabs:
  max_per_page: 30  # 기본: 20
  max_total: 50      # 기본: 25
```

### 리뷰 수 범위 조정
```yaml
# config.yaml 수정
review_range:
  min: 500   # 기본: 100
  max: 10000 # 기본: 5000
```

## 9. 트러블슈팅 체크리스트 (Troubleshooting Checklist)

실행 전 체크:
- [ ] Python 3.8+ 설치
- [ ] `pip install -r requirements.txt` 완료
- [ ] `npm install` 완료
- [ ] Tesseract OCR 설치
- [ ] `.env` 파일에 `GEMINI_API_KEY` 입력
- [ ] 디스플레이 해상도 1920x1080
- [ ] Windows 배율 100%
- [ ] Chrome 브라우저 실행 중
- [ ] 네이버 쇼핑 검색 결과 페이지 대기 중

실행 중 확인:
- [ ] 로그 파일 생성 확인 (`logs/` 디렉토리)
- [ ] Chrome 탭 자동 오픈 확인
- [ ] 외부몰 자동 닫힘 확인
- [ ] CAPTCHA 발생 시 수동 입력 준비

## 10. 예상 실행 시간 (Expected Runtime)

### 단일 키워드, 3페이지 기준
- **환경 검증**: ~5초
- **페이지당 스캔**: ~30-60초
  - 스크롤 (8-12회): ~20-40초
  - 탭 오픈 (최대 20개): ~10-20초
- **탭 처리**: ~10-30초
- **페이지 이동**: ~2-5초
- **총 예상 시간**: ~3-5분

### CAPTCHA 발생 시
- **자동 해결 시도**: ~10-30초 (최대 3회)
- **수동 입력 대기**: 사용자 입력 시간

### 여러 키워드
- **키워드당**: 위 시간 × 키워드 수

## 11. 고급 사용법 (Advanced Usage)

### 로그 분석
```bash
# 특정 이벤트 필터링
grep "candidate_found" logs/deskmaster_*.jsonl

# 탭 오픈 카운트
grep "tab_open" logs/deskmaster_*.jsonl | wc -l

# CAPTCHA 발생 횟수
grep "captcha_detected" logs/deskmaster_*.jsonl | wc -l
```

### 커스텀 설정 파일 사용
```bash
python src/main.py 캠핑텐트 --config custom_config.yaml
```

### 디버그 모드
```python
# src/main.py 수정
self.logger = HUDLogger(self.config.log_dir, debug=True)
```

---

## 빠른 시작 요약 (Quick Start Summary)

```bash
# 1. 설치
cd deskmaster
pip install -r requirements.txt

# 2. .env 설정
# GEMINI_API_KEY 입력

# 3. Chrome 준비
# - Chrome 브라우저 열기
# - 네이버 쇼핑 검색 결과 페이지로 이동

# 4. 실행
python src/main.py 캠핑텐트

# 5. 결과 확인
# - Chrome 탭: 내부몰 상품들
# - logs/: 로그 파일
# - artifacts/: 스크린샷 (CAPTCHA 시)
```

---

**문제 발생 시**: `COMPLETION_REPORT.md`의 "Known Limitations" 섹션 참조
