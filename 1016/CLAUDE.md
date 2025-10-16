# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **DeskMaster MCP** project - a Windows UI Automation (UIA) based scanner for Naver Shopping price comparison pages. The system scans product listings, filters by review count, and identifies internal vs external mall products.

**Key Purpose**: Automated list-up scanner that opens qualifying products in background tabs, automatically closes external mall tabs, and keeps only internal mall (Smartstore) tabs.

## Critical Security Warning

⚠️ **IMMEDIATELY ADDRESS**: This repository currently contains sensitive credentials that must NOT be committed to version control:
- `jadong-471919-f2a4b145bd16.json` - Google Cloud service account private key
- `github_1_token.md` - GitHub personal access token

**Required Actions**:
1. Add these files to `.gitignore` immediately
2. Rotate/invalidate these credentials if already pushed to any remote
3. Store credentials in environment variables or secure vault instead

## Architecture

### Core Components

**Automation Stack**:
- **Windows UI Automation (UIA)**: Primary interaction method (no CDP/Playwright/Selenium)
- **Process-level Chrome control**: `chrome.exe --new-tab` for tab management
- **OCR Fallback**: Tesseract with `kor+eng` languages when UIA tree is insufficient
- **Gemini Vision API**: Automatic CAPTCHA solving with manual fallback

**Required MCP Servers**:
- `win-uia` - UIA element finding/interaction (invoke, scroll, set_value, back)
- `screen-grab` - Screen capture and cropping
- `ocr-tesseract` - Text recognition from screenshots
- `gemini-vision` - CAPTCHA solving
- `chrome-proc` - Chrome tab management via process commands
- `hud-logger` - Event logging and screenshot management

### Workflow Phases

1. **Environment Validation** (automatic)
   - Display: 1920×1080, 100% zoom, 100% display scale (primary monitor only)
   - Chrome: Maximized window with accessibility enabled
   - Presets: Auto-verify/apply "리뷰 많은순" (most reviews) + "80개 보기" (80 items)

2. **List Scanning** (automatic)
   - Scroll through price comparison listings (Tab 1 remains active)
   - Extract review counts via UIA tree or OCR fallback
   - Open qualifying products in new background tabs
   - Tab limits: 25 total, 20 per page, 3 pages per keyword

3. **Detail Tab Processing** (automatic)
   - Check each new tab for internal mall signals: "관심고객수", "관심 고객 수", "스토어 찜"
   - Keep internal mall tabs (smartstore.naver.com, brand.naver.com)
   - Close external mall tabs immediately
   - Block: aliexpress, 11st, gmarket, coupang, auction, taobao, tmall

4. **CAPTCHA Handling** (automatic + manual fallback)
   - Auto-detect CAPTCHA via UIA Name matching
   - Auto-solve via `node bin/captcha-solve.js` (Gemini Vision)
   - Max 3 attempts, confidence threshold: 0.6
   - On failure: Pause → manual operator solving → Resume

5. **Page Navigation** (automatic)
   - Navigation only within bottom pagination container (Role=navigation)
   - Random dwell times: 1200-3500ms, occasionally 5000-7000ms
   - OCR limited to bottom 20-25% ROI only

## Environment Variables

Required `.env` configuration:

```bash
# Required
GEMINI_API_KEY=AIza...              # For CAPTCHA solving
CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe

# Optional
CAPTCHA_SOLVER_CLI=node bin\captcha-solve.js
TESSERACT_PATH=...                  # If not in PATH
OCR_LANGS=kor+eng

# NEVER SET PROXY VARIABLES (direct connection only)
# HTTPS_PROXY - Must NOT be set
# HTTP_PROXY - Must NOT be set
```

**Keywords Configuration**:
```javascript
KEYWORDS: string[]  // Search terms
REVIEW_RANGE: {min: number, max: number}  // Review count filter
INTERNAL_SIGNALS: ["관심고객수", "관심 고객 수", "스토어 찜"]
ALLOWED_DOMAINS: ["smartstore.naver.com", "brand.naver.com", "shopping.naver.com"]
BLOCKED_DOMAINS: ["aliexpress", "11st", "gmarket", "coupang", "auction", "taobao", "tmall"]
```

## Prohibited Technologies

**Strictly Forbidden**:
- CDP (Chrome DevTools Protocol)
- Remote debugging ports
- Playwright/Selenium/browser automation libraries
- Physical keyboard/mouse input (cursor movement, typing simulation)
- Proxy servers (HTTPS_PROXY, HTTP_PROXY)
- Ctrl+F or any global search shortcuts

