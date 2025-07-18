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


## Create A Python Virtual Environment And Activate It
python3 -m venv venv
source venv/bin/activate


## Install Dependencies 
pip install -r requirements.txt


## Running The Script
Run the Python script to fetch data and generate NLP-friendly summaries:

python converter.py

#OR 

# If this doesn't work use:
# 
# python3 -m venv venv         # only if I haven't created venv yet
source venv/bin/activate
pip install requests         # only once or if dependencies change
python converter.py


This will create a summary.md file in the project folder containing the processed content.
Output

resources_summary.md: A Markdown file with a detailed summary of each resource returned from the API.

#To open the generated file use this:
cat resources_summary.md


# OR to list the indidual files use:
ls resource_*.md

#To open a specific folder use:

cat resource_1_some_resource_name.md (This is jus an example name, you have to type in the file name yourself)


## Contact

For questions or contributions, contact Cameron @ cameron.kalon@gmail.com


## NEXT STEPS

Enhance text formatting and include more API fields

Integrate generated summaries into the ACCESS support chatbot

Prepare final presentation materials
