# 📄 company/jobplanet_company.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time

def crawl_jobplanet_company_info() -> list[dict]:
    print("[Crawler] 잡플래닛 회사정보 수집 시작")

    company_info = {
        "당근마켓": "https://www.jobplanet.co.kr/companies/157816",
        "비바리퍼블리카": "https://www.jobplanet.co.kr/companies/999177"
    }

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(3)

    results = []

    for company, url in company_info.items():
        try:
            driver.get(url)
            time.sleep(3)
            try:
                rating = driver.find_element(By.CSS_SELECTOR, ".rate_point span").text.strip()
                overview = driver.find_element(By.CSS_SELECTOR, ".company_info .text").text.strip()
                description = f"[평점] {rating}\n[소개] {overview}"
            except:
                description = "(정보 없음)"

            results.append({
                "source": "잡플래닛",
                "company_name": company,
                "job_title": "회사 리뷰 및 개요",
                "post_url": url,
                "posted_at": datetime.now(),
                "description": description
            })

        except Exception as e:
            print(f"[잡플래닛] {company} 정보 크롤링 실패: {e}")
            continue

    driver.quit()
    return results