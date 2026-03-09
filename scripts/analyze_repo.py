import os

print("MakerHub AI Analyzer Running")

documentation_files = []

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".md"):
            documentation_files.append(file)

print("Documentation files discovered:")

for doc in documentation_files:
    print("-", doc)

print("Analysis complete")
