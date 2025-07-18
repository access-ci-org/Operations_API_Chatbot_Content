# Converting REST API Responses into NLP-Friendly Text

This project contains a Python script that fetches resource data from the ACCESS Operations REST API and converts it into natural language summaries optimized for use with large language models (LLMs) and chatbots.

## Project Overview

The goal is to transform structured API JSON responses into easy-to-understand paragraphs that can be fed into AI-powered support chatbots for improved user experience.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- `requests` library

### Setup

1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd <repo_folder>

    Create a Python Virtual Environment and activate it:

python3 -m venv venv
source venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Running The Script

Run the Python script to fetch data and generate NLP-friendly summaries:

python converter.py

Or, if you need to recreate your virtual environment or install dependencies again:

# (Re)create the virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install requests

# Run the script
python converter.py

This will create a resources_summary.md file or multiple individual files in the project folder (inside the summaries subfolder) containing the processed content.
Output

    resources_summary.md: A Markdown file with a detailed summary of each resource returned from the API.

    Or: Multiple resource_*.md files in the summaries folder if the script is configured that way.

To view the generated files:

# View the combined summary file
cat resources_summary.md

# Or list the individual files
ls summaries/resource_*.md

# To view a specific individual file
cat summaries/resource_1_some_resource_name.md

Contact

For questions or contributions, contact Cameron @ cameron.kalon@gmail.com
NEXT STEPS

    Enhance text formatting and include more API fields

    Integrate generated summaries into the ACCESS support chatbot

    Prepare final presentation materials
