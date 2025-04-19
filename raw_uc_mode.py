"""UC Mode has PyAutoGUI methods for CAPTCHA-bypass."""

from seleniumbase import SB
from scrapy.selector import Selector

old_jobs = []
# with open("jobs.txt", 'r') as job_reader:
#     old_jobs = job_reader.read().splitlines()

new_jobs = []
jobs_to_sent = []

with SB(uc=True, incognito=True, test=True) as sb:
    url = (
        "https://www.upwork.com/nx/search/jobs/?amount=-20&nbs=1"
        "&q=%28scraping%20OR%20automation%20OR%20extraction%29"
        "&sort=recency&t=1"
    )
    sb.activate_cdp_mode(url)
    sb.uc_gui_click_captcha()
    sb.sleep(10)
    page_source = sb.get_page_source()
    selector = Selector(text=page_source)
    job_elements = selector.css('article')

    for job_element in job_elements:
        posted_date = job_element.css(
            'small[data-test="job-pubilshed-date"] span::text'
        ).getall()
        posted_date = " ".join(posted_date).strip()

        title = job_element.css(
            'a[data-test="job-tile-title-link UpLink"]::text'
        ).get('')
        title = title.strip() if title else "No title available"

        url = job_element.css(
            'a[data-test="job-tile-title-link UpLink"]::attr(href)'
        ).get('')

        job_type = job_element.css(
            'li[data-test="job-type-label"] strong::text'
        ).get()

        experience_level = job_element.css(
            'li[data-test="experience-level"] strong::text'
        ).get()

        budget = job_element.css(
            'li[data-test="is-fixed-price"] strong::text'
        ).getall()
        budget = " ".join(budget).strip()

        description = "".join([
            i.strip() for i in job_element.css(
                'div[data-test="UpCLineClamp JobDescription"] p::text'
            ).getall() if i.strip()
        ])
        description = (
            description.strip()
            if description
            else "No description available"
        )

        if url not in old_jobs:
            new_jobs.append(str(url))
            job = {
                "Posted Date": posted_date,
                "Job Title": title,
                "Job URL": f"https://www.upwork.com{url}",
                "Job Type": job_type,
                "Experience Level": experience_level,
                "Estimated Budget": budget,
                "Description": description,
            }
            print(job)
            print("*" * 40)
