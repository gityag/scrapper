import requests
from bs4 import BeautifulSoup
import csv

page_url = "https://remote.co/remote-jobs/data-science/"

def get_content(url):
    response = requests.get(url)
    if response.status_code == 200:
    # Page content is stored in response.text
        print("The corresponding page fetched successfully!")
    else:
        response.raise_for_status()
        print("Error fetching homepage:", response.status_code)
    return BeautifulSoup(response.content, "html.parser")

def extract_job_links(soup):
    job_links = []
    for link in soup.find_all("a", class_="card m-0 border-left-0 border-right-0 border-top-0 border-bottom"):
        job_links.append(link["href"])
    return job_links

soup = get_content(page_url)
# Print the extracted links
job_links = extract_job_links(soup)
if job_links:
    print("Extracted job links:")
    for link in job_links:
        print(link)
else:
    print("No job links found.")

def extract_job_details(soup, job_links):
    job_data = []
    for link in job_links:
        # prepend base url
        base_url = "https://remote.co/"
        if not link.startswith("http"):
            link = f"{base_url}{link}"
        # soup object that has html content
        job_soup = get_content(link)

        job_title = job_soup.find("h1", class_ = "font-weight-bold").text.strip()

        experience_sentences = []
        for paragraph in job_soup.find_all("p"):
            text = paragraph.text.strip()
            if "experience" in text.lower():
                experience_sentences.append(text)

        job_data.append({
            "title": job_title,
            "experience_sentences": experience_sentences
        })

    return job_data

with open("extracted_jobs.csv", "w", newline = "") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Job Title", "Experience Sentences"])
    for job in extract_job_details(soup, job_links):
        writer.writerow([job["title"], ":".join(job["experience_sentences"])])
