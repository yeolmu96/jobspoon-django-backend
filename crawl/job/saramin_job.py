from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time

def crawl_saramin_jobs() -> list[dict]:
    print("[Crawler] 사람인 채용정보 수집 시작")

    companies = ["당근마켓", "비바리퍼블리카"]
    base_url = "https://www.saramin.co.kr/zf_user/search?searchword="

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # ← 개발 중엔 주석 처리
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(3)

    results = []

    for company in companies:
        try:
            driver.get(base_url + company)
            time.sleep(3)
            job_cards = driver.find_elements(By.CSS_SELECTOR, "div.item_recruit")

            print(f"[사람인] {company} 공고 수: {len(job_cards)}")

            for idx, job in enumerate(job_cards[:10]):
                try:
                    link_elem = job.find_element(By.CSS_SELECTOR, "h2.job_tit a")
                    job_title = link_elem.text.strip()
                    post_url = link_elem.get_attribute("href")

                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(post_url)
                    time.sleep(2)

                    try:
                        desc_elem = driver.find_element(By.CSS_SELECTOR, "div.user_content")
                        description = desc_elem.text.strip()
                    except:
                        description = "(본문 없음)"

                    results.append({
                        "source": "사람인",
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
                    print(f"[사람인] {company} 공고 {idx + 1} 실패: {inner_e}")
                    continue

        except Exception as e:
            print(f"[사람인] {company} 크롤링 실패: {e}")
            continue

    driver.quit()
    return results
