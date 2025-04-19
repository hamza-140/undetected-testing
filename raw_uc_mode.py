"""UC Mode has PyAutoGUI methods for CAPTCHA-bypass."""


from seleniumbase import SB
from scrapy.selector import Selector
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
old_jobs = []
# with open("jobs.txt", 'r') as job_reader:
#     old_jobs = job_reader.read().splitlines()
new_jobs = []
jobs_to_sent = []
with SB(uc=True, incognito=True, test=True) as sb:
    url = "https://www.upwork.com/nx/search/jobs/?amount=-20&nbs=1&q=%28scraping%20OR%20automation%20OR%20extraction%29&sort=recency&t=1"
    sb.activate_cdp_mode(url)
    sb.uc_gui_click_captcha()
    sb.sleep(10)      
    page_source = sb.get_page_source()
    selector = Selector(text=page_source)
    job_elements = selector.css('article')
    for job_element in job_elements:
        posted_date = job_element.css('small[data-test="job-pubilshed-date"] span::text').getall()
        posted_date = " ".join(posted_date).strip()
        title = job_element.css('a[data-test="job-tile-title-link UpLink"]::text').get('')
        if title: 
            title = title.strip()
        else:
            title = "No title available"  
        url = job_element.css('a[data-test="job-tile-title-link UpLink"]::attr(href)').get('')
        job_type = job_element.css('li[data-test="job-type-label"] strong::text').get()
        experience_level = job_element.css('li[data-test="experience-level"] strong::text').get()
        budget = job_element.css('li[data-test="is-fixed-price"] strong::text').getall()
        budget = " ".join(budget).strip()
        description = "".join([i.strip() for i in job_element.css('div[data-test="UpCLineClamp JobDescription"] p::text').getall() if i.strip()])
        if description:  
            description = description.strip()
        else:
            description = "No description available"
        if url not in old_jobs:
            new_jobs.append(str(url))
            job = dict()  
            job["Posted Date"] = posted_date
            job["Job Title"] = title
            job["Job URL"] = f"https://www.upwork.com{url}"
            job["Job Type"] = job_type
            job["Experience Level"] = experience_level
            job["Estimated Budget"] = budget
            job["Description"] = description
            print(job)
            print("*"*40)