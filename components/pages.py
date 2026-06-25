import os
import json
import markdown2
import re
from jinja2 import Template
from datetime import datetime
from loguru import logger


def build_project_pages(projects, custom_css):
    """Build HTML pages for each project"""

    built_projects = []
    for p in projects:
        if os.path.exists(p["md"]):
            try:
                with open(p["md"], "r", encoding="utf-8") as f:
                    content = f.read()

                    # FIX: Change .png to .webp inside the HTML content dynamically
                    content = re.sub(r"\.(png|jpg|jpeg)", ".webp", content)
                    content = content.replace("./images/", "images/")

                html_snippet = markdown2.markdown(
                    content, extras=["fenced-code-blocks", "tables"]
                )

                with open("templates/layout.html", "r", encoding="utf-8") as f:
                    template = Template(f.read())

                full_html = template.render(
                    project_name=p["title"],
                    project_content=html_snippet,
                    custom_css=custom_css,
                )

                output_path = os.path.join("docs", p["out"])
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(full_html)

                built_projects.append(p)
                logger.success(f"Published: {p['title']}")
            except Exception as e:
                logger.error(f"Error Processing {p['title']}: {e}")

    return built_projects


def generate_home_page(projects, custom_css, skills):
    """Build and render portfolio home page"""

    # Generate a readable date string and collect all project categories.
    formatted_date = datetime.now().strftime("%B %d, %Y")
    categories = sorted(list(set(p["category"] for p in projects)))

    try:
        with open("templates/home_template.html", "r", encoding="utf-8") as f:
            t = Template(f.read())

        # Ensure the home page thumbnails also point to .webp
        for p in projects:
            p["thumbnail"] = (
                p["thumbnail"]
                .replace(".png", ".webp")
                .replace(".jpg", ".webp")
            )

        # Pass project data into HTML files
        rendered_html = t.render(
            projects=projects,
            categories=categories,
            custom_css=custom_css,
            current_date=formatted_date,
            skills=skills,
        )
        with open("docs/index.html", "w", encoding="utf-8") as f:
            f.write(rendered_html)  # Write rendered HTML to output file
    except Exception as e:
        logger.error(f"Failed to generate home page: {e}")


def build_challenges_page(custom_css):
    """Assemble HTML for the Challenges portfolio section"""

    try:
        with open("challenges.json", "r", encoding="utf-8") as f:
            challenges = json.load(f)  # Load data from JSON file
        with open(
            "templates/challenges_template.html", "r", encoding="utf-8"
        ) as f:
            t = Template(f.read())  # Load and parse the HTML template
        rendered_html = t.render(challenges=challenges, custom_css=custom_css)
        with open("docs/challenges.html", "w", encoding="utf-8") as f:
            f.write(rendered_html)
    except Exception as e:
        logger.error(f"Failed to build challenges page: {e}")
