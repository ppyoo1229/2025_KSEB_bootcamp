from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

menu_list = [
    "백반", "초밥", "순대국밥", "비빔밥", "돼지국밥", "일반김밥",
    "칼국수", "짜장면", "파스타/스파게티", "짬뽕", "물냉면", "우동",
    "갈비탕", "뼈해장국", "추어탕", "샤브샤브", "부대찌개", "김치찌개",
    "육개장", "감자탕", "곰탕", "돼지갈비", "삼겹살", "소갈비",
    "불고기/주물럭", "소곱창구이", "닭갈비", "장어구이", "생선구이", "스테이크",
    "등심구이", "목살", "떡볶이", "쭈꾸미볶음", "낙지볶음", "치킨",
    "돈가스", "탕수육", "아귀찜", "족발", "고기보쌈/수육", "모듬회",
    "피자", "소주", "병맥주(국산)", "생맥주(국산)", "병맥주(수입)",
    "아메리카노", "탄산음료", "카페라떼"
]

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

results = []

try:
    for menu in menu_list:
        driver.get("https://www.atfis.or.kr/fip/front/M000000287/stats/pos.do")
        time.sleep(2)

        # 종류 선택
        try:
            Select(WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "minorMenu"))
            )).select_by_visible_text(menu)
        except:
            print(f"[실패] '{menu}' 메뉴 선택 불가")
            continue

        time.sleep(2)

        # 인천광역시 가격 추출
        try:
            area_items = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".areaList li"))
            )
            for li in area_items:
                if "인천광역시" in li.text:
                    price = li.text.split()[1].replace(",", "").replace("원", "")
                    results.append({
                        "소분류 메뉴": menu,
                        "인천 평균가": int(price)
                    })
                    print(f"[완료] {menu}: {price}원")
                    break
        except:
            print(f"[없음] '{menu}' 데이터 없음")
            
finally:
    driver.quit()

# CSV 저장
df = pd.DataFrame(results)
df.to_csv("1AVG_incheon.csv", index=False, encoding="utf-8-sig")
print("저장 완료: 1AVG_incheon.csv")