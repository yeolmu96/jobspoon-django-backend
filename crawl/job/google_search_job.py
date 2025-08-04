from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time

def crawl_google_search_jobs(keyword: str, site: str = "jobkorea.co.kr") -> list[dict]:
    print(f"[Crawler] Google 검색 기반 채용정보 수집: site:{site} {keyword}")
    query = f"site:{site} {keyword} 채용"
    search_url = f"https://www.google.com/search?q={query}"

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(3)

    driver.get(search_url)
    time.sleep(2)

    results = []
    items = driver.find_elements(By.CSS_SELECTOR, "div.g")
    for item in items:
        try:
            title = item.find_element(By.TAG_NAME, "h3").text
            link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
            desc = item.find_element(By.CLASS_NAME, "VwiC3b").text
            results.append({
                "source": f"Google via {site}",
                "company_name": keyword,
                "job_title": title,
                "post_url": link,
                "posted_at": datetime.now(),
                "description": desc
            })
        except:
            continue

    driver.quit()
    return results