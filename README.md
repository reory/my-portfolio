# 🚀 Portfolio Generator (Static Site Engine)

A custom-built, lightweight Static Site Generator (SSG) designed to transform raw project documentation into a professional, hosted web portfolio. 

---

## 🛠️ The Architecture
This project serves as a "Project Factory," automating the deployment of my 22+ technical repositories into a unified web interface. 

- **Core Engine:** Python 3.13
- **Template Engine:** Jinja2
- **Markdown Parser:** Markdown2
- **Deployment:** GitHub Pages (Automated via `/docs` pipeline)

---

## 📂 Project Structure
- `build.py`: The automation engine that parses Markdown and renders HTML.
- `projects.json`: The "Source of Truth" inventory for all 22 projects.
- `layout.html`: The global design system (Stencil).
- `readmes/`: Raw input documentation gathered from individual project repos.
- `docs/`: The production-ready showroom containing the generated site.

---

## 🚀 How It Works
1. **Ingest:** The script reads metadata (titles, categories, thumbnails) from `projects.json`.
2. **Transform:** Markdown files are converted to HTML snippets.
3. **Inject:** Snippets are injected into the `layout.html` Jinja2 template.
4. **Publish:** The final site is written to the `/docs` folder for immediate GitHub Pages hosting.

---

## 📈 Featured Projects
This engine currently manages **22 repositories**, including:
- **Pydescope:** Static analysis & dependency mapping.
- **Smart File Agent:** Agentic AI pipelines.
- **Web Atlas:** Technical SEO visualization.
- *...and 19 more.*

---

* **Built by Roy Peters** 😁[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/roy-p-74980b382/)