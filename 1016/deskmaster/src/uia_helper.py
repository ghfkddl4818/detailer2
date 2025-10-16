"""Windows UI Automation helper using pywinauto."""
from typing import Optional, List, Dict, Tuple
import time
import re
from pywinauto import Desktop, Application
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.findwindows import ElementNotFoundError

class UIAHelper:
    """Helper class for Windows UI Automation operations."""

    def __init__(self, logger):
        self.logger = logger
        self.desktop = Desktop(backend="uia")
        self.chrome_app = None
        self.chrome_window = None

    def connect_to_chrome(self) -> bool:
        """
        Connect to Chrome browser window.
        Connects to the currently focused (active) Chrome window.

        Returns:
            True if connected, False otherwise
        """
        try:
            import win32gui

            # Get the currently focused window handle
            foreground_hwnd = win32gui.GetForegroundWindow()

            # Get the class name of the focused window
            class_name = win32gui.GetClassName(foreground_hwnd)

            # Check if it's a Chrome window
            if class_name == "Chrome_WidgetWin_1":
                self.logger.info("Detected focused Chrome window")

                # Connect to this specific Chrome window by handle
                self.chrome_app = Application(backend="uia").connect(handle=foreground_hwnd)
                self.chrome_window = self.chrome_app.window(handle=foreground_hwnd)

                self.logger.info("Connected to Chrome via UIA")
                return True
            else:
                # Fallback: find any Chrome window
                self.logger.info(f"Focused window is not Chrome (class: {class_name}), searching for Chrome windows...")

                chrome_windows = self.desktop.windows(class_name="Chrome_WidgetWin_1")

                if not chrome_windows:
                    self.logger.error("uia-chrome-not-found", "No Chrome windows found")
                    return False

                self.logger.info(f"Found {len(chrome_windows)} Chrome window(s), using the first one")

                # Get the first Chrome window
                self.chrome_window = chrome_windows[0]
                self.chrome_app = Application(backend="uia").connect(handle=self.chrome_window.handle)

                self.logger.info("Connected to Chrome via UIA")
                return True

        except ElementNotFoundError:
            self.logger.error("uia-chrome-not-found", "Chrome window not found")
            return False
        except Exception as e:
            self.logger.error("uia-connect-failed", str(e))
            return False

    def find_element_by_name(self, name_pattern: str, control_type: Optional[str] = None) -> Optional[UIAWrapper]:
        """
        Find UI element by name pattern.

        Args:
            name_pattern: Regex pattern to match element name
            control_type: Optional control type filter

        Returns:
            UIAWrapper element or None
        """
        try:
            if not self.chrome_window:
                if not self.connect_to_chrome():
                    return None

            # Get all descendants
            descendants = self.chrome_window.descendants()

            for elem in descendants:
                try:
                    elem_name = elem.window_text()

                    # Check name pattern
                    if re.search(name_pattern, elem_name):
                        # Check control type if specified
                        if control_type:
                            if elem.element_info.control_type == control_type:
                                return elem
                        else:
                            return elem

                except:
                    continue

            return None

        except Exception as e:
            self.logger.error("uia-find-element-failed", str(e))
            return None

    def find_all_elements_by_name(self, name_pattern: str) -> List[UIAWrapper]:
        """
        Find all UI elements matching name pattern.

        Args:
            name_pattern: Regex pattern to match element names

        Returns:
            List of UIAWrapper elements
        """
        results = []

        try:
            if not self.chrome_window:
                if not self.connect_to_chrome():
                    return results

            descendants = self.chrome_window.descendants()

            for elem in descendants:
                try:
                    elem_name = elem.window_text()
                    if re.search(name_pattern, elem_name):
                        results.append(elem)
                except:
                    continue

        except Exception as e:
            self.logger.error("uia-find-all-failed", str(e))

        return results

    def get_element_text(self, element: UIAWrapper) -> Optional[str]:
        """Get text from element."""
        try:
            return element.window_text()
        except:
            return None

    def click_element(self, element: UIAWrapper) -> bool:
        """
        Invoke UI element using UIA pattern (NO physical mouse/keyboard).

        Args:
            element: Element to invoke

        Returns:
            Success status
        """
        try:
            # Use Invoke pattern (UIA automation, no physical input)
            element.invoke()
            time.sleep(0.1)
            return True
        except Exception as e:
            self.logger.error("uia-invoke-failed", str(e))
            return False

    def set_element_value(self, element: UIAWrapper, value: str) -> bool:
        """
        Set value using Value pattern (NO physical keyboard input).

        Args:
            element: Input element
            value: Value to set

        Returns:
            Success status
        """
        try:
            # Use Value pattern (UIA automation, no physical input)
            element.element_info.set_value(value)
            return True
        except Exception as e:
            self.logger.error("uia-set-value-failed", str(e))
            return False

    def scroll_page(self, direction: str = "down", amount: int = 3) -> bool:
        """
        Scroll page using UIA Scroll pattern (NO physical keyboard).

        Args:
            direction: 'down' or 'up'
            amount: Number of times to scroll

        Returns:
            Success status
        """
        try:
            if not self.chrome_window:
                if not self.connect_to_chrome():
                    return False

            # Define scroll amount based on direction
            scroll_amount = "SmallIncrement" if direction == "down" else "SmallDecrement"

            # Find scrollable element (document/pane)
            try:
                scroll_elem = self.chrome_window.child_window(control_type="Pane", found_index=0)

                for _ in range(amount):
                    scroll_elem.scroll(direction="vertical", amount=scroll_amount)
                    time.sleep(0.05)

                return True
            except:
                # Fallback: try to find Document element
                try:
                    doc_elem = self.chrome_window.child_window(control_type="Document", found_index=0)
                    for _ in range(amount):
                        doc_elem.scroll(direction="vertical", amount=scroll_amount)
                        time.sleep(0.05)
                    return True
                except:
                    self.logger.error("uia-scroll-failed", "No scrollable element found")
                    return False

        except Exception as e:
            self.logger.error("uia-scroll-failed", str(e))
            return False

    def get_element_rectangle(self, element: UIAWrapper) -> Optional[Tuple[int, int, int, int]]:
        """
        Get element's bounding rectangle.

        Args:
            element: UI element

        Returns:
            Tuple of (left, top, right, bottom) or None
        """
        try:
            rect = element.rectangle()
            return (rect.left, rect.top, rect.right, rect.bottom)
        except:
            return None

    def get_tab_count(self) -> int:
        """
        Get number of Chrome tabs.

        Returns:
            Tab count
        """
        try:
            # Find tab strip - multilingual patterns
            tab_patterns = [r'.*탭$', r'.*tab$', r'.*Tab$']
            tab_elements = []

            for pattern in tab_patterns:
                elements = self.find_all_elements_by_name(pattern)
                if elements:
                    tab_elements = elements
                    break

            if not tab_elements:
                return 0

            # Filter to actual tab elements (not "새 탭"/"New tab" button)
            exclude_patterns = ['새 탭', 'New tab', 'New Tab']
            actual_tabs = []

            for elem in tab_elements:
                text = self.get_element_text(elem)
                if text and not any(pattern in text for pattern in exclude_patterns):
                    actual_tabs.append(elem)

            return len(actual_tabs)

        except Exception as e:
            self.logger.error("uia-tab-count-failed", str(e))
            return 0

    def get_current_url(self) -> Optional[str]:
        """
        Get current page URL from address bar.

        Returns:
            URL string or None
        """
        try:
            # Find address bar (omnibox) - multilingual patterns
            address_patterns = [
                r'.*주소 및 검색 표시줄.*',  # Korean
                r'.*Address and search bar.*',  # English
                r'.*Search or enter address.*',  # English variant
                r'.*주소.*검색.*',  # Korean variant
            ]

            address_bar = None
            for pattern in address_patterns:
                elem = self.find_element_by_name(pattern)
                if elem:
                    address_bar = elem
                    break

            if address_bar:
                url = self.get_element_text(address_bar)
                return url

            # Fallback: Try to find by control type
            try:
                # Address bar is usually an Edit control
                address_bar = self.chrome_window.child_window(control_type="Edit", found_index=0)
                if address_bar:
                    url = self.get_element_text(address_bar)
                    if url and ('http' in url or 'www' in url):
                        return url
            except:
                pass

            return None

        except Exception as e:
            self.logger.error("uia-get-url-failed", str(e))
            return None

    def close_current_tab(self) -> bool:
        """
        Close current tab by finding and invoking close button (NO keyboard input).

        Returns:
            Success status
        """
        try:
            if not self.chrome_window:
                if not self.connect_to_chrome():
                    return False

            # Find tab close button - multilingual patterns
            close_patterns = [
                r'닫기',        # Korean
                r'Close',       # English
                r'close',       # lowercase
                r'×',           # Close symbol
                r'[Xx]',       # X button
            ]

            close_button = None
            for pattern in close_patterns:
                elem = self.find_element_by_name(pattern)
                if elem:
                    close_button = elem
                    break

            if close_button:
                return self.click_element(close_button)
            else:
                self.logger.error("uia-close-tab-failed", "Close button not found")
                return False

        except Exception as e:
            self.logger.error("uia-close-tab-failed", str(e))
            return False

    def switch_to_tab(self, tab_index: int) -> bool:
        """
        Switch to tab by finding and invoking tab element (NO keyboard input).

        Args:
            tab_index: Tab index (1-based)

        Returns:
            Success status
        """
        try:
            if not self.chrome_window:
                if not self.connect_to_chrome():
                    return False

            # Find all tab elements - multilingual patterns
            tab_patterns = [r'.*탭$', r'.*tab$', r'.*Tab$']
            tab_elements = []

            for pattern in tab_patterns:
                elements = self.find_all_elements_by_name(pattern)
                if elements:
                    tab_elements = elements
                    break

            if not tab_elements:
                self.logger.error("uia-switch-tab-failed", "No tab elements found")
                return False

            # Filter out "새 탭"/"New tab" button
            exclude_patterns = ['새 탭', 'New tab', 'New Tab']
            actual_tabs = []

            for elem in tab_elements:
                text = self.get_element_text(elem)
                if text and not any(pattern in text for pattern in exclude_patterns):
                    actual_tabs.append(elem)

            if tab_index <= len(actual_tabs):
                target_tab = actual_tabs[tab_index - 1]
                return self.click_element(target_tab)
            else:
                self.logger.error("uia-switch-tab-failed", f"Tab index {tab_index} out of range (max: {len(actual_tabs)})")
                return False

        except Exception as e:
            self.logger.error("uia-switch-tab-failed", str(e))
            return False

    def press_key(self, key: str) -> bool:
        """
        DEPRECATED: Physical keyboard input not allowed per spec.
        Use UIA patterns (Invoke/Value/Scroll) instead.

        Args:
            key: Key to press (NOT USED)

        Returns:
            Always False
        """
        self.logger.error("uia-press-key-forbidden", "Physical keyboard input not allowed - use UIA patterns")
        return False
