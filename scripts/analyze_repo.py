import requests
import os
from datetime import datetime

ORG_NAME = "MakerHub-24-7"

REPORT_DIR = "reports"
PROMPT_DIR = "prompts"

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(PROMPT_DIR, exist_ok=True)

print("MakerHub Knowledge Engine Running")

repos_url = f"https://api.github.com/orgs/{ORG_NAME}/repos"
repos = requests.get(repos_url).json()

repo_count = len(repos)

knowledge_entries = []
prompt_entries = []

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
                f"| {repo_name} | {item['name']} | {preview} |"
            )

# scan local prompt directory
for root, dirs, files in os.walk(PROMPT_DIR):
    for file in files:
        if file.endswith(".md"):
            prompt_entries.append(f"| {file} | {root} |")

# knowledge report
knowledge_report = f"""
# MakerHub Knowledge Report

Generated: {datetime.utcnow()}

Repositories scanned: {repo_count}

---

| Repository | File | Preview |
|---|---|---|
{chr(10).join(knowledge_entries)}
"""

with open(os.path.join(REPORT_DIR, "knowledge_report.md"), "w") as f:
    f.write(knowledge_report)

# prompt index
prompt_report = f"""
# MakerHub Prompt Index

Generated: {datetime.utcnow()}

| Prompt | Location |
|---|---|
{chr(10).join(prompt_entries)}
"""

with open(os.path.join(REPORT_DIR, "prompt_index.md"), "w") as f:
    f.write(prompt_report)

print("Reports generated")
