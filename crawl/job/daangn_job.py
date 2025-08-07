from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time

def crawl_daangn_jobs() -> list[dict]:
    print("[Crawler] 당근 채용정보 수집 시작")

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # ← 개발 중에는 주석 처리
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(3)
    driver.get("https://about.daangn.com/jobs")

    results = []

    try:
        job_cards = driver.find_elements(By.CLASS_NAME, "JobCard_className__xv8mQ")
        print(f"[당근] 공고 수: {len(job_cards)}")

        for idx, job in enumerate(job_cards):
            try:
                link_elem = job.find_element(By.TAG_NAME, "a")
                post_url = link_elem.get_attribute("href")
                job_title = link_elem.text.strip()

                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(post_url)
                time.sleep(2)

                try:
                    desc_elem = driver.find_element(By.CLASS_NAME, "JobDescription_className__AjtJq")
                    description = desc_elem.text.strip()
                except:
                    description = "(본문 없음)"

                results.append({
                    "source": "당근",
                    "company_name": "당근마켓",
                    "job_title": job_title,
                    "post_url": post_url,
                    "posted_at": datetime.now(),
                    "description": description
                })

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)

            except Exception as e:
                print(f"[당근] 공고 {idx+1} 실패: {e}")
                continue

    finally:
        driver.quit()

    return results
