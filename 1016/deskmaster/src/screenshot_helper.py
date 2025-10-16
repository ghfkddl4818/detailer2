"""Screenshot capture helper."""
from PIL import ImageGrab, Image
from pathlib import Path
from typing import Optional, Tuple
import time

class ScreenshotHelper:
    """Helper for capturing screenshots."""

    def __init__(self, logger, artifacts_dir: Path):
        self.logger = logger
        self.artifacts_dir = artifacts_dir

    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> Optional[Image.Image]:
        """
        Capture screenshot.

        Args:
            region: Optional (left, top, right, bottom) tuple for region capture

        Returns:
            PIL Image or None
        """
        try:
            if region:
                img = ImageGrab.grab(bbox=region)
            else:
                img = ImageGrab.grab()

            return img

        except Exception as e:
            self.logger.error("screenshot-capture-failed", str(e))
            return None

    def save_screenshot(self, img: Image.Image, filename: str) -> Optional[Path]:
        """
        Save screenshot to artifacts directory.

        Args:
            img: PIL Image
            filename: Filename (without path)

        Returns:
            Path to saved file or None
        """
        try:
            filepath = self.artifacts_dir / filename
            img.save(filepath)
            self.logger.info(f"Screenshot saved: {filepath}")
            return filepath

        except Exception as e:
            self.logger.error("screenshot-save-failed", str(e))
            return None

    def capture_and_save(self, filename: str, region: Optional[Tuple[int, int, int, int]] = None) -> Optional[Path]:
        """
        Capture and save screenshot in one call.

        Args:
            filename: Filename for saved screenshot
            region: Optional region to capture

        Returns:
            Path to saved file or None
        """
        img = self.capture_screen(region)
        if img:
            return self.save_screenshot(img, filename)
        return None

    def capture_viewport(self) -> Optional[Path]:
        """
        Capture current browser viewport.

        Returns:
            Path to saved screenshot or None
        """
        timestamp = int(time.time())
        filename = f"viewport_{timestamp}.png"
        return self.capture_and_save(filename)

    def capture_element_region(self, rect: Tuple[int, int, int, int], name: str) -> Optional[Path]:
        """
        Capture specific element region.

        Args:
            rect: (left, top, right, bottom) rectangle
            name: Name for file (e.g., 'captcha', 'card')

        Returns:
            Path to saved screenshot or None
        """
        timestamp = int(time.time())
        filename = f"{name}_{timestamp}.png"
        return self.capture_and_save(filename, region=rect)
