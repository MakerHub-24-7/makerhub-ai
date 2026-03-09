import requests
import os
from datetime import datetime

ORG_NAME = "MakerHub-24-7"
OUTPUT_DIR = "reports"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("MakerHub Knowledge Engine Running")

repos_url = f"https://api.github.com/orgs/{ORG_NAME}/repos"
repos = requests.get(repos_url).json()

repo_count = len(repos)

knowledge_entries = []

for repo in repos:

    repo_name = repo["name"]
    repo_api = f"https://api.github.com/repos/{ORG_NAME}/{repo_name}/contents"

    print(f"Scanning repo: {repo_name}")

    try:
        contents = requests.get(repo_api).json()
    except:
        continue

    for item in contents:

        if item["type"] == "file" and item["name"].lower().endswith(".md"):

            file_url = item["download_url"]

            try:
                text = requests.get(file_url).text
            except:
                continue

            preview = text[:300].replace("\n", " ")

            knowledge_entries.append(
                f"""
### Repository: {repo_name}
File: {item['name']}

Preview:
{preview}

---
"""
            )

report = f"""
# MakerHub Knowledge Report

Generated: {datetime.utcnow()}

Repositories scanned: {repo_count}

Total documentation files found: {len(knowledge_entries)}

---

## Documentation Knowledge Base

{''.join(knowledge_entries)}

"""

report_path = os.path.join(OUTPUT_DIR, "knowledge_report.md")

with open(report_path, "w") as f:
    f.write(report)

print("Knowledge report generated.")
