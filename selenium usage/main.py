from indeed_scraper import indeed_scraper

job = input("Enter the job you are looking for: ")
location = input("Enter where you are looking for the above job: ")
indeed_scraper(job=job,location=location)