"""
PORTFOLIO CHALLENGE SCANNER UTILITY
WHAT IT DOES:
This script acts as an automated ingestion engine for the developer portfolio.
It recursively walks through designated workspace directories looking for specific
structured documentation tags inside Python source files:
    - # [PORTFOLIO_PROJECT]
    - # [PORTFOLIO_CHALLENGE]
    - # [PORTFOLIO_DESCRIPTION]
    - # [PORTFOLIO_SOLUTION]

It extracts these code-level notes, groups them into unified challenge objects,
handles automated deduplication so historical data is protected,
injects a default status of "Resolved", and appends the new records directly into
the central 'challenges.json' file.

WHY IT EXISTS:
To completely eliminate the friction of manual JSON data entry.
By allowing you to capture engineering roadblocks and solutions directly behind
standard comment hashes (#) while you are actively coding and debugging,
this utility transforms portfolio maintenance into a completely hands-free
byproduct of your natural developer workflow.
"""

import os
import json
from loguru import logger

# Add the paths to the external project folders you want Python to scan.
TARGET_DIRECTORIES = [
    "C:/Users/Admin/Desktop/code",
]

CHALLENGES_FILE = "challenges.json"


def scan_for_challenges():
    """
    Traverses target folders,
    parses files for portfolio tags, and updates challenges.json"""
    logger.info(
        "🔍 Scanning external projects for fresh developer headaches..."
    )

    new_challenges = []
    current_entry = None

    # Walk through every folder and file in your target directories
    for directory in TARGET_DIRECTORIES:
        if not os.path.exists(directory):
            logger.warning(f"⚠️ Target directory not found: {directory}")
            continue

        for root, dirs, files in os.walk(directory):
            # Skip common junk/virtual environment folders to keep it lightning fast
            if any(
                junk in root
                for junk in [
                    "venv",
                    ".venv",
                    "__pycache__",
                    ".git",
                    "node_modules",
                ]
            ):
                continue

            for file in files:

                # GUARDRAILS: Skip the scanner script itself
                # so it doesn't read its own code!
                if file == "scanner.py":
                    continue

                if file.endswith(".py"):
                    file_path = os.path.join(root, file)

                    try:
                        with open(
                            file_path, "r", encoding="utf-8", errors="ignore"
                        ) as f:
                            for line in f:
                                line_str = line.strip()

                                # GUARDRAILS: Only look at lines that are actual
                                # Python comments
                                if not line_str.startswith("#"):
                                    continue

                                # If found a Project tag,
                                # start a brand new challenge object
                                if "[PORTFOLIO_PROJECT]" in line_str:
                                    if (
                                        current_entry
                                        and current_entry.get("project")
                                        and current_entry.get("challenge")
                                    ):
                                        new_challenges.append(current_entry)

                                    current_entry = {
                                        "project": line_str.split(
                                            "[PORTFOLIO_PROJECT]"
                                        )[-1].strip(),
                                        "challenge": "",
                                        "description": "",
                                        "solution": "",
                                        "status": "Resolved",
                                    }

                                # EXACT MATCHING LOOKUPS HAPPEN HERE:
                                elif current_entry:
                                    if "[PORTFOLIO_CHALLENGE]" in line_str:
                                        current_entry["challenge"] = (
                                            line_str.split(
                                                "[PORTFOLIO_CHALLENGE]"
                                            )[-1].strip()
                                        )
                                    elif "[PORTFOLIO_DESCRIPTION]" in line_str:
                                        current_entry["description"] = (
                                            line_str.split(
                                                "[PORTFOLIO_DESCRIPTION]"
                                            )[-1].strip()
                                        )
                                    elif "[PORTFOLIO_SOLUTION]" in line_str:
                                        current_entry["solution"] = (
                                            line_str.split(
                                                "[PORTFOLIO_SOLUTION]"
                                            )[-1].strip()
                                        )

                    except Exception as e:
                        logger.error(
                            f"❌ Failed reading file {file_path}: {e}"
                        )

    # Catch the very last entry remaining in memory
    if (
        current_entry
        and current_entry.get("project")
        and current_entry.get("challenge")
    ):
        new_challenges.append(current_entry)

    if not new_challenges:
        logger.info("⏸️ No new code tags found during this scan.")
        return

    # Read existing challenges so script dosen't accidentally wipe out old data
    existing_challenges = []
    if os.path.exists(CHALLENGES_FILE):
        try:
            with open(CHALLENGES_FILE, "r", encoding="utf-8") as f:
                existing_challenges = json.load(f)
        except Exception:
            existing_challenges = []

    # Deduplicate - Ignore entries already pulled in before
    existing_keys = {
        (c["project"], c["challenge"]) for c in existing_challenges
    }
    added_count = 0

    for item in new_challenges:
        if (item["project"], item["challenge"]) not in existing_keys:
            existing_challenges.append(item)
            added_count += 1
            logger.success(
                f"✨ Found New Challenge: {item['project']} -> {item['challenge']}"
            )

    # Write back to the central challenges.json file
    if added_count > 0:
        try:
            with open(CHALLENGES_FILE, "w", encoding="utf-8") as f:
                json.dump(existing_challenges, f, indent=4)
            logger.success(
                f"💾 Successfully compiled and updated {CHALLENGES_FILE} with {added_count} new item(s)!"
            )
        except Exception as e:
            logger.error(f"❌ Failed writing to json file: {e}")
    else:
        logger.info("✅ challenges.json is already up to date.")
