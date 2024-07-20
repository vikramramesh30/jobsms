import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import schedule
import time

def send_sms(phone, message, api_key):
    requests.post('https://textbelt.com/text', {
      'phone': phone,
      'message': message,
      'key' : api_key,
    })

def fetch_job_postings(url):
    # Fetch the content from the URL
    response = requests.get(url)
    content = response.text

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

    return job_postings

def check_for_new_postings(url):
    job_postings = fetch_job_postings(url)

    today = datetime.now().strftime("%b %d")

    for job in job_postings:
        if job['date'] == today:
            message = f"New Job Posting!\nDate: {job['date']}\nCompany: {job['company']}\nRole: {job['role']}"

            load_dotenv()

            phone_number = os.getenv("PHONE_NUMBER")
            api_key = os.getenv("API_KEY")
            
            response = send_sms(phone_number, message, api_key)
            print(response)

if __name__=="__main__": 
    print("SMS Internship Program Enabled")
    check_for_new_postings("https://raw.githubusercontent.com/Ouckah/Summer2025-Internships/main/README.md") 

schedule.every(5).minutes.do(check_for_new_postings)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)