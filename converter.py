"""
generate_resource_summaries.py

Pulls ACCESS Operations API data and converts it into NLP-friendly Markdown summaries.
Author: Cameron Jones
Email: cameron.kalon@gmail.com
Date: July 2025
"""

import requests


def fetch_api_data(url):
    """Fetch JSON data from the given API URL and return the parsed Python object."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API request failed: {e}")
        return None


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


def create_resource_summary(item, index):
    """Turn a single resource dict into a natural language Markdown summary."""
    short_name = item.get("short_name", "N/A")
    cider_type = item.get("cider_type", "N/A")
    affiliation = item.get("project_affiliation", "N/A")
    resource_name = item.get("resource_descriptive_name", "N/A")
    description = item.get("resource_description", "N/A")
    recommended_use = item.get("recommended_use", "N/A")
    access_description = item.get("access_description", "N/A")
    latest_status = item.get("latest_status", "N/A")
    status_begin = item.get("latest_status_begin", "N/A")
    status_end = item.get("latest_status_end", "N/A")
    org_name = item.get("organization_name", "N/A")
    org_url = item.get("organization_url", "N/A")

    # Handle features
    features = item.get("features", [])
    features_text = ""
    if features:
        features_text += "### Key Features:\n"
        for feat in features:
            fname = feat.get("name", "N/A")
            fdesc = feat.get("description", "N/A")
            fcat = feat.get("feature_category", "N/A")
            features_text += f"- **{fname}**: {fdesc} _(Category: {fcat})_\n"

    # Combine into Markdown
    summary = f"""## Resource #{index}: {resource_name}

**Project:** {short_name}  
**Type:** {cider_type}  
**Affiliation:** {affiliation}  

{resource_name} is a **{cider_type}** resource affiliated with **{affiliation}**.  
Description: *"{description}"*  
**Recommended use:** {recommended_use}.  
**Access details:** {access_description}.

**Current status:** "{latest_status}" from **{status_begin}** to **{status_end}**.  
Provided by: [{org_name}]({org_url})

{features_text}

---

"""

    return summary


def main():
    API_URL = "https://operations-api.access-ci.org/wh2/cider/v1/access-allocated/"
    print("[INFO] Fetching data from API...")

    data = fetch_api_data(API_URL)
    if not data:
        print("[ERROR] No data fetched. Exiting.")
        return

    records = extract_records(data)
    if not records:
        print("[ERROR] No resource records found. Exiting.")
        return

    print(f"[INFO] Found {len(records)} resources. Generating summaries...")

    output_file = "resources_summary.md"

    with open(output_file, "w", encoding="utf-8") as f:
        for idx, item in enumerate(records, start=1):
            summary = create_resource_summary(item, idx)
            f.write(summary)

    print(f"[SUCCESS] All summaries saved to {output_file}")


if __name__ == "__main__":
    main()
