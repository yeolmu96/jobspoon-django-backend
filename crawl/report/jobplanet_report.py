from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time

def crawl_jobplanet_report() -> list[dict]:
    print("[Crawler] 잡플래닛 기업 정보 수집 시작")

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
            time.sleep(2)

            try:
                rating = driver.find_element(By.CSS_SELECTOR, ".rate_point span").text.strip()
            except:
                rating = None

            try:
                overview = driver.find_element(By.CSS_SELECTOR, ".company_info .text").text.strip()
            except:
                overview = ""

            results.append({
                "source": "잡플래닛",
                "company_name": company,
                "rating": rating,
                "overview": overview,
                "welfare": "복지 좋음",
                "salary_info": "업계 평균 이상",
                "culture": "자율적 분위기",
                "review_summary": "좋아요: 성장 가능성 / 아쉬움: 연봉",
                "collected_at": datetime.now(),
            })

        except Exception as e:
            print(f"[잡플래닛] {company} 처리 실패: {e}")
            continue

    driver.quit()
    return results