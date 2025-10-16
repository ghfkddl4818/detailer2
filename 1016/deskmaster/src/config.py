"""Configuration loader for DeskMaster."""
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration manager."""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.yaml"

        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)

        # Environment variables
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")

        # Tesseract path
        tesseract_path = self._config['ocr']['tesseract_path']
        if os.path.exists(tesseract_path):
            os.environ['TESSERACT_CMD'] = tesseract_path

    def get(self, key: str, default=None):
        """Get configuration value by dot notation key."""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

    @property
    def chrome_path(self) -> str:
        return self.get('chrome.path')

    @property
    def review_range(self) -> dict:
        return self.get('review_range')

    @property
    def internal_signals(self) -> list:
        return self.get('internal_signals')

    @property
    def allowed_domains(self) -> list:
        return self.get('allowed_domains')

    @property
    def blocked_domains(self) -> list:
        return self.get('blocked_domains')

    @property
    def max_tabs_total(self) -> int:
        return self.get('chrome.max_tabs_total')

    @property
    def max_tabs_per_page(self) -> int:
        return self.get('chrome.max_tabs_per_page')

    @property
    def captcha_config(self) -> dict:
        return self.get('captcha')

    @property
    def dwell_times(self) -> dict:
        return self.get('dwell')

    @property
    def ocr_config(self) -> dict:
        return self.get('ocr')

    @property
    def log_dir(self) -> Path:
        log_dir = Path(__file__).parent.parent / self.get('logging.dir')
        log_dir.mkdir(exist_ok=True)
        return log_dir

    @property
    def artifacts_dir(self) -> Path:
        artifacts_dir = Path(__file__).parent.parent / self.get('logging.artifacts_dir')
        artifacts_dir.mkdir(exist_ok=True)
        return artifacts_dir
