# This script will take a README and "print" it into a HTML template.

import json
import markdown2
from jinja2 import Template
from datetime import datetime
import os
from loguru import logger
from PIL import Image

THEME_NAME = "slate.css"

# Configure Loguru to write to a file and the console
logger.add("generator.log", rotation="1 MB")

def load_theme_css(theme_name):
    """Reads the CSS file from the templates folder."""

    css_path = os.path.join("templates", "css", theme_name)
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            logger.info(f"🎨 Applying theme: {theme_name}")
            return f.read()
    except Exception as e:
        logger.error(f"Could not load theme {theme_name}: {e}")
        return ""

def build_portfolio():

    logger.info("🚀 Starting Portfolio Build Sequence...")

    if not os.path.exists("docs"):
        os.makedirs("docs")
        logger.info("Created missing /docs directory.")
    
    # Load CSS content once to inject into all pages
    custom_css = load_theme_css(THEME_NAME)

    # Load JSON file of projects
    try:
        with open("projects.json", "r", encoding="utf-8") as f:
            projects = json.load(f)
            projects.sort(key=lambda x: x['title'].lower())
            logger.info(f"📦 Loaded {len(projects)} projects from JSON")
    except Exception as e:
        logger.error(f"Failed to load projects.json: {e}")
        return

    # Load Project Page Template (layout.html)
    with open("templates/layout.html", "r", encoding="utf-8") as f:
        template = Template(f.read())

    built_projects = []
    
    for p in projects:
        if os.path.exists(p['md']):
            try:
                with open(p['md'], "r", encoding="utf-8") as f:
                    html_snippet = markdown2.markdown(
                        f.read(), 
                        extras=["fenced-code-blocks", "tables"]
                    )

                # Pass custom_css to the template
                full_html = template.render(
                    project_name=p['title'], 
                    project_content=html_snippet,
                    custom_css=custom_css 
                )

                output_path = os.path.join("docs", p['out'])
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(full_html)
                    
                built_projects.append(p)
                logger.success(f"Published: {p['title']}")
            except Exception as e:
                logger.error(f"Error Processing {p['title']}: {e}")
        else:
            logger.warning(f"Skipping {p['title']}: {p['md']} not found.")

    generate_home_page(built_projects, custom_css)

def optimise_images():
    """Shrink images for web performance."""

    source_dir = "docs/images"

    if not os.path.exists(source_dir):
        logger.error(f"❌ Error: The folder {source_dir} does not exist!")
        return

    logger.info("🚀 Starting image optmisation..")

    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            img_path = os.path.join(source_dir, filename)

            try:
                with Image.open(img_path) as img:
                    img = img.convert("RGB")

                # Resize image if too big - keep aspect ratio
                max_width = 800
                if img.width > max_width:
                    w_percent = (max_width / float(img.width))
                    h_size = int((float(img.height) * float(w_percent)))
                    img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)

                # Save with optimisation (80 is a good number for optimisation)
                img.save(img_path, "JPEG", optimize=True, quality=80)
                logger.debug(f"Compressed: {filename}")

            except Exception as e:
                logger.error(f"Failed to optimise {filename}: {e}")

    logger.success("🖼️ Image crunching complete!")

def generate_home_page(projects, custom_css):

    logger.info("🏠 Generating home page...")

    formatted_date = datetime.now().strftime("%B %d, %Y")
    
    categories = sorted(list(set(p['category'] for p in projects)))

    try:
        with open("templates/home_template.html", "r", encoding="utf-8") as f:
            template_content = f.read()
        
        t = Template(template_content)
        # Pass custom_css here
        rendered_html = t.render(
            projects=projects, 
            categories=categories, 
            custom_css=custom_css,
            current_date=formatted_date
        )
        
        with open("docs/index.html", "w", encoding="utf-8") as f:
            f.write(rendered_html)

        logger.success(f"Home Page generated with date: {formatted_date}")
    except Exception as e:
        logger.error(f"Failed to generate home page: {e}")

if __name__ == "__main__":
    # Shrink the images with correct aspect ratio
    optimise_images()
    # Build the portfolio HTML page
    build_portfolio()