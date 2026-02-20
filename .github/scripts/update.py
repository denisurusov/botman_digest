import requests
import os
import re
from datetime import datetime
from pathlib import Path
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_URL = "https://api.x.ai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('GROK_API_KEY')}",
    "Content-Type": "application/json"
}

# Paths
root = Path(__file__).parent.parent.parent
raw_digest_dir = root / "docs" / "raw_digest"
digest_md_path = root / "docs" / "digest.md"
platforms_md_path = root / "docs" / "platforms.md"
update_summary_path = root / "docs" / "update_summary.md"

# Get latest daily digest
digest_files = list(raw_digest_dir.glob("daily-digest_*.md"))
if not digest_files:
    raise Exception("No daily digest files found")

# Sort by filename timestamp (YYYY-MM-DD_HH-MM)
latest_digest_file = max(digest_files, key=lambda x: x.stem.split('_')[1] + x.stem.split('_')[2])
with open(latest_digest_file, "r", encoding="utf-8") as f:
    latest_digest = f.read()

# Read current files
with open(digest_md_path, "r", encoding="utf-8") as f:
    current_digest = f.read()

with open(platforms_md_path, "r", encoding="utf-8") as f:
    current_platforms = f.read()

# ────────────────────────────────────────────────
#  Read prompts from files
# ────────────────────────────────────────────────

prompts_dir = root / "prompts"

digest_prompt_template = (prompts_dir / "update_digest.md").read_text(encoding="utf-8")
platforms_prompt_template = (prompts_dir / "update_platforms.md").read_text(encoding="utf-8")

# Prepare replacements
replacements = {
    "{{CURRENT_DIGEST}}": current_digest,
    "{{CURRENT_PLATFORMS}}": current_platforms,
    "{{LATEST_DIGEST}}": latest_digest,
    "{{LATEST_FILENAME}}": latest_digest_file.name,
}

# Build final prompts
digest_prompt = digest_prompt_template
platforms_prompt = platforms_prompt_template

for placeholder, value in replacements.items():
    digest_prompt = digest_prompt.replace(placeholder, value)
    platforms_prompt = platforms_prompt.replace(placeholder, value)

def clean_markdown_fences(content: str) -> str:
    """Removes ```markdown and ``` fences if present."""
    # Remove start fence (optionally with 'markdown')
    content = re.sub(r'^```(?:markdown)?\s*\n', '', content, flags=re.IGNORECASE)
    # Remove end fence
    content = re.sub(r'\n```\s*$', '', content)
    return content.strip()

def call_api(prompt: str, max_tokens: int = 20000) -> str:
    payload = {
        "model": "grok-4-1-fast-reasoning",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.2
    }

    try:
        r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=180)
        r.raise_for_status()
        raw_content = r.json()["choices"][0]["message"]["content"].strip()
        return clean_markdown_fences(raw_content)
    except requests.exceptions.SSLError:
        print("SSL error, retrying without verification...")
        r = requests.post(API_URL, headers=HEADERS, json=payload, verify=False, timeout=180)
        r.raise_for_status()
        raw_content = r.json()["choices"][0]["message"]["content"].strip()
        return clean_markdown_fences(raw_content)


# Make two separate calls
print("Updating digest.md...")
updated_digest = call_api(digest_prompt)

print("Updating platforms.md...")
updated_platforms = call_api(platforms_prompt, max_tokens=12000)

# Write updated files
with open(digest_md_path, "w", encoding="utf-8") as f:
    f.write(updated_digest)

with open(platforms_md_path, "w", encoding="utf-8") as f:
    f.write(updated_platforms)

# Minimal update summary - only essentials
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

summary_content = f"""Update executed: {timestamp}

Input file used:
{latest_digest_file.name}

(Full input digest content for reference follows)
{latest_digest}
"""

with open(update_summary_path, "w", encoding="utf-8") as f:
    f.write(summary_content)

print(f"Update finished. Summary written to: {update_summary_path}")

print(f"✅ Successfully updated both files using {latest_digest_file.name}")
