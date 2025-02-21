import os
import time
import urllib
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def get_indeed_jobs_page(job_title, location, experience_filter):
    base_url = f'https://www.indeed.com/jobs?q={job_title}&l={location}&fromage=14&jt=fulltime&sort=date'
    
    if experience_filter == 'entry_level':
        # Update the URL for Entry Level
        base_url = f'https://www.indeed.com/jobs?q={job_title}&l={location}&sc=0kf%3Aexplvl(ENTRY_LEVEL)jt(fulltime)%3B&fromage=14'
    
    elif experience_filter == 'no_experience':
        # Update the URL for No Experience Required
        base_url = f'https://www.indeed.com/jobs?q={job_title}&l={location}&sc=0kf%3Aattr(D7S5D)jt(fulltime)%3B&fromage=14'

    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    "Chrome/91.0.4472.124 Safari/537.36"
    )
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("window-size=1920x1080")

    # Set the path for chromedriver
    # os.environ['PATH'] += os.pathsep + '/Users/rayidali/Downloads/'

    # Set up the Selenium driver without specifying the executable_path
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the updated URL
    driver.get(base_url)
    time.sleep(5)  # Adjust if necessary.

    # Extract page source and then close the browser
    page_source = driver.page_source
    driver.close()

    # Check first 500 characters of page source for debugging
    print(page_source[:500])

    return page_source



import re

def extract_jobs_from_indeed(page_source, experience_filter):
    soup = BeautifulSoup(page_source, "html.parser")
    
    # Identify the main container for jobs using a regular expression to match class patterns
    job_cards = soup.find_all("div", class_=re.compile(r'cardOutline tapItem'))
    
    # Print the number of job cards found
    print(f"Found {len(job_cards)} job cards.")

    jobs = []
    for job_card in job_cards:
        title_elem = job_card.find("h2", class_="jobTitle")
        title = title_elem.span.get("title") if title_elem else None
        link = f"https://www.indeed.com{title_elem.a.get('href')}" if title_elem and title_elem.a else None
        
        jobs.append({
            'title': title, 
            'link': link,
            'experience': "No Experience" if experience_filter == 'no_experience' else "Entry Level"  # Add experience level
        })
            
        # Print out the title, link, and experience level for each job
        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Experience: {jobs[-1]['experience']}\n")  # Print the experience level

    return jobs

def get_linkedin_jobs_page(job_title, location, experience_filter):
    base_url = f'https://www.linkedin.com/jobs/search?keywords={job_title}&location={location}&geoId=103644278&f_TPR=r604800&f_E=2&f_JT=F&position=1&pageNum=0'
    
    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    "Chrome/91.0.4472.124 Safari/537.36"
    )
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("window-size=1920x1080")
    # Set the path for chromedriver
    # os.environ['PATH'] += os.pathsep + '/Users/rayidali/Downloads/'

    # Set up the Selenium driver
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the updated URL
    driver.get(base_url)
    time.sleep(5)  # Adjust if necessary.

    # Extract page source and then close the browser
    page_source = driver.page_source
    driver.close()

    # Check first 500 characters of page source for debugging
    print(page_source[:500])

    return page_source

def extract_jobs_from_linkedin(page_source, experience_filter):
    jobs = [] 
    
    soup = BeautifulSoup(page_source, "html.parser")
    
    # Note: The element selection might need further tuning based on the actual structure of LinkedIn's job listings
    # job_cards = soup.find_all("div", class_="result-card job-result-card")
    job_cards = soup.find_all("div", class_=re.compile(r'base-card'))
    
    # Print the number of job cards found
    print(f"Found {len(job_cards)} job cards.")

    # jobs = []
    for job_card in job_cards:
        title_elem = job_card.find("a", class_="base-card__full-link")
        title = title_elem.text.strip() if title_elem else None
        link = title_elem.get("href") if title_elem else None
        
        jobs.append({
            'title': title, 
            'link': link,
            'experience': "Entry Level"  # We're assuming all are Entry Level as per the URL
        })
            
        # Print out the title, link, and experience level for each job
        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Experience: {jobs[-1]['experience']}\n")  # Print the experience level

    return jobs



from mailjet_rest import Client

def send_email_with_jobs(jobs):
    # Define the Mailjet credentials
    api_key = '5116a0fe9834a72004c39c8f8db4e895'
    api_secret = '08ec016410f504040b5890a424fbd48e'
    
    # Initialize the Mailjet client
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    # Prepare email content
    
    email_content = f"You have {len(jobs)} new job listings:\n\n"
    email_content += "\n".join([f"Title: {job['title']}\nLink: {job['link']}\nExperience: {job['experience']}\n" for job in jobs])


    # Mailjet send email request
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "rayidam@g.clemson.edu", # Your Mailjet registered email
                    "Name": "Job Alert"
                },
                "To": [
                    {
                        "Email": "rayidam@g.clemson.edu",
                        "Name": "Rayid Ali"
                    }
                ],
                "Subject": "Daily Job Alerts from Indeed and Linkedin",
                "TextPart": email_content
            }
        ]
    }

    result = mailjet.send.create(data=data)
    print(result.status_code, result.json())


def main():
    # LinkedIn scraping
    page_source_linkedin = get_linkedin_jobs_page("data scientist", "united states", 'entry_level')
    jobs_linkedin = extract_jobs_from_linkedin(page_source_linkedin, 'entry_level')

    # Indeed scraping
    page_source_entry_level = get_indeed_jobs_page("data scientist", "united states", 'entry_level')
    page_source_no_experience = get_indeed_jobs_page("data scientist", "united states", 'no_experience')
    jobs_entry_level = extract_jobs_from_indeed(page_source_entry_level, 'entry_level')
    jobs_no_experience = extract_jobs_from_indeed(page_source_no_experience, 'no_experience')

    # Combine job listings, ensuring there are no duplicates
    all_jobs = jobs_linkedin + jobs_entry_level + jobs_no_experience
    unique_jobs = [dict(t) for t in {tuple(sorted(job.items())) for job in all_jobs}]  # To ensure uniqueness

    # Check how many jobs were extracted
    print(f"Extracted {len(unique_jobs)} relevant jobs.")

    if unique_jobs:
        send_email_with_jobs(unique_jobs)
    else:
        print("No relevant jobs were found.")



# If running as a standalone script
if __name__ == '__main__':
    main()