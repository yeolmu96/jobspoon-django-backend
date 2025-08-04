from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import time

def crawl_wanted_jobs() -> list[dict]:
    print("[Crawler] 원티드 채용정보 수집 시작")

    companies = ["당근마켓", "비바리퍼블리카"]
    base_url = "https://www.wanted.co.kr/search?query="

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--headless')
    driver_path = "C:/tools/chromedriver/chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(3)

    results = []

    for company in companies:
        try:
            driver.get(base_url + company)
            time.sleep(3)
            job_cards = driver.find_elements(By.CLASS_NAME, "JobCard_container__FqChn")
            print(f"[원티드] {company} 공고 수: {len(job_cards)}")

            for idx, job in enumerate(job_cards[:10]):
                try:
                    link_elem = job.find_element(By.TAG_NAME, "a")
                    post_url = link_elem.get_attribute("href")
                    job_title = link_elem.text.strip()

                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(post_url)
                    time.sleep(2)

                    try:
                        desc_elem = driver.find_element(By.CLASS_NAME, "JobDescription_JobDescription__VWfcb")
                        description = desc_elem.text.strip()
                    except:
                        description = "(본문 없음)"

                    results.append({
                        "source": "원티드",
                        "company_name": company,
                        "job_title": job_title,
                        "post_url": post_url,
                        "posted_at": datetime.now(),
                        "description": description
                    })

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(1)

                except Exception as inner_e:
                    print(f"[원티드] {company} 공고 {idx + 1} 실패: {inner_e}")
                    continue

        except Exception as e:
            print(f"[원티드] {company} 크롤링 실패: {e}")
            continue

    driver.quit()
    return results
