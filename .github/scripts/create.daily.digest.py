import requests
import os
from datetime import datetime
from pathlib import Path
import urllib3

# Disable SSL warnings if verification is disabled (not recommended for production)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_URL = "https://api.x.ai/v1/chat/completions"  # Updated to correct URL
HEADERS = {
    "Authorization": f"Bearer {os.getenv('GROK_API_KEY')}",
    "Content-Type": "application/json"
}

# Read prompt from file
PROMPT_FILE = Path(__file__).parent.parent.parent / "prompts" / "create_daily.digest.md"
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    PROMPT_TEMPLATE = f.read()

# Format prompt with current date
prompt_content = f"{PROMPT_TEMPLATE}\n\nGenerate digest for: {datetime.now().strftime('%Y-%m-%d')}"

try:
    # Try with SSL verification first
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={
            "model": "grok-4-1-fast-reasoning",
            "messages": [{"role": "user", "content": prompt_content}],
            "max_tokens": 16000,
            "temperature": 0.7
        },
        timeout=90
    )
except requests.exceptions.SSLError as e:
    print(f"SSL verification failed: {e}")
    print("Retrying without SSL verification (not recommended for production)...")

    # Retry without SSL verification
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={
            "model": "grok-4-1-fast-reasoning",
            "messages": [{"role": "user", "content": prompt_content}],
            "max_tokens": 16000,
            "temperature": 0.7
        },
        verify=False,  # Disable SSL verification
        timeout=00
    )

if response.status_code == 200:
    digest = response.json()["choices"][0]["message"]["content"]

    # Create filename with timestamp: YYYY-MM-DD_HH-MM
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    filename = f"daily-digest_{timestamp}.md"

    # Save to docs/raw_digest directory
    output_dir = Path(__file__).parent.parent.parent / "docs" / "raw_digest"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / filename

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(digest)

    print(f"Digest saved successfully to: {output_file}")
else:
    raise Exception(f"API error ({response.status_code}): {response.text}")
