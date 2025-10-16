"""List scanner - Main scanning logic for Naver Shopping."""
import re
import time
import random
from typing import List, Tuple, Optional
from uia_helper import UIAHelper
from screenshot_helper import ScreenshotHelper

class ListScanner:
    """Scans Naver Shopping price comparison lists."""

    def __init__(self, config, logger, mcp_client, chrome_manager, uia_helper, screenshot_helper):
        self.config = config
        self.logger = logger
        self.mcp = mcp_client
        self.chrome = chrome_manager
        self.uia = uia_helper
        self.screenshot = screenshot_helper

        self.review_min = config.review_range['min']
        self.review_max = config.review_range['max']

    def scan_current_viewport(self, keyword: str, page: int) -> List[Tuple[object, int]]:
        """
        Scan current viewport for qualifying products.

        Args:
            keyword: Search keyword
            page: Current page number

        Returns:
            List of (element, review_count) tuples where element is clickable UIAWrapper
        """
        self.logger.list_scan_start(keyword, page)
        candidates = []

        # Try UIA first
        uia_results = self._scan_via_uia()
        if uia_results:
            candidates.extend(uia_results)
            self.logger.info(f"UIA scan found {len(uia_results)} candidates")
        else:
            # Fallback to OCR
            self.logger.info("UIA scan failed, falling back to OCR")
            ocr_results = self._scan_via_ocr()
            if ocr_results:
                candidates.extend(ocr_results)
                self.logger.info(f"OCR scan found {len(ocr_results)} candidates")

        # Filter by review range
        qualified = []
        for idx, (element, review_count) in enumerate(candidates):
            if self.review_min <= review_count <= self.review_max:
                qualified.append((element, review_count))
                self.logger.candidate_found("uia" if uia_results else "ocr", review_count, idx, keyword, page)

        return qualified

    def _scan_via_uia(self) -> List[Tuple[object, int]]:
        """
        Scan using Windows UIA.

        Returns:
            List of (clickable_element, review_count) tuples
        """
        results = []

        try:
            # Find all elements with "리뷰" in their name
            review_elements = self.uia.find_all_elements_by_name(r'리뷰\s*[0-9,]+')

            self.logger.info(f"Found {len(review_elements)} elements with review counts")

            for elem in review_elements:
                try:
                    # Get element text
                    text = self.uia.get_element_text(elem)
                    if not text:
                        continue

                    # Extract review count
                    review_count = self._extract_review_count(text)
                    if review_count is None:
                        continue

                    # Try to find parent clickable element
                    clickable = self._find_clickable_parent(elem)
                    if clickable:
                        results.append((clickable, review_count))

                except Exception as e:
                    self.logger.error("uia-scan-element-failed", str(e))
                    continue

            return results

        except Exception as e:
            self.logger.error("uia-scan-failed", str(e))
            return []

    def _find_clickable_parent(self, element) -> Optional[object]:
        """
        Find clickable parent element (link/button) from review element.

        Args:
            element: Review count element

        Returns:
            Clickable UIAWrapper element or None
        """
        try:
            # Traverse up the tree to find a clickable element
            current = element
            max_depth = 5  # Don't go too far up

            for _ in range(max_depth):
                try:
                    parent = current.parent()
                    if not parent:
                        break

                    # Check if parent is clickable (Link or Button)
                    control_type = parent.element_info.control_type
                    if control_type in ['Hyperlink', 'Button', 'Link']:
                        return parent

                    # Check if parent has clickable patterns
                    try:
                        # If element supports Invoke pattern, it's clickable
                        parent.invoke()  # Try to get the pattern
                        return parent
                    except:
                        pass

                    current = parent

                except Exception:
                    break

            # If no clickable parent found, look for link siblings
            try:
                parent = element.parent()
                siblings = parent.children()

                for sibling in siblings:
                    try:
                        control_type = sibling.element_info.control_type
                        if control_type in ['Hyperlink', 'Link']:
                            return sibling
                    except:
                        continue
            except:
                pass

            return None

        except Exception:
            return None

    def _scan_via_ocr(self) -> List[Tuple[str, int]]:
        """
        Scan using OCR fallback.

        Returns:
            List of (url, review_count) tuples
        """
        results = []

        try:
            # Capture viewport screenshot
            screenshot_path = self.screenshot.capture_viewport()
            if not screenshot_path:
                self.logger.error("ocr-screenshot-failed", "Failed to capture viewport")
                return results

            # Extract text using OCR
            text = self.mcp.ocr_extract_text(str(screenshot_path), 'file')
            if not text:
                self.logger.error("ocr-extract-failed", "Failed to extract text from screenshot")
                return results

            # Find all review counts in the text
            pattern = r'리뷰\s*([0-9,]+)'
            matches = re.finditer(pattern, text)

            for match in matches:
                review_count_str = match.group(1).replace(',', '')
                try:
                    review_count = int(review_count_str)

                    # For OCR fallback, we can't easily get URLs
                    # This would require more sophisticated coordinate mapping
                    # For now, log that we found candidates but can't get URLs
                    self.logger.info(f"OCR found review count: {review_count} (URL extraction not implemented)")

                    # Could be enhanced with:
                    # 1. Character coordinate mapping from Tesseract
                    # 2. Spatial relationship analysis to find nearby URLs
                    # 3. Pattern matching for common URL structures in the image

                except ValueError:
                    continue

            self.logger.info(f"OCR fallback incomplete - found counts but URL extraction needs enhancement")
            return results

        except Exception as e:
            self.logger.error("ocr-scan-failed", str(e))
            return results

    def _extract_review_count(self, text: str) -> Optional[int]:
        """
        Extract review count from text.

        Args:
            text: Text containing review count (e.g., "리뷰 1,234")

        Returns:
            Review count as integer or None
        """
        # Pattern: "리뷰 N,NNN" or "리뷰 NNN"
        pattern = r'리뷰\s*([0-9,]+)'
        match = re.search(pattern, text)

        if match:
            count_str = match.group(1).replace(',', '')
            try:
                return int(count_str)
            except ValueError:
                return None

        return None

    def scroll_viewport(self, direction: str = 'down'):
        """
        Scroll the current viewport.

        Args:
            direction: 'down' or 'up'
        """
        # Random scroll amount for human-like behavior
        amount = random.randint(1, 3)

        # Use UIA helper to scroll
        self.uia.scroll_page(direction, amount)

        # Random dwell time
        dwell_min = self.config.dwell_times['view_min']
        dwell_max = self.config.dwell_times['view_max']
        dwell_ms = random.randint(dwell_min, dwell_max)

        time.sleep(dwell_ms / 1000.0)

    def perform_scroll_passes(self, keyword: str, page: int) -> List[Tuple[object, int]]:
        """
        Perform multiple scroll passes on current page.

        Args:
            keyword: Search keyword
            page: Current page number

        Returns:
            All qualified candidates found (element, review_count) tuples
        """
        scroll_min = self.config.get('list_scan.scroll_passes_min')
        scroll_max = self.config.get('list_scan.scroll_passes_max')
        num_passes = random.randint(scroll_min, scroll_max)

        all_candidates = []
        seen_elements = set()

        for pass_num in range(num_passes):
            # Scan current viewport
            candidates = self.scan_current_viewport(keyword, page)

            # Add new candidates (deduplicate by element ID)
            for elem, count in candidates:
                elem_id = id(elem)
                if elem_id not in seen_elements:
                    all_candidates.append((elem, count))
                    seen_elements.add(elem_id)

            # Scroll down
            if pass_num < num_passes - 1:
                self.scroll_viewport('down')

        self.logger.info(f"Completed {num_passes} scroll passes, found {len(all_candidates)} unique candidates")
        return all_candidates

    def open_candidates_in_tabs(self, candidates: List[Tuple[object, int]], keyword: str, page: int):
        """
        Open qualified candidates in new tabs by clicking elements.

        Args:
            candidates: List of (clickable_element, review_count) tuples
            keyword: Search keyword
            page: Current page number
        """
        for elem, review_count in candidates:
            try:
                # Click the element to open in new tab
                # Note: This may open in same tab, need Ctrl+Click or middle click
                # For now, just invoke the element
                success = self.uia.click_element(elem)

                if success:
                    self.logger.open_new_tab(True, f"element_{id(elem)}", keyword, page)
                    # Wait for new tab to open
                    time.sleep(0.5)
                else:
                    self.logger.open_new_tab(False, f"element_{id(elem)}", keyword, page)

            except Exception as e:
                self.logger.error("open-tab-failed", str(e))
                self.logger.open_new_tab(False, f"element_{id(elem)}", keyword, page)

            # Small delay between tab opens
            time.sleep(random.uniform(0.1, 0.3))
