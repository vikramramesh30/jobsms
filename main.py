import requests
from bs4 import BeautifulSoup
import markdown


# resp = requests.post('https://textbelt.com/text', {
#   'phone': '(609) 933-4711',
#   'message': 'Hello world',
#   'key': 'fbb484a78a6734771867e6d7720bc41713def1c44OdyDS5MRqZxl5MevaxCA1DrS',
# })

import requests
from bs4 import BeautifulSoup

# URL of the GitHub README page
url = "https://raw.githubusercontent.com/Ouckah/Summer2025-Internships/main/README.md"

# Fetch the content from the URL
response = requests.get(url)
content = response.text

# Parse the content with BeautifulSoup
soup = BeautifulSoup(content, "html.parser")

# Initialize an empty list to store job postings
job_postings = []

# Find the table in the content
table_start = content.find("| Company | Role | Location | Application/Link | Date Posted |")
table_end = content.find("<!-- Please leave a one line gap between this and the table TABLE_END (DO NOT CHANGE THIS LINE) -->")

# Extract the table content
table_content = content[table_start:table_end]

# Split the table into rows
rows = table_content.split("\n")

# Extract the job postings from the rows
for row in rows[2:]:  # Skip the header rows
    columns = row.split("|")
    if len(columns) > 1:
        company = columns[1].strip()
        role = columns[2].strip()
        date_posted = columns[5].strip()
        job_postings.append({"date": date_posted, "company": company, "role": role})

# Print the job postings
for job in job_postings:
    print(f"Date: {job['date']}, Company: {job['company']}, Role: {job['role']}")