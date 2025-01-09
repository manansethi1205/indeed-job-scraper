from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def indeed_scraper(job,location):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        path = "C:/Users/HP/OneDrive/Desktop/indeed-job-scraper/selenium usage/chromedriver.exe"
        service = ChromeService(executable_path=path)
        driver = webdriver.Chrome(service=service)
        driver.get("https:/in.indeed.com/?r=us")

        job_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "text-input-what"))
        )
        job_field.send_keys(f'{job}')
        sleep(1)
        location_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "text-input-where"))
        )
        location_field.send_keys(f'{location}')
        sleep(1)

        if job_field.get_attribute('value') != f"{job}":
            job_field.clear()  
            job_field.send_keys(f"{job}")

        driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton").click()

        # get the link to current webpage and then parse for jobs
        page_html = driver.page_source

        soup = BeautifulSoup(page_html,"html.parser")
        job_listings = soup.find_all("a", class_="jcs-JobTitle")
        job_data = []

        for job in job_listings:
            # Get job title and link
            job_title = job.get_text()
            job_link = "https://in.indeed.com" + job['href']
            print(f"Job Title: {job_title}\nJob Link: {job_link}\n")
            job_data.append({"Job Title": job_title, "Job Link": job_link})

    except Exception as e:
        print("Error occurred:",e)
    finally:    
        driver.quit()

    df = pd.DataFrame(job_data)
    df.to_excel("indeed_jobs.xlsx", index=False, engine='openpyxl')
    print("Job data has been saved to indeed_jobs.xlsx.")
