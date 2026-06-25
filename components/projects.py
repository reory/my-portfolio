import json
from collections import Counter
from loguru import logger


def load_projects():
    """Load and sort projects from projects.json"""

    try:
        with open("projects.json", "r", encoding="utf-8") as f:
            projects = json.load(f)
            projects.sort(key=lambda x: x["title"].lower())
            return projects
    except Exception as e:
        logger.error(f"Failed to load projects.json: {e}")
        return []


def scan_skills(projects):
    """Scan projects for skills and tags based on description and category"""

    # Scan each project's description and collect all tags for later
    # frequency analysis.
    all_skills = []
    for p in projects:
        tags = ["Python"]
        desc = p.get("desc", "").lower()
        cat = p.get("category", "").lower()

        if any(
            w in desc or w in cat
            for w in [
                "sql",
                "duckdb",
                "postgres",
                "mongodb",
                "sqlite",
                "sqlalchemy",
            ]
        ):
            tags.append("SQL and Databases")

        if any(
            w in desc or w in cat
            for w in ["pipeline", "etl", "polars", "scraping", "automation"]
        ):
            tags.append("Data Engineering")

        if any(
            w in desc or w in cat
            for w in [
                "django",
                "fastapi",
                "reflex",
                "kivy",
                "flet",
                "dash",
                "flask",
            ]
        ):
            tags.append("Full Stack")

        if any(
            w in desc or w in cat
            for w in ["agent", "ml", "xgboost", "ai", "intelligence"]
        ):
            tags.append("AI and Machine Learning")

        if any(
            w in desc or w in cat
            for w in ["forensics", "security", "password", "analysis"]
        ):
            tags.append("Digital Forensics and Security")

        p["tags"] = list(set(tags))
        all_skills.extend(p["tags"])

    # Count all skills and return the top six most frequent ones
    skill_counts = Counter(all_skills).most_common(6)
    return skill_counts
