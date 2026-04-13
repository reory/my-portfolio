# This script will take a README and "print" it into a HTML template.

import json
import markdown2
from jinja2 import Template
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("generator.log"),
        logging.StreamHandler()
    ]
)

def build_portfolio():
    logging.info("Starting Portfolio Build Sequence..")

    if not os.path.exists("docs"):
        os.makedirs("docs")
        logging.info("Created missing / docs directory.")
    
    # Load JSON file of projects
    try:
        with open("projects.json", "r", encoding="utf-8") as f:
            projects = json.load(f)
            projects.sort(key=lambda x: x['title'].lower())
            logging.info(f"Loaded {len(projects)} projects from JSON")
    except Exception as e:
        logging.error(f"Failed to load projects.json: {e}")
        return

    # Load HTML stencil once
    with open("templates/layout.html", "r", encoding="utf-8") as f:
        template = Template(f.read())

    built_projects = []
    
    # Process every project in the JSON file
    for p in projects:
        # Check if the README file actually exists
        if os.path.exists(p['md']):
            try:
                with open(p['md'], "r", encoding="utf-8") as f:
                    html_snippet = markdown2.markdown(
                        f.read(), 
                        extras=["fenced-code-blocks", "tables"]
                    )

                # Render the specific project page
                full_html = template.render(
                    project_name=p['title'], 
                    project_content=html_snippet
                )

                # Save HTMl inside the docs folder for github
                output_path = os.path.join("docs", p['out'])
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(full_html)
                    
                built_projects.append(p)
                logging.info(f" Successfully Published: {p['title']}")
            except Exception as e:
                logging.error(f"Error Processing {p['title']}: {e}")
        else:
            # If you haven't downloaded the README yet, the script notifies you
            logging.warning(
                f"⚠️ Skipping {p['title']}: File {p['md']} not found.")

    generate_home_page(built_projects)

def generate_home_page(projects):

    logging.info("Generating home page from external template...")
    
    # Prepare the data
    categories = sorted(list(set(p['category'] for p in projects)))

    try:
        # Open the file where the HTML and other languages live
        with open("templates/home_template.html", "r", encoding="utf-8") as f:
            template_content = f.read()
        # Jinja 2
        t = Template(template_content)
        rendered_html = t.render(projects=projects, categories=categories)
        
        # Write final result to the docs folder
        with open("docs/index.html", "w", encoding="utf-8") as f:
            f.write(rendered_html)

        logging.info("Home Page (index.html) successfully generated in /docs")
    except Exception as e:
        logging.error(f"Failed to generate home page: {e}")

if __name__ == "__main__":
    build_portfolio()