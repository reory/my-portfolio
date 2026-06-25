import os
from loguru import logger

from components.cleanup import clean_docs
from components.images import sync_images, optimise_images
from components.themes import load_theme_css
from components.projects import load_projects, scan_skills
from components.scanner import scan_for_challenges
from components.pages import (
    build_project_pages,
    generate_home_page,
    build_challenges_page,
)

THEME_NAME = "slate.css"
logger.add("generator.log", rotation="1 MB")


def build_portfolio():
    """Assemble full portfolio dataset or assets for export/render"""

    logger.info("🚀 Starting Portfolio Build Sequence...")
    if not os.path.exists("docs"):
        os.makedirs("docs")

    # Load the selected theme's CSS and fetch all project data for the build.
    custom_css = load_theme_css(THEME_NAME)
    projects = load_projects()

    if not projects:
        return

    # Rescan all projects to extract skills
    # then keep the resulting frequency counts.
    scan_skills(projects)
    skill_counts = scan_skills(projects)

    # Build all project pages, then generate the home page using the result
    # and skills stats.
    built_projects = build_project_pages(projects, custom_css)
    generate_home_page(built_projects, custom_css, skill_counts)


if __name__ == "__main__":
    clean_docs()  # Wipe the slate clean to allow successful builds
    sync_images()  # Fetch the images
    optimise_images()  # Turn them into webp
    scan_for_challenges()  # Scan for challenges/headache notes
    css = load_theme_css(THEME_NAME)
    build_portfolio()  # Build HTML with webp links
    build_challenges_page(css)  # Build the challenges page with CSS theme
