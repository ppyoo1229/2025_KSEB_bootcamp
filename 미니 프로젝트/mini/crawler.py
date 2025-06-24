import pandas as pd
import time
import numpy as np
from collections import Counter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from storedb_util import (
    upsert_restaurant,
    insert_missing,
    insert_outlier,
    get_category_avg,
    category_avg
)

# 메뉴 크롤링 함수
def crawling_get_menus(store_name, driver):
    menu_data = {
        "place_name": store_name,
        "menu": [],
        "naver_category": None
    }
    driver.get("https://map.naver.com/v5/search/" + store_name)
    time.sleep(2.5)

    # 1. entryIframe 자동 판별 / 이거 네이버 지도 구조 보고 바뀌는거 확인해야함...
    try:
        WebDriverWait(driver, 2).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "searchIframe"))
        )
        try:
            container = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul'))
            )
        except TimeoutException:
            driver.switch_to.default_content()
        else:
            buttons = container.find_elements(By.TAG_NAME, 'a')
            if buttons:
                try:
                    first_btn_class = buttons[0].get_attribute("class")
                    if "place_thumb" in first_btn_class and len(buttons) > 1:
                        buttons[1].send_keys(Keys.ENTER)
                    else:
                        buttons[0].send_keys(Keys.ENTER)
                    time.sleep(1.5)
                except StaleElementReferenceException:
                    pass
            driver.switch_to.default_content()
    except TimeoutException:
        driver.switch_to.default_content()

    # 2. entryIframe 진입
    try:
        entry_iframe = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.ID, "entryIframe"))
        )
        driver.switch_to.frame(entry_iframe)
    except TimeoutException:
        print(f"{store_name}: entryIframe 로딩 실패")
        return menu_data

    # 3. 네이버 업종명
    try:
        naver_category = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.lnJFt"))
        ).text
        menu_data["naver_category"] = naver_category
    except:
        pass

    # 4. '메뉴 더보기' 버튼 클릭
    try:
        menu_more_btn = driver.find_element(By.CSS_SELECTOR, "button[aria-label='메뉴 더보기']")
        menu_more_btn.click()
        time.sleep(1.5)  # 클릭 후 로딩 대기
    except Exception:
        pass  # 더보기 버튼이 없으면 무시

    # 5. 스크롤 맨 아래로 (전체 메뉴 로딩)
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    except Exception:
        pass

    # 6. 메뉴 크롤링 (포토 메뉴)
    try:
        photo_menu_list = driver.find_elements(By.CSS_SELECTOR, "ul.t1osG")
        if photo_menu_list:
            li_elements = photo_menu_list[0].find_elements(By.CSS_SELECTOR, "li.ipNNM")
            for li in li_elements:
                menu_name = li.find_element(By.CSS_SELECTOR, "span.VQvNX").text
                menu_price = li.find_element(By.CSS_SELECTOR, "div.gl2cc").text
                menu_data["menu"].append((menu_name, menu_price))
    except Exception as e:
        print(f"{store_name}: 포토 메뉴 크롤링 오류 - {e}")

    # 7. 메뉴 크롤링 (사진 없는 메뉴)
    try:
        text_menu_list = driver.find_elements(By.CSS_SELECTOR, "ul.jnwQZ")
        if text_menu_list:
            li_elements = text_menu_list[0].find_elements(By.CSS_SELECTOR, "li.gHmZ_")
            for li in li_elements:
                menu_name = li.find_element(By.CSS_SELECTOR, "div.ds3HZ a").text
                menu_price = li.find_element(By.CSS_SELECTOR, "div.mkBm3").text
                menu_data["menu"].append((menu_name, menu_price))
    except Exception as e:
        print(f"{store_name}: 텍스트 메뉴 크롤링 오류 - {e}")
    return menu_data

if __name__ == "__main__":
    input_csv = r"C:\inha_restaurant_FE.csv"
    output_csv = r"C:\inha_result_final.csv"
    chrome_driver_path = r"C:\chromedriver.exe"

    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    df = pd.read_csv(input_csv, encoding="utf-8-sig")
    store_names = df["상호명"].tolist()
    results = []

    # 필터 기준
    exclude_keywords = [
        "마스코트", "사장님", "기분", "없음", "전설", "VIP", "샘플", "test", "TEST",
        "한정", "도전", "무료", "서비스", "Special", "스페셜", "sample"
    ]
    MIN_PRICE = 1000
    MAX_PRICE = 100000

    for name in store_names:
        print(f"크롤링 중: {name}")
        try:
            data = crawling_get_menus(name, driver)
            prices = []
            for menu_name, price in data["menu"]:
                if any(word in menu_name for word in exclude_keywords):
                    continue
                try:
                    num = int(price.replace(",", "").replace("원", "").strip())
                    if MIN_PRICE <= num <= MAX_PRICE:
                        prices.append(num)
                except:
                    continue

            naver_category = data.get("naver_category")
            avg_price = None

            # 메뉴 가격 추출 실패(결측): 업종별 평균가로 대체값
            if not prices:
                avg_price = get_category_avg_price(naver_category, default=15000)
            else:
                # 메뉴 4개 이상: IQR 이상치 제거 후 중앙값 or 최빈값(편차 작으면)
                if len(prices) >= 4:
                    std = np.std(prices)
                    most_common = Counter(prices).most_common(1)[0][0]
                    if std < 1000:
                        avg_price = most_common
                    else:
                        q1 = np.percentile(prices, 25)
                        q3 = np.percentile(prices, 75)
                        iqr = q3 - q1
                        lower = q1 - 1.5 * iqr
                        upper = q3 + 1.5 * iqr
                        filtered_prices = [p for p in prices if lower <= p <= upper]
                        if filtered_prices:
                            avg_price = int(np.median(filtered_prices))
                        else:
                            avg_price = int(np.median(prices))
                else:
                    # 메뉴 4개 미만: 단순 평균
                    avg_price = sum(prices) // len(prices)

            # 결과 저장(프로젝트용 로컬 csv / 서비스용 DB upsert)
            results.append({
                "상호명": name,
                "1인 평균 가격": avg_price,
                "메뉴 수": len(prices),
                "네이버 업종명": naver_category
            })

            # DB
            upsert_restaurant(name, avg_price, len(prices), naver_category)
        if avg_price is None or menu_count == 0 or naver_category is None:
            insert_missing(name, avg_price, menu_count, naver_category, note="결측치 발생")
        else:
            upsert_restaurant(name, avg_price, menu_count, naver_category)
            # 업종 평균 자동 갱신
        category_avg(naver_category)

        except Exception as e:
        insert_missing(name, None, 0, None, note=f"오류: {e}")
    # 프로젝트 분석용 백업 csv
    # pd.DataFrame(results).to_csv(output_csv, index=False, encoding="utf-8-sig")
    # print(f"결과 저장: {output_csv}")

    driver.quit()
    pd.DataFrame(results).to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"결과 저장 완료: {output_csv}")