**Why**: To avoid detection and maintain human-like behavior patterns.

## Development Requirements

**System Prerequisites**:
- Windows OS (UIA is Windows-specific)
- Chrome browser with accessibility enabled (`chrome://accessibility`)
- Primary monitor: 1920×1080 resolution, 100% display scaling
- Node.js LTS (18/20+)
- Tesseract OCR installed with Korean + English language packs

**Chrome Launch Flags** (recommended):
```bash
--force-renderer-accessibility
--new-tab
--start-maximized
```

## Logging & Artifacts

**HUD Log Events** (JSON Lines format):
```
Common fields: ts, phase, event, keyword, page, tab, extra{}
```

Key events:
- `preset-verify(start|ok|retry|fail)` - Sorting/display preset validation
- `list-scan-start`, `candidate-found(method, reviews, idx)` - Scanning progress
- `open-new-tab(ok|fail)`, `tab-closed`, `tab-pruned` - Tab management
- `internal-signal-ok | internal-signal-missing` - Mall type detection
- `captcha-detected(type)`, `captcha-solve-ok`, `captcha-solve-fail` - CAPTCHA handling
- `pause`, `resume` - Manual intervention states
- `error(code, reason, recoverable)` - Error tracking

**Artifacts** (`artifacts/` directory):
- `viewport_<ts>.png` - Viewport screenshots during scanning
- `captcha_<ts>.png` - CAPTCHA images for solving/debugging
- `accepted_urls.csv` - Opened internal mall URLs with keywords

## Human-Like Behavior Patterns

**Randomization Requirements**:
- UIA operation delays: 90-300ms between calls
- Viewport dwell time: 400-700ms random
- Page transition: 1200-3500ms, occasionally 5000-7000ms
- Scroll patterns: Mix up/down micro-movements
- Navigation: Mix number clicks and "다음" (next) button

**Rate Limits**:
- 8-12 scroll passes per page
- 15-25 new tabs per page maximum
- 1-3 page navigations per keyword

## Code Style Conventions

The master prompt document (DeskMaster_MCP_Master_Prompt_v2.1.md) is written in Korean and serves as the authoritative specification. When implementing:

1. Use Korean variable names for domain concepts matching the specification
2. Maintain strict separation between UIA primary logic and OCR fallback
3. Always log via `hud.log` with structured event names from spec
4. Implement verification → application → re-verification loops for critical settings
5. Never mix UIA patterns with deprecated browser automation approaches

## Quality Acceptance Criteria

1. Products within `REVIEW_RANGE` open in new tabs; external malls close immediately
2. CAPTCHA auto-detection with logged solve attempts; auto-pause on failure
3. Page navigation only within bottom navigation container with randomized delays
4. Zero physical input - pure UIA/process commands
5. Preset validation (sorting + display count) logged at startup
6. Tab limit enforcement with `tab-pruned` events
7. OCR confidence tracking with fallback retries on low confidence

## Testing Considerations

Since this is a UI automation project:
- Test display scaling detection before any UIA operations
- Verify CAPTCHA detection without triggering real CAPTCHAs
- Mock `chrome.exe` process calls during unit tests
- Use screenshot fixtures for OCR testing
- Test tab counting and pruning logic independently

## Common Pitfalls

1. **Display scaling mismatch**: Code will abort if not 100% - verify before running
2. **Proxy environment variables**: Even if set in shell, code must ignore them
3. **Navigation scope**: Only search within pagination container, not full page
4. **OCR ROI**: Restrict to relevant card bounding boxes or bottom 20-25% for navigation
5. **Tab limits**: Must prune old external mall tabs first when hitting limits
6. **Internal signal timing**: Check after 2-second delay for slow-loading pages

## File Organization

- `DeskMaster_MCP_Master_Prompt_v2.1.md` - Authoritative Korean specification
- `.env` - Environment variables (create from template, never commit)
- `bin/captcha-solve.js` - CAPTCHA solver CLI (invoked by main automation)
- `logs/` - HUD event logs (JSON Lines)
- `artifacts/` - Screenshots and CSV exports

## Version & Maintenance

**Current Version**: v2.1 (as of specification document)

**Key v2.1 Changes** (inferred from prompt):
- Gemini Vision API fixed as CAPTCHA solver
- Preset verification → application → re-verification routine added
- Tab limit and pruning logic formalized
- Network proxy rules explicitly prohibited
- OCR confidence thresholds and multi-scale attempts
