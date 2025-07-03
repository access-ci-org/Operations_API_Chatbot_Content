import requests

def main():
    url = "https://operations-api.access-ci.org/wh2/cider/v1/access-allocated/"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return

    # Inspect the top-level structure of data
    if isinstance(data, dict):
        # If data is a dictionary, look for key holding list of records
        records = data.get('data') or data.get('results') or data.get('items') or data.get('access_allocated') or []
    elif isinstance(data, list):
        records = data
    else:
        print("Unexpected data format:", type(data))
        return

    if not records:
        print("No records found in API response.")
        return

    first_item = records[0]

    output = f"""
Project: {first_item.get('short_name', 'N/A')}
Type: {first_item.get('cider_type', 'N/A')}
Affiliation: {first_item.get('project_affiliation', 'N/A')}
Resource: {first_item.get('resource_descriptive_name', 'N/A')}
Description: {first_item.get('resource_description', 'N/A')}
Recommended Use: {first_item.get('recommended_use', 'N/A')}
Access Description: {first_item.get('access_description', 'N/A')}
Latest Status: {first_item.get('latest_status', 'N/A')} 
Status Period: {first_item.get('latest_status_begin', 'N/A')} to {first_item.get('latest_status_end', 'N/A')}
Organization: {first_item.get('organization_name', 'N/A')} ({first_item.get('organization_url', 'N/A')})
"""

    print(output)

if __name__ == "__main__":
    main()
