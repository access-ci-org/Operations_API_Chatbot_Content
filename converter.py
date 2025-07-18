"""
generate_resource_summaries.py

Pulls ACCESS Operations API data and converts it into individual NLP-friendly Markdown summaries.
Author: Cameron Jones
Email: cameron.kalon@gmail.com
Date: July 2025
"""

# -------------------------
# Imports
# -------------------------

import requests  # For HTTP GET requests
import re        # For slugify
import os        # For directories & paths
from datetime import datetime  # For date+time-based folders

# -------------------------
# Fetch API data
# -------------------------

def fetch_api_data(url):
    """Fetch JSON data from the given API URL and return the parsed Python object."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API request failed: {e}")
        return None

# -------------------------
# Extract records list
# -------------------------

def extract_records(data):
    """Extract the list of resource records from the API response."""
    if isinstance(data, dict):
        return (
            data.get("data")
            or data.get("results")
            or data.get("items")
            or data.get("access_allocated")
            or []
        )
    elif isinstance(data, list):
        return data
    else:
        print(f"[ERROR] Unexpected response format: {type(data)}")
        return []

# -------------------------
# Safe slug creator
# -------------------------

def slugify(text):
    """Create a filesystem-safe slug from text."""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text.strip().lower())

# -------------------------
# Generate markdown content
# -------------------------

def create_resource_summary(item, index):
    """Generate a Markdown summary for a single resource."""

    # Extract main fields
    resource_name = item.get("resource_descriptive_name", "N/A")
    resource_type = item.get("cider_type", "Other")
    provider_name = item.get("organization_name", "N/A")
    provider_url = item.get("organization_url", "N/A")
    status = item.get("latest_status", "N/A").lower()
    status_begin = item.get("latest_status_begin", "N/A")
    affiliation = item.get("project_affiliation", "N/A")
    short_name = item.get("short_name", "N/A")

    recommended_use = item.get("recommended_use", "")
    description = item.get("resource_description", "")
    brief_purpose = recommended_use or description

    md_content = f"""### Resource Name: {resource_name}

**Type:** {resource_type.capitalize()}

**Provider:** {provider_name} ({provider_url})

**Status:** {status}, since {status_begin}

The {resource_name} ({short_name}) is a {resource_type} resource affiliated with {affiliation}, provided by {provider_name}. It entered its current status ("{status}") on {status_begin}.

"""

    if brief_purpose:
        md_content += f"{resource_name} supports scientific computing through {brief_purpose}. This resource is integrated into the broader ACCESS ecosystem and is intended to support national-scale research infrastructure.\n\n"

    # System Overview
    system_lines = []
    architecture = item.get("architecture", "")
    cpu_info = item.get("cpu", "")
    memory = item.get("memory", "")
    storage = item.get("storage", "")
    interconnects = item.get("interconnects", "")
    software_stack = item.get("software_stack", "")

    if architecture:
        system_lines.append(f"- **Architecture/Platform:** {architecture}")
    if cpu_info:
        system_lines.append(f"- **CPU:** {cpu_info}")
    if memory:
        system_lines.append(f"- **Memory:** {memory}")
    if storage:
        system_lines.append(f"- **Storage:** {storage}")
    if interconnects:
        system_lines.append(f"- **Interconnects:** {interconnects}")
    if software_stack:
        system_lines.append(f"- **Software Stack:** {software_stack}")

    if system_lines:
        md_content += "**System Overview:**\n\n" + "\n".join(system_lines) + "\n\n"

    # Recommended Use Cases
    if recommended_use:
        md_content += "**Recommended Use Cases:**\n\n" + recommended_use + "\n\n"

    # Access Instructions
    access_instructions = item.get("access_description", "")
    if access_instructions:
        md_content += "**Access Instructions:**\n\n" + access_instructions + "\n\n"

    # Features / Tags
    features = item.get("features", [])
    feature_lines = []
    for feat in features:
        fname = feat.get("name", "")
        if fname:
            feature_lines.append(f"- {fname}")
    if feature_lines:
        md_content += "**Key Features and Tags:**\n\n" + "\n".join(feature_lines) + "\n\n"

    # Integration Notes (optional)
    integration_notes = item.get("integration_notes", "")
    if integration_notes:
        md_content += "**Integration Notes:**\n\n" + integration_notes + "\n\n"

    md_content += "---\n"

    return md_content, slugify(resource_name)

# -------------------------
# Main execution block
# -------------------------

def main():
    API_URL = "https://operations-api.access-ci.org/wh2/cider/v1/access-allocated/"
    print("[INFO] Fetching data from API...")

    # Base output path
    base_path = "/run/media/deck/GF8S5/DOWNLOADS/Illinois Internship/Project Folder Rest APIs into text"

    # Create dynamic folder name with today's date and time
    now_str = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_dir = os.path.join(base_path, f"summaries_{now_str}")

    # Make sure the new dated+timed folder exists
    os.makedirs(output_dir, exist_ok=True)

    data = fetch_api_data(API_URL)
    if not data:
        print("[ERROR] No data fetched. Exiting.")
        return

    records = extract_records(data)
    if not records:
        print("[ERROR] No resource records found. Exiting.")
        return

    print(f"[INFO] Found {len(records)} resources. Generating individual summaries in '{output_dir}'...")

    for idx, item in enumerate(records, start=1):
        md_content, slug = create_resource_summary(item, idx)
        filename = os.path.join(output_dir, f"resource_{idx}_{slug}.md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"[INFO] Saved summary to {filename}")

    print(f"[SUCCESS] All individual summaries generated in '{output_dir}'.")

# -------------------------
# Run script
# -------------------------

if __name__ == "__main__":
    main()
