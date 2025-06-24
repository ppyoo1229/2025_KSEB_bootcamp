-- 정상 데이터 테이블
CREATE TABLE restaurants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL UNIQUE,
    avg_price INT,
    menu_count INT,
    naver_category VARCHAR(50),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 결측치(미수집/오류) 데이터 테이블
CREATE TABLE restaurants_missing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    avg_price INT,
    menu_count INT,
    naver_category VARCHAR(50),
    note VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 이상치 데이터 테이블
CREATE TABLE restaurants_outlier (
    id INT AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    avg_price INT,
    menu_count INT,
    naver_category VARCHAR(50),
    note VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 업종별 평균가 관리 테이블 (자동 갱신)
CREATE TABLE category_avg (
    id INT AUTO_INCREMENT PRIMARY KEY,
    naver_category VARCHAR(50) NOT NULL UNIQUE,
    avg_price INT,
    menu_count INT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
