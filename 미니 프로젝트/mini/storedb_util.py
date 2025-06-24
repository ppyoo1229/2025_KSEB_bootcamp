import pymysql

# DB 연결 정보
DB_CONFIG = {
    'host': 'localhost',
    'user': 'user',
    'password': 'worldcup7!',
    'db': '현민',
    'charset': 'utf8mb4'
}

# 정상 데이터 upsert(중복 시 update)
def upsert_restaurant(store_name, avg_price, menu_count, naver_category):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO restaurants (store_name, avg_price, menu_count, naver_category)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                avg_price=VALUES(avg_price),
                menu_count=VALUES(menu_count),
                naver_category=VALUES(naver_category),
                updated_at=NOW()
            """
            cursor.execute(sql, (store_name, avg_price, menu_count, naver_category))
        conn.commit()
    finally:
        conn.close()

# 결측치 데이터 insert
def insert_missing(store_name, avg_price, menu_count, naver_category, note=None):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO restaurants (store_name, avg_price, menu_count, naver_category, note)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (store_name, avg_price, menu_count, naver_category, note))
        conn.commit()
    finally:
        conn.close()

# 이상치 데이터 insert
def insert_outlier(store_name, avg_price, menu_count, naver_category, note=None):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO restaurants_outlier (store_name, avg_price, menu_count, naver_category, note)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (store_name, avg_price, menu_count, naver_category, note))
        conn.commit()
    finally:
        conn.close()

# 가격/메뉴 없는 가게 자동 입력
def get_category_avg(category, default=15000):
    # category_avg에서 값 조회
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = "SELECT avg_price FROM category_avg WHERE naver_category=%s"
            cursor.execute(sql, (category,))
            row = cursor.fetchone()
            if row and row[0]:
                return row[0]
            else:
                return default  # 임의 기본값
    finally:
        conn.close()

# 업종별 평균가 db 수집용
def category_avg(category):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = """
            UPDATE category_avg 
            SET avg_price = (SELECT ROUND(AVG(avg_price)) FROM restaurants WHERE naver_category=%s AND avg_price > 0),
                menu_count = (SELECT COUNT(*) FROM restaurants WHERE naver_category=%s AND avg_price > 0),
                last_updated = NOW()
            WHERE naver_category=%s
            """
            cursor.execute(sql, (category, category, category))
        conn.commit()
    finally:
        conn.close()
