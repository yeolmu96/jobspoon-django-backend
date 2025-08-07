from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time

def crawl_wanted_report() -> list[dict]:
    print("[Crawler] 원티드 기업 정보 수집 시작")

    companies = ["당근마켓", "비바리퍼블리카"]

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(3)

    results = []

    for company in companies:
        try:
            search_url = f"https://www.wanted.co.kr/search?query={company}"
            driver.get(search_url)
            time.sleep(2)

            overview = f"{company}의 원티드 등록 정보입니다."

            results.append({
                "source": "원티드",
                "company_name": company,
                "rating": None,
                "overview": overview,
                "welfare": "정보 없음",
                "salary_info": "정보 없음",
                "culture": "정보 없음",
                "review_summary": "정보 없음",
                "collected_at": datetime.now(),
            })

        except Exception as e:
            print(f"[원티드] {company} 처리 실패: {e}")
            continue

    driver.quit()
    return results
