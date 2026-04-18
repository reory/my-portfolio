import json
import markdown2
from jinja2 import Template
from datetime import datetime
import os
import shutil  # Added for moving files
import re      # Added for fixing links
from loguru import logger
from PIL import Image
from collections import Counter

THEME_NAME = "slate.css"
logger.add("generator.log", rotation="1 MB")

def load_theme_css(theme_name):
    css_path = os.path.join("templates", "css", theme_name)
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Could not load theme {theme_name}: {e}")
        return ""

def sync_images():
    """Moves images from root /images to docs/images before optimization."""
    src = "images"
    dest = "docs/images"
    if os.path.exists(src):
        if not os.path.exists(dest):
            os.makedirs(dest)
        for f in os.listdir(src):
            shutil.copy(os.path.join(src, f), os.path.join(dest, f))
        logger.success("✅ Raw images synced to docs/images")

def build_portfolio():
    logger.info("🚀 Starting Portfolio Build Sequence...")
    if not os.path.exists("docs"):
        os.makedirs("docs")
    
    custom_css = load_theme_css(THEME_NAME)

    try:
        with open("projects.json", "r", encoding="utf-8") as f:
            projects = json.load(f)
            projects.sort(key=lambda x: x['title'].lower())
    except Exception as e:
        logger.error(f"Failed to load projects.json: {e}")
        return

    # Skill scanning
    all_skills = []
    for p in projects:
        tags = ["Python"]
        desc = p.get('desc', '').lower()
        cat = p.get('category', '').lower()
        if any(w in desc or w in cat for w in ['sql', 'duckdb', 'postgres', 'mongodb', 'sqlite', 'sqlalchemy']):
            tags.append("SQL and Databases")
        if any(w in desc or w in cat for w in ['pipeline', 'etl', 'polars', 'scraping', 'automation']):
            tags.append("Data Engineering")
        if any(w in desc or w in cat for w in ['django', 'fastapi', 'reflex', 'kivy', 'flet', 'dash', 'flask']):
            tags.append("Full Stack")
        if any(w in desc or w in cat for w in ['agent', 'ml', 'xgboost', 'ai', 'intelligence']):
            tags.append("AI and Machine Learning")
        if any(w in desc or w in cat for w in ['forensics', 'security', 'password', 'analysis']):
            tags.append("Digital Forensics and Security") # Fixed typo here

        p['tags'] = list(set(tags))
        all_skills.extend(p['tags'])

    skill_counts = Counter(all_skills).most_common(6)

    with open("templates/layout.html", "r", encoding="utf-8") as f:
        template = Template(f.read())

    built_projects = []
    for p in projects:
        if os.path.exists(p['md']):
            try:
                with open(p['md'], "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    # FIX: Change .png to .webp inside the HTML content dynamically
                    content = re.sub(r'\.(png|jpg|jpeg)', '.webp', content)
                    content = content.replace('./images/', 'images/')

                html_snippet = markdown2.markdown(
                    content, extras=["fenced-code-blocks", "tables"])

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

    generate_home_page(built_projects, custom_css, skill_counts)

def optimise_images():
    source_dir = "docs/images"
    if not os.path.exists(source_dir): 
        return

    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            old_path = os.path.join(source_dir, filename)
            base_name = os.path.splitext(filename)[0]
            new_path = os.path.join(source_dir, f"{base_name}.webp")

            try:
                with Image.open(old_path) as img:

                    # Resize images if too big for Portfolio page.
                    max_width = 800
                    if img.width > max_width:
                        w_percent = (max_width / float(img.width))
                        h_size = int((float(img.height) * float(w_percent)))

                        # Resize images
                        img = img.resize((
                            max_width, h_size), 
                            Image.Resampling.LANCZOS
                        )
                        logger.debug(f" Resized {filename} to 600px wide.")

                    # Save as webp
                    img.save(new_path, "WEBP", quality=80)

                # Clean up old file if it was removed as png/jpg
                if old_path != new_path:
                    os.remove(old_path)

            except Exception as e:
                logger.error(f"Failed to optimise {filename}: {e}")

def build_challenges_page(custom_css):
    try:
        with open("challenges.json", "r", encoding="utf-8") as f:
            challenges = json.load(f)
        with open("templates/challenges_template.html", "r", encoding="utf-8") as f:
            t = Template(f.read())
        rendered_html = t.render(challenges=challenges, custom_css=custom_css)
        with open("docs/challenges.html", "w", encoding="utf-8") as f:
            f.write(rendered_html)
    except Exception as e:
        logger.error(f"Failed to build challenges page: {e}")

def generate_home_page(projects, custom_css, skills):
    formatted_date = datetime.now().strftime("%B %d, %Y")
    categories = sorted(list(set(p['category'] for p in projects)))
    try:
        with open("templates/home_template.html", "r", encoding="utf-8") as f:
            t = Template(f.read())
        
        # Ensure the home page thumbnails also point to .webp
        for p in projects:
            p['thumbnail'] = p['thumbnail'].replace('.png', '.webp').replace('.jpg', '.webp')

        rendered_html = t.render(
            projects=projects, categories=categories, 
            custom_css=custom_css, current_date=formatted_date, skills=skills
        )
        with open("docs/index.html", "w", encoding="utf-8") as f:
            f.write(rendered_html)
    except Exception as e:
        logger.error(f"Failed to generate home page: {e}")

def clean_docs():
    """Removes all generated HTML files to ensure a fresh build"""
    if not os.path.exists("docs"):
        os.makedirs("docs")
        return

    for f in os.listdir("docs"):
        if f.endswith(".html"):
            os.remove(os.path.join("docs", f))
    logger.info("🧹 Successfully cleaned old HTML files from/docs")

if __name__ == "__main__":
    clean_docs()       # Wipe the slate clean
    sync_images()      # Get the images ready
    optimise_images()  # Turn them into webp
    css = load_theme_css(THEME_NAME)
    build_portfolio()  # 3. Generate HTML with webp links
    build_challenges_page(css)