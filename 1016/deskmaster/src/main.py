"""DeskMaster MCP - Main orchestrator."""
import sys
import time
import random
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from hud_logger import HUDLogger
from mcp_client import MCPClient
from chrome_manager import ChromeManager
from uia_helper import UIAHelper
from screenshot_helper import ScreenshotHelper
from scanner import ListScanner
from tab_processor import TabProcessor
from captcha_solver import CaptchaSolver
from page_navigator import PageNavigator
from environment import EnvironmentValidator


class DeskMaster:
    """Main orchestrator for DeskMaster automation."""

    def __init__(self):
        # Initialize configuration
        self.config = Config()

        # Initialize logger
        self.logger = HUDLogger(self.config.log_dir)
        self.logger.info("DeskMaster starting...")

        # Initialize helpers
        self.uia = UIAHelper(self.logger)
        self.screenshot = ScreenshotHelper(self.logger, self.config.artifacts_dir)
        self.environment = EnvironmentValidator(self.config, self.logger)

        # Initialize components
        self.mcp = MCPClient(self.config, self.logger)
        self.chrome = ChromeManager(self.config.chrome_path, self.logger)
        self.scanner = ListScanner(self.config, self.logger, self.mcp, self.chrome, self.uia, self.screenshot)
        self.tab_processor = TabProcessor(self.config, self.logger, self.uia, self.chrome)
        self.captcha_solver = CaptchaSolver(self.config, self.logger, self.mcp, self.uia, self.screenshot)
        self.page_navigator = PageNavigator(self.config, self.logger, self.uia)

        # State
        self.current_keyword = None
        self.current_page = 1
        self.total_tabs_opened = 0

    def verify_environment(self) -> bool:
        """
        Verify environment before starting.
        Checks display resolution, zoom, scaling, etc.

        Returns:
            True if environment is valid, False otherwise
        """
        return self.environment.verify_all()

    def verify_presets(self) -> bool:
        """
        Verify and apply sorting/display presets.
        - Sorting: 리뷰 많은순
        - Display: 80개씩 보기

        Returns:
            True if presets verified, False otherwise
        """
        return self.page_navigator.verify_presets()

    def scan_current_page(self, keyword: str, page: int):
        """
        Scan current page for qualifying products.

        Args:
            keyword: Search keyword
            page: Page number
        """
        # Perform scroll passes and collect candidates
        candidates = self.scanner.perform_scroll_passes(keyword, page)

        if not candidates:
            self.logger.info(f"No candidates found on page {page}")
            return

        # Check tab limits before opening
        # TODO: Get actual tab count via UIA
        current_tabs = self.total_tabs_opened + 1  # +1 for list tab

        max_per_page = self.config.max_tabs_per_page
        if len(candidates) > max_per_page:
            self.logger.info(f"Limiting {len(candidates)} candidates to {max_per_page} per page")
            candidates = candidates[:max_per_page]

        # Open candidates in new tabs
        self.scanner.open_candidates_in_tabs(candidates, keyword, page)
        self.total_tabs_opened += len(candidates)

        # Random dwell before processing tabs
        dwell = random.randint(self.config.dwell_times['page_min'],
                              self.config.dwell_times['page_max'])
        time.sleep(dwell / 1000.0)

        # Process detail tabs
        self.process_detail_tabs()

        # Check for CAPTCHA
        if not self.captcha_solver.handle_captcha():
            self.logger.error("captcha-unresolved", "CAPTCHA not solved, stopping")
            return

    def process_detail_tabs(self):
        """Process all detail page tabs to filter internal/external malls."""
        tabs_processed, tabs_closed = self.tab_processor.process_all_tabs()
        self.logger.info(f"Processed {tabs_processed} tabs, closed {tabs_closed} external malls")

        # Update tab count
        self.total_tabs_opened -= tabs_closed

        # Enforce tab limits
        current_tabs = self.uia.get_tab_count()
        if current_tabs > 0:
            pruned = self.tab_processor.enforce_tab_limits(current_tabs)
            if pruned > 0:
                self.total_tabs_opened -= pruned

    def navigate_to_next_page(self) -> bool:
        """
        Navigate to next page via pagination.

        Returns:
            True if navigation successful, False if no next page
        """
        return self.page_navigator.navigate_to_next_page(self.current_page)

    def run_keyword(self, keyword: str):
        """
        Run automation for a single keyword.

        Args:
            keyword: Search keyword to process
        """
        self.logger.info(f"Starting keyword: {keyword}")
        self.current_keyword = keyword
        self.current_page = 1

        max_pages = self.config.get('list_scan.max_pages_per_keyword')

        for page_num in range(1, max_pages + 1):
            self.current_page = page_num
            self.logger.info(f"Processing page {page_num}/{max_pages}")

            # Scan current page
            self.scan_current_page(keyword, page_num)

            # Navigate to next page (if not last)
            if page_num < max_pages:
                if not self.navigate_to_next_page():
                    self.logger.info("No more pages, stopping")
                    break

        self.logger.info(f"Completed keyword: {keyword}, opened {self.total_tabs_opened} tabs")

    def run(self, keywords: list):
        """
        Main execution loop.

        Args:
            keywords: List of keywords to process
        """
        try:
            # Start MCP servers
            self.logger.info("Starting MCP servers...")
            # MCP servers will be started on-demand by mcp_client

            # Verify environment
            if not self.verify_environment():
                self.logger.error("environment-check-failed", "Environment verification failed")
                return

            # Verify presets
            if not self.verify_presets():
                self.logger.error("preset-check-failed", "Preset verification failed")
                return

            # Process each keyword
            for keyword in keywords:
                self.run_keyword(keyword)

            # Final summary
            internal_count = self.total_tabs_opened  # Approximate, would need UIA count
            self.logger.session_end(self.total_tabs_opened + 1, internal_count)

        except KeyboardInterrupt:
            self.logger.info("User interrupted, stopping")
        except Exception as e:
            self.logger.error("fatal-error", str(e), recoverable=False)
            raise
        finally:
            # Cleanup
            self.logger.info("Shutting down...")
            self.mcp.stop_all_servers()


def main():
    """Entry point."""
    # Check for keywords argument
    if len(sys.argv) < 2:
        print("Usage: python main.py <keyword1> [keyword2] ...")
        print("Example: python main.py 캠핑텐트 백팩")
        sys.exit(1)

    keywords = sys.argv[1:]

    print(f"=== DeskMaster MCP ===")
    print(f"Keywords: {', '.join(keywords)}")
    print(f"\n⚠️  준비 사항:")
    print(f"1. Chrome 브라우저에서 네이버 쇼핑 검색 결과 페이지를 열어두세요")
    print(f"2. Chrome 창을 클릭해서 활성화하세요")
    print(f"\n5초 후 자동으로 시작됩니다...")

    # Give user time to switch to Chrome
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)

    print(f"\n시작!\n")

    deskmaster = DeskMaster()
    deskmaster.run(keywords)

    print("\n=== Automation Complete ===")
    print(f"Check logs in: {deskmaster.config.log_dir}")
    print(f"Check artifacts in: {deskmaster.config.artifacts_dir}")


if __name__ == "__main__":
    main()
