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
    with open("layout.html", "r", encoding="utf-8") as f:
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

    categories = sorted(list(set(p['category'] for p in projects)))

    # Template for the homepage list
    home_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Portfolio</title>
        <style>
            body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; color: #333; }
            .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
            .card { border: 1px solid #ddd; padding: 15px; border-radius: 8px; transition: 0.3s; }
            .card:hover { border-color: #007bff; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            .tag { font-size: 0.8em; color: #666; text-transform: uppercase; }
            a { text-decoration: none; color: #007bff; font-weight: bold; }

            /* Style for the new filter UI*/
            .filter-nav { margin-bottom: 30px; background: #f4f4f4; padding: 15px; border-radius: 8px; }
            select { padding: 8px; border-radius: 4px; border: 1px solid #ccc; width: 200px; }
        </style>
    </head>
    <body>
        <h1>My Project Portfolio</h1>
        <p>A collection of my work in Python, Data Visualisation, Data Engineering, and AI.</p>
        
        <div class="filter-nav">
            <label for="catSelect"><strong>Filter by Category:</strong> </label>
            <select id="catSelect" onchange="filterSelection()">
                <option value="all">All Projects</option>
                {% for cat in categories %}
                <option value="{{ cat }}">{{ cat }}</option>
                {% endfor %}
            </select> 
        </div>     
        
        <div class="grid" id="projectGrid">
            {% for p in projects %}
            <div class="card" data-category="{{ p.category }}">
                {% if p.thumbnail %}
                <img src="{{ p.thumbnail }}" style="width:100%; height:150px; object-fit:cover; border-radius:4px; margin-bottom:10px;">
                {% endif %}
                
                <span class="tag">{{ p.category }}</span>
                <h3>{{ p.title }}</h3>
                <p>{{ p.desc }}</p>
                <a href="{{ p.out }}">View Project →</a>
            </div>
            {% endfor %}
        </div>

        <script>
        function filterSelection() {
            var input = document.getElementById("catSelect");
            var filter = input.value;
            var cards = document.getElementsByClassName("card");

            for (var i = 0; i < cards.length; i++) {
                var category = cards[i].getAttribute("data-category");
                if (filter === "all" || category === filter) {
                    cards[i].style.display = "";
                } else {
                    cards[i].style.display = "none";
                }
            }
        }
        </script>
    </body>
    </html>
    """
    try:
        t = Template(home_template)
        with open("docs/index.html", "w", encoding="utf-8") as f:
            f.write(t.render(projects=projects, categories=categories))
        logging.info("Home Page (index.html) successfully generated in /docs")
    except Exception as e:
        logging.error(f"Failed to generate home page: {e}")

if __name__ == "__main__":
    build_portfolio()