"""Environment validation and verification."""
import ctypes
import win32gui
import win32con
from typing import Tuple, Optional

class EnvironmentValidator:
    """Validates system environment before automation starts."""

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

        self.required_width = config.get('display.width', 1920)
        self.required_height = config.get('display.height', 1080)
        self.required_scale = config.get('display.scale', 100)

    def get_screen_resolution(self) -> Tuple[int, int]:
        """Get current screen resolution."""
        user32 = ctypes.windll.user32
        width = user32.GetSystemMetrics(0)  # SM_CXSCREEN
        height = user32.GetSystemMetrics(1)  # SM_CYSCREEN
        return width, height

    def get_display_scaling(self) -> int:
        """Get display scaling percentage."""
        try:
            # Get DPI awareness
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
        except:
            pass

        # Get DPI
        hdc = ctypes.windll.user32.GetDC(0)
        dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
        ctypes.windll.user32.ReleaseDC(0, hdc)

        # Calculate scaling percentage (96 DPI = 100%)
        scaling = int((dpi / 96.0) * 100)
        return scaling

    def verify_display_settings(self) -> bool:
        """
        Verify display resolution and scaling.

        Returns:
            True if valid, False otherwise
        """
        # Check resolution
        width, height = self.get_screen_resolution()
        self.logger.info(f"Screen resolution: {width}x{height}")

        if width != self.required_width or height != self.required_height:
            self.logger.error(
                "display-resolution-mismatch",
                f"Expected {self.required_width}x{self.required_height}, got {width}x{height}",
                recoverable=False
            )
            return False

        # Check scaling
        scaling = self.get_display_scaling()
        self.logger.info(f"Display scaling: {scaling}%")

        if scaling != self.required_scale:
            self.logger.error(
                "display-scale-mismatch",
                f"Expected {self.required_scale}%, got {scaling}%",
                recoverable=False
            )
            return False

        self.logger.info("Display settings verified OK")
        return True

    def verify_chrome_zoom(self) -> bool:
        """
        Verify Chrome zoom is at 100%.
        This requires UIA to check Chrome's zoom level.

        Returns:
            True if 100%, False otherwise
        """
        # TODO: Implement via UIA
        # Would need to:
        # 1. Find Chrome window
        # 2. Check zoom level (possibly via menu or keyboard shortcut)
        # 3. Set to 100% if not already

        self.logger.info("Chrome zoom verification not yet implemented (assuming OK)")
        return True

    def verify_chrome_maximized(self) -> bool:
        """
        Verify Chrome window is maximized.

        Returns:
            True if maximized, False otherwise
        """
        try:
            # Find Chrome window
            hwnd = win32gui.FindWindow("Chrome_WidgetWin_1", None)
            if not hwnd:
                self.logger.error("chrome-window-not-found", "Chrome window not found")
                return False

            # Check if maximized
            placement = win32gui.GetWindowPlacement(hwnd)
            is_maximized = (placement[1] == win32con.SW_SHOWMAXIMIZED)

            if not is_maximized:
                self.logger.info("Chrome not maximized, maximizing now...")
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                self.logger.info("Chrome maximized")

            return True

        except Exception as e:
            self.logger.error("chrome-maximize-check-failed", str(e))
            return False

    def check_primary_monitor(self) -> bool:
        """
        Check if automation is running on primary monitor.

        Returns:
            True if on primary monitor
        """
        # For multi-monitor setups, should verify Chrome is on primary
        # For now, assume single monitor or primary
        self.logger.info("Primary monitor check not yet implemented (assuming OK)")
        return True

    def verify_all(self) -> bool:
        """
        Run all environment checks.

        Returns:
            True if all checks pass, False otherwise
        """
        self.logger.info("Starting environment verification...")

        checks = [
            ("Display settings", self.verify_display_settings),
            ("Primary monitor", self.check_primary_monitor),
            ("Chrome maximized", self.verify_chrome_maximized),
            ("Chrome zoom", self.verify_chrome_zoom),
        ]

        for check_name, check_func in checks:
            self.logger.info(f"Checking: {check_name}")
            if not check_func():
                self.logger.error(
                    "environment-check-failed",
                    f"Failed: {check_name}",
                    recoverable=False
                )
                return False

        self.logger.info("All environment checks passed ✓")
        return True
