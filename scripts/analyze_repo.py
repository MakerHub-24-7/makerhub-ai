import requests
import os

ORG_NAME = "MakerHub-24-7"
OUTPUT_FILE = "makerhub_org_report.md"

print("MakerHub Organization Analyzer Running")

url = f"https://api.github.com/orgs/{ORG_NAME}/repos"
response = requests.get(url)
repos = response.json()

report_lines = []
report_lines.append("# MakerHub Organization Report\n")

repo_count = len(repos)
report_lines.append(f"Total repositories: {repo_count}\n")

for repo in repos:
    name = repo["name"]
    stars = repo["stargazers_count"]
    forks = repo["forks_count"]

    report_lines.append(f"## {name}")
    report_lines.append(f"Stars: {stars}")
    report_lines.append(f"Forks: {forks}\n")

print("Repositories analyzed:", repo_count)

with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(report_lines))

print("Report generated:", OUTPUT_FILE)
