from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time

def crawl_jobkorea_report() -> list[dict]:
    print("[Crawler] 잡코리아 기업 정보 수집 시작")

    companies = ["당근마켓", "비바리퍼블리카"]

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(3)

    results = []

    for name in companies:
        try:
            query = f"https://www.jobkorea.co.kr/Search/?stext={name}"
            driver.get(query)
            time.sleep(2)

            overview = f"{name}의 잡코리아 등록 정보입니다."

            results.append({
                "source": "잡코리아",
                "company_name": name,
                "rating": None,
                "overview": overview,
                "welfare": "정보 없음",
                "salary_info": "정보 없음",
                "culture": "정보 없음",
                "review_summary": "정보 없음",
                "collected_at": datetime.now(),
            })

        except Exception as e:
            print(f"[잡코리아] {name} 처리 실패: {e}")
            continue

    driver.quit()
    return results
