from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup

def indeed_scraper(job,location):
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    path = "C:/Users/Manan Sethi/OneDrive/Desktop/projects/selenium usage/chromedriver.exe"
    service = ChromeService(executable_path=path)
    driver = webdriver.Chrome(service=service)
    driver.get("https:/in.indeed.com/?r=us")

    job_field = driver.find_element(By.ID, "text-input-what")
    job_field.send_keys(f'{job}')
    sleep(1)
    driver.find_element(By.ID, "text-input-where").send_keys(f'{location}')
    sleep(1)

    if job_field.get_attribute('value') != f"{job}":
        job_field.clear()  
        job_field.send_keys(f"{job}")

    driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton").click()

    # get the link to current webpage and then parse for jobs
    page_html = driver.page_source

    soup = BeautifulSoup(page_html,"html.parser")
    divs = soup.find_all("div", class_="css-dekpa e37uo190") # to get all the suitable div tags

    for div in divs:
        span = div.find("span") # to find all the spans in the divs we looked for
        if span:
            print(span.get_text()) #to print the text contained in the spans
        a_tag = div.find("a")  
        if a_tag and a_tag.has_attr('href'):
            final_link = "https://in.indeed.com/"+a_tag['href']
            print(final_link)

    driver.quit()

