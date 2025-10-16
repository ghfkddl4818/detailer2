"""Tab processor - Checks and filters internal/external malls (UIA implemented)."""
import time
from typing import Optional, List, Tuple
from urllib.parse import urlparse

class TabProcessor:
    """Processes detail page tabs to identify and filter malls."""

    def __init__(self, config, logger, uia_helper, chrome_manager):
        self.config = config
        self.logger = logger
        self.uia = uia_helper
        self.chrome = chrome_manager

        self.internal_signals = config.internal_signals
        self.allowed_domains = config.allowed_domains
        self.blocked_domains = config.blocked_domains

    def is_internal_mall(self, tab_index: int) -> bool:
        """
        Check if current tab is an internal mall (Smartstore).

        Args:
            tab_index: Tab index

        Returns:
            True if internal mall, False if external
        """
        # Get current URL
        url = self.uia.get_current_url()
        if not url:
            self.logger.error("tab-url-get-failed", f"Could not get URL for tab {tab_index}")
            return False

        self.logger.detail_check_start(tab_index, url)

        # Check domain first (fast check)
        domain = urlparse(url).netloc if url.startswith('http') else url

        # Blocked domain - definitely external
        for blocked in self.blocked_domains:
            if blocked in domain:
                self.logger.internal_signal_missing(tab_index)
                return False

        # Allowed domain - force internal (even if signal temporarily missing)
        for allowed in self.allowed_domains:
            if allowed in domain:
                self.logger.internal_signal_found(tab_index, f"domain:{allowed}")
                return True

        # Check for internal signals via UIA
        signal_found = self._check_internal_signals(tab_index)

        if signal_found:
            self.logger.internal_signal_found(tab_index, signal_found)
            return True
        else:
            # Edge case: brand.naver.com frames might load slowly
            # Wait 2 seconds and re-check
            self.logger.info(f"Tab {tab_index}: No signal found, waiting 2s for slow load")
            time.sleep(2)

            signal_found = self._check_internal_signals(tab_index)
            if signal_found:
                self.logger.internal_signal_found(tab_index, signal_found)
                return True
            else:
                self.logger.internal_signal_missing(tab_index)
                return False

    def _check_internal_signals(self, tab_index: int) -> Optional[str]:
        """
        Check for internal mall signals in current tab.

        Args:
            tab_index: Tab to check

        Returns:
            Found signal text or None
        """
        try:
            # Search for each internal signal
            for signal in self.internal_signals:
                # Try to find element with this signal text
                element = self.uia.find_element_by_name(signal)

                if element:
                    return signal

            return None

        except Exception as e:
            self.logger.error("internal-signal-check-failed", str(e))
            return None

    def get_all_tab_info(self) -> List[Tuple[int, str]]:
        """
        Get information about all tabs.

        Returns:
            List of (tab_index, url) tuples
        """
        tab_info = []

        try:
            tab_count = self.uia.get_tab_count()
            self.logger.info(f"Total tabs: {tab_count}")

            # Switch to each tab and get URL
            for i in range(1, min(tab_count + 1, 10)):  # Limit to first 9 tabs (Ctrl+1-9)
                if self.uia.switch_to_tab(i):
                    time.sleep(0.3)  # Wait for tab to load

                    url = self.uia.get_current_url()
                    if url:
                        tab_info.append((i, url))

            return tab_info

        except Exception as e:
            self.logger.error("tab-info-get-failed", str(e))
            return tab_info

    def process_all_tabs(self) -> Tuple[int, int]:
        """
        Process all tabs and close external malls.
        Processes tabs in reverse order to handle index changes when closing.

        Returns:
            Tuple of (tabs_processed, tabs_closed)
        """
        tab_info = self.get_all_tab_info()

        tabs_processed = 0
        tabs_closed = 0

        # Skip tab 1 (the list page), process in reverse order
        # Reverse order prevents index shift issues when closing tabs
        for tab_index, url in reversed(tab_info[1:]):
            tabs_processed += 1

            # Switch to tab
            if not self.uia.switch_to_tab(tab_index):
                self.logger.error("tab-switch-failed", f"Failed to switch to tab {tab_index}")
                continue

            time.sleep(0.5)

            # Check if internal
            if not self.is_internal_mall(tab_index):
                # Close external mall
                if self.uia.close_current_tab():
                    self.logger.tab_closed(tab_index, "external-mall")
                    tabs_closed += 1
                    time.sleep(0.2)

        return tabs_processed, tabs_closed

    def enforce_tab_limits(self, current_tab_count: int) -> int:
        """
        Enforce tab limits by closing oldest external tabs.
        Processes tabs in reverse to handle index changes.

        Args:
            current_tab_count: Current number of tabs

        Returns:
            Number of tabs pruned
        """
        max_total = self.config.max_tabs_total

        if current_tab_count <= max_total:
            return 0

        self.logger.tab_limit_hit(current_tab_count, max_total)

        to_prune = current_tab_count - max_total
        pruned = 0

        # Get all tab info
        tab_info = self.get_all_tab_info()

        # First pass: Close external malls (priority), process in reverse
        for tab_index, url in reversed(tab_info[1:]):
            if pruned >= to_prune:
                break

            # Switch to tab
            if not self.uia.switch_to_tab(tab_index):
                continue

            time.sleep(0.3)

            # Check if external (priority to close these first)
            if not self.is_internal_mall(tab_index):
                if self.uia.close_current_tab():
                    pruned += 1
                    self.logger.tab_closed(tab_index, "external-mall-pruned")
                    time.sleep(0.2)

        # If still need to prune, close oldest internal tabs
        if pruned < to_prune:
            # Refresh tab info after closing some tabs
            tab_info = self.get_all_tab_info()

            # Process oldest tabs first (lowest indices after tab 1)
            for tab_index, url in tab_info[1:]:
                if pruned >= to_prune:
                    break

                # Always work with lowest available index (tab 2)
                # Since we close from the front, index 2 will always be the oldest
                if self.uia.switch_to_tab(2):
                    time.sleep(0.3)

                    if self.uia.close_current_tab():
                        self.logger.tab_closed(2, "tab-limit-exceeded")
                        pruned += 1
                        time.sleep(0.2)

        self.logger.tab_pruned(pruned)
        return pruned
