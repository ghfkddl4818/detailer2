"""HUD Logger - JSON Lines event logging system."""
import json
import datetime
from pathlib import Path
from typing import Any, Dict, Optional

class HUDLogger:
    """JSON Lines logger for DeskMaster events."""

    def __init__(self, log_dir: Path):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Create log file with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"deskmaster_{timestamp}.jsonl"

        # Initialize log file
        self._log_event("session-start", extra={"log_file": str(self.log_file)})

    def _log_event(
        self,
        event: str,
        phase: Optional[str] = None,
        keyword: Optional[str] = None,
        page: Optional[int] = None,
        tab: Optional[int] = None,
        extra: Optional[Dict[str, Any]] = None
    ):
        """Write event to JSON Lines log."""
        log_entry = {
            "ts": datetime.datetime.now().isoformat(),
            "event": event,
        }

        if phase:
            log_entry["phase"] = phase
        if keyword:
            log_entry["keyword"] = keyword
        if page is not None:
            log_entry["page"] = page
        if tab is not None:
            log_entry["tab"] = tab
        if extra:
            log_entry["extra"] = extra

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    # Preset verification events
    def preset_verify_start(self):
        self._log_event("preset-verify", phase="start")

    def preset_verify_ok(self, preset_type: str):
        self._log_event("preset-verify", phase="ok", extra={"type": preset_type})

    def preset_verify_retry(self, preset_type: str, attempt: int):
        self._log_event("preset-verify", phase="retry", extra={"type": preset_type, "attempt": attempt})

    def preset_verify_fail(self, preset_type: str):
        self._log_event("preset-verify", phase="fail", extra={"type": preset_type})

    # List scanning events
    def list_scan_start(self, keyword: str, page: int):
        self._log_event("list-scan-start", keyword=keyword, page=page)

    def candidate_found(self, method: str, reviews: int, idx: int, keyword: str, page: int):
        self._log_event("candidate-found", keyword=keyword, page=page,
                       extra={"method": method, "reviews": reviews, "idx": idx})

    def open_new_tab(self, success: bool, url: str, keyword: str, page: int):
        status = "ok" if success else "fail"
        self._log_event(f"open-new-tab-{status}", keyword=keyword, page=page, extra={"url": url})

    # Tab management events
    def tab_limit_hit(self, total_tabs: int, max_allowed: int):
        self._log_event("tab-limit-hit", extra={"total": total_tabs, "max": max_allowed})

    def tab_pruned(self, count: int):
        self._log_event("tab-pruned", extra={"count": count})

    # Detail page events
    def detail_check_start(self, tab: int, url: str):
        self._log_event("detail-check-start", tab=tab, extra={"url": url})

    def internal_signal_found(self, tab: int, signal: str):
        self._log_event("internal-signal-ok", tab=tab, extra={"signal": signal})

    def internal_signal_missing(self, tab: int):
        self._log_event("internal-signal-missing", tab=tab)

    def tab_closed(self, tab: int, reason: str):
        self._log_event("tab-closed", tab=tab, extra={"reason": reason})

    # Page navigation events
    def page_move_attempt(self, page: int, target: int):
        self._log_event("page-move", phase="attempt", page=page, extra={"target": target})

    def page_move_ok(self, page: int):
        self._log_event("page-move", phase="ok", page=page)

    def page_move_fail(self, page: int, reason: str):
        self._log_event("page-move", phase="fail", page=page, extra={"reason": reason})

    def page_wait(self, ms: int):
        self._log_event("page-wait", extra={"ms": ms})

    # CAPTCHA events
    def captcha_detected(self, captcha_type: str):
        self._log_event("captcha-detected", extra={"type": captcha_type})

    def captcha_solve_start(self, provider: str):
        self._log_event("captcha-solve-start", extra={"provider": provider})

    def captcha_solve_ok(self, confidence: float):
        self._log_event("captcha-solve-ok", extra={"confidence": confidence})

    def captcha_solve_fail(self, reason: str, attempt: int):
        self._log_event("captcha-solve-fail", extra={"reason": reason, "attempt": attempt})

    def pause(self, reason: str):
        self._log_event("pause", extra={"reason": reason})

    def resume(self):
        self._log_event("resume")

    # OCR events
    def ocr_attempt(self, scale: float, psm: int, confidence_avg: float):
        self._log_event("ocr-attempt", extra={"scale": scale, "psm": psm, "confidence": confidence_avg})

    # Error events
    def error(self, code: str, reason: str, recoverable: bool = True):
        self._log_event("error", extra={"code": code, "reason": reason, "recoverable": recoverable})

    # General info
    def info(self, message: str, **kwargs):
        self._log_event("info", extra={"message": message, **kwargs})

    # Session end
    def session_end(self, total_tabs: int, internal_count: int):
        self._log_event("session-end", extra={"total_tabs": total_tabs, "internal_count": internal_count})
