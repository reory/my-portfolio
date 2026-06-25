import os
from loguru import logger


def load_theme_css(theme_name):
    """Load CSS file for selected UI theme"""

    # Build full path to the selected themes CSS directory
    css_path = os.path.join("templates", "css", theme_name)

    try:
        with open(css_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Could not load theme {theme_name}: {e}")
        return ""
