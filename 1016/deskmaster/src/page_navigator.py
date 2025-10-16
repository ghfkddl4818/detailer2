"""Page navigation handler for pagination."""
import time
import random
from typing import Optional

class PageNavigator:
    """Handles page navigation via pagination controls."""

    def __init__(self, config, logger, uia_helper):
        self.config = config
        self.logger = logger
        self.uia = uia_helper

    def find_pagination_container(self):
        """
        Find pagination container (bottom navigation area).

        Returns:
            Pagination container element or None
        """
        try:
            # Look for navigation role elements in bottom 25% of screen
            # Common patterns: "페이지", "다음", "이전", numbers
            nav_patterns = [r'페이지', r'다음', r'이전', r'[0-9]+']

            for pattern in nav_patterns:
                elem = self.uia.find_element_by_name(pattern)
                if elem:
                    # Check if element is in bottom 25% of screen
                    rect = self.uia.get_element_rectangle(elem)
                    if rect:
                        # Get screen height
                        screen_height = 1080  # From config
                        elem_top = rect[1]

                        if elem_top > screen_height * 0.75:
                            return elem.parent()  # Return container

            return None

        except Exception as e:
            self.logger.error("pagination-container-not-found", str(e))
            return None

    def find_next_page_element(self, current_page: int) -> Optional[object]:
        """
        Find next page link element.

        Args:
            current_page: Current page number

        Returns:
            Next page element or None
        """
        try:
            next_page = current_page + 1

            # Try to find next page number
            next_page_elem = self.uia.find_element_by_name(str(next_page))
            if next_page_elem:
                # Verify it's in pagination area (bottom 25%)
                rect = self.uia.get_element_rectangle(next_page_elem)
                if rect and rect[1] > 1080 * 0.75:
                    return next_page_elem

            # Try to find "다음" (Next) button
            next_button = self.uia.find_element_by_name(r'다음')
            if next_button:
                rect = self.uia.get_element_rectangle(next_button)
                if rect and rect[1] > 1080 * 0.75:
                    return next_button

            return None

        except Exception as e:
            self.logger.error("next-page-element-not-found", str(e))
            return None

    def navigate_to_next_page(self, current_page: int) -> bool:
        """
        Navigate to next page.

        Args:
            current_page: Current page number

        Returns:
            True if navigation successful, False otherwise
        """
        next_page = current_page + 1

        self.logger.page_move_attempt(current_page, next_page)

        # Random dwell before navigation
        if random.random() < 0.1:  # 10% chance of long wait
            dwell = random.randint(
                self.config.dwell_times['long_min'],
                self.config.dwell_times['long_max']
            )
        else:
            dwell = random.randint(
                self.config.dwell_times['page_min'],
                self.config.dwell_times['page_max']
            )

        self.logger.page_wait(dwell)
        time.sleep(dwell / 1000.0)

        # Optional: random up/down scroll before clicking
        if random.random() < 0.3:  # 30% chance
            self.uia.scroll_page('up', 1)
            time.sleep(0.2)
            self.uia.scroll_page('down', 1)
            time.sleep(0.2)

        # Find and click next page element
        next_elem = self.find_next_page_element(current_page)
        if not next_elem:
            self.logger.page_move_fail(current_page, "next-page-not-found")
            return False

        # Click the element
        if self.uia.click_element(next_elem):
            time.sleep(1.5)  # Wait for page to load
            self.logger.page_move_ok(next_page)
            return True
        else:
            self.logger.page_move_fail(current_page, "click-failed")
            return False

    def verify_presets(self) -> bool:
        """
        Verify and apply sorting/display presets.

        Returns:
            True if presets verified, False otherwise
        """
        self.logger.preset_verify_start()

        preset_sorting = self.config.get('preset.sorting')
        preset_display = self.config.get('preset.display_count')
        max_retry = self.config.get('preset.max_retry', 3)
        skip_display_check = self.config.get('preset.skip_display_check', False)

        # Verify sorting preset
        for attempt in range(max_retry):
            sorting_elem = self.uia.find_element_by_name(preset_sorting)

            if sorting_elem:
                self.logger.preset_verify_ok("sorting")
                break
            else:
                self.logger.preset_verify_retry("sorting", attempt + 1)

                # Try to find sorting dropdown and select
                sort_dropdown = self.uia.find_element_by_name(r'정렬')
                if sort_dropdown:
                    self.uia.click_element(sort_dropdown)
                    time.sleep(0.5)

                    # Find and click the preset option
                    preset_option = self.uia.find_element_by_name(preset_sorting)
                    if preset_option:
                        self.uia.click_element(preset_option)
                        time.sleep(1)
                        continue

                if attempt == max_retry - 1:
                    self.logger.preset_verify_fail("sorting")
                    return False

        # Verify display count preset (optional)
        if skip_display_check:
            self.logger.info("Skipping display count verification (skip_display_check=true)")
            return True

        for attempt in range(max_retry):
            display_elem = self.uia.find_element_by_name(preset_display)

            if display_elem:
                self.logger.preset_verify_ok("display")
                break
            else:
                self.logger.preset_verify_retry("display", attempt + 1)

                # Try multiple patterns to find display dropdown
                dropdown_patterns = [
                    r'.*개씩.*보기.*',  # More flexible pattern
                    r'.*개.*보기.*',
                    r'40개씩 보기',  # Current value (if not 80)
                    r'80개씩 보기',  # Target value
                ]

                display_dropdown = None
                for pattern in dropdown_patterns:
                    elem = self.uia.find_element_by_name(pattern)
                    if elem:
                        display_dropdown = elem
                        self.logger.info(f"Found display dropdown with pattern: {pattern}")
                        break

                if display_dropdown:
                    self.uia.click_element(display_dropdown)
                    time.sleep(1.0)  # Wait for dropdown to open

                    # Find and click the preset option (80개씩 보기)
                    preset_option = self.uia.find_element_by_name(preset_display)
                    if preset_option:
                        self.uia.click_element(preset_option)
                        time.sleep(1.5)  # Wait for page reload
                        continue
                else:
                    self.logger.info("Display dropdown not found, trying direct click")

                if attempt == max_retry - 1:
                    self.logger.preset_verify_fail("display")
                    return False

        return True
