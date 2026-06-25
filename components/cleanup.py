import os
from loguru import logger


def clean_docs():
    """Removes all generated HTML files to ensure a fresh build"""

    if not os.path.exists("docs"):
        os.makedirs("docs")
        return

    for f in os.listdir("docs"):
        if f.endswith(".html"):
            os.remove(os.path.join("docs", f))
    logger.info("🧹 Successfully cleaned old HTML files from/docs")
