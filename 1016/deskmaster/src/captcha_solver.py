"""CAPTCHA solver using Gemini Vision API (UIA implemented)."""
import time
import random
from pathlib import Path
from typing import Optional, Dict

class CaptchaSolver:
    """Solves CAPTCHAs using Gemini Vision API."""

    def __init__(self, config, logger, mcp_client, uia_helper, screenshot_helper):
        self.config = config
        self.logger = logger
        self.mcp = mcp_client
        self.uia = uia_helper
        self.screenshot = screenshot_helper

        self.captcha_config = config.captcha_config
        self.artifacts_dir = config.artifacts_dir

        self.paused = False

    def detect_captcha(self) -> Optional[str]:
        """
        Detect if CAPTCHA is present on current page.

        Returns:
            CAPTCHA type if detected, None otherwise
        """
        keywords = self.captcha_config['keywords']

        try:
            # Check for CAPTCHA keywords in UIA elements
            for keyword in keywords:
                element = self.uia.find_element_by_name(keyword)
                if element:
                    self.logger.info(f"CAPTCHA detected via keyword: {keyword}")
                    return "text"  # Assume text CAPTCHA for now

            return None

        except Exception as e:
            self.logger.error("captcha-detect-failed", str(e))
            return None

    def capture_captcha_screenshot(self) -> Optional[Path]:
        """
        Capture screenshot of CAPTCHA area.

        Returns:
            Path to saved screenshot or None
        """
        try:
            # Try to find CAPTCHA element to get its region
            captcha_elem = None
            for keyword in self.captcha_config['keywords']:
                elem = self.uia.find_element_by_name(keyword)
                if elem:
                    captcha_elem = elem
                    break

            if captcha_elem:
                # Get element rectangle
                rect = self.uia.get_element_rectangle(captcha_elem)
                if rect:
                    # Capture that region
                    return self.screenshot.capture_element_region(rect, "captcha")

            # Fallback: capture full viewport
            return self.screenshot.capture_viewport()

        except Exception as e:
            self.logger.error("captcha-screenshot-failed", str(e))
            return None

    def solve_with_gemini(self, image_path: Path, attempt: int) -> Optional[Dict]:
        """
        Solve CAPTCHA using Gemini Vision API.

        Args:
            image_path: Path to CAPTCHA image
            attempt: Attempt number (1-based)

        Returns:
            Dict with 'answer' and 'confidence' or None
        """
        self.logger.captcha_solve_start("gemini")

        try:
            result = self.mcp.gemini_solve_captcha(str(image_path))

            if result and result.get('confidence', 0) >= self.captcha_config['min_confidence']:
                self.logger.captcha_solve_ok(result['confidence'])
                return result
            else:
                self.logger.captcha_solve_fail("low-confidence", attempt)
                return None

        except Exception as e:
            self.logger.captcha_solve_fail(str(e), attempt)
            return None

    def enter_captcha_answer(self, answer: str) -> bool:
        """
        Enter CAPTCHA answer into input field.

        Args:
            answer: CAPTCHA answer text

        Returns:
            Success status
        """
        try:
            # Find CAPTCHA input field
            # Common patterns: "보안문자", "입력", "input"
            input_patterns = [r'입력', r'보안문자', r'answer', r'captcha']

            input_elem = None
            for pattern in input_patterns:
                elem = self.uia.find_element_by_name(pattern)
                if elem:
                    input_elem = elem
                    break

            if not input_elem:
                self.logger.error("captcha-input-not-found", "Could not find CAPTCHA input field")
                return False

            # Enter answer
            if not self.uia.set_element_value(input_elem, answer):
                return False

            time.sleep(0.5)

            # Find and click submit button
            submit_patterns = [r'확인', r'제출', r'submit', r'OK']

            for pattern in submit_patterns:
                submit_elem = self.uia.find_element_by_name(pattern)
                if submit_elem:
                    self.uia.click_element(submit_elem)
                    time.sleep(1)
                    return True

            # If no submit button found, log error (NO keyboard input allowed)
            self.logger.error("captcha-submit-not-found", "Could not find submit button")
            return False

        except Exception as e:
            self.logger.error("captcha-enter-failed", str(e))
            return False

    def verify_captcha_solved(self) -> bool:
        """
        Verify that CAPTCHA was solved successfully.

        Returns:
            True if CAPTCHA is gone, False if still present
        """
        # Wait a bit for page to update
        time.sleep(1)

        # Check if CAPTCHA is still present
        captcha_type = self.detect_captcha()
        return captcha_type is None

    def pause_for_manual_solve(self):
        """Pause automation for manual CAPTCHA solving."""
        self.paused = True
        self.logger.pause("captcha-manual-solve-required")

        print("\n" + "="*60)
        print("⚠️  CAPTCHA 자동 해결 실패")
        print("="*60)
        print("수동으로 CAPTCHA를 해결해주세요.")
        print("해결 후 아무 키나 누르면 계속됩니다...")
        print("="*60 + "\n")

        input("Press Enter to resume...")

        self.paused = False
        self.logger.resume()

    def handle_captcha(self) -> bool:
        """
        Main CAPTCHA handling workflow.

        Returns:
            True if CAPTCHA solved or not present, False if failed
        """
        # Detect CAPTCHA
        captcha_type = self.detect_captcha()
        if not captcha_type:
            return True  # No CAPTCHA present

        self.logger.captcha_detected(captcha_type)

        if not self.captcha_config['auto_solver']['enabled']:
            # Auto-solver disabled, pause for manual solving
            self.pause_for_manual_solve()
            return self.verify_captcha_solved()

        # Capture screenshot
        screenshot_path = self.capture_captcha_screenshot()
        if not screenshot_path:
            self.pause_for_manual_solve()
            return self.verify_captcha_solved()

        # Try auto-solving with retries
        max_attempts = self.captcha_config['auto_solver']['max_attempts']

        for attempt in range(1, max_attempts + 1):
            result = self.solve_with_gemini(screenshot_path, attempt)

            if result:
                # Enter answer
                if self.enter_captcha_answer(result['answer']):
                    # Verify solved
                    if self.verify_captcha_solved():
                        self.logger.resume()
                        return True

            # Backoff before retry
            if attempt < max_attempts:
                backoff = random.uniform(2, 5)
                time.sleep(backoff)

        # All attempts failed, pause for manual solving
        self.pause_for_manual_solve()
        return self.verify_captcha_solved()
