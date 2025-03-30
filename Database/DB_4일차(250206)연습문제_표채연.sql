create database madang;
use madang;

drop table 극장;
drop table 상영관;
drop table 예약;
drop table 고객;

select * from 극장;
select * from 상영관;
select * from 예약;
select * from 고객;

CREATE TABLE 극장( 극장번호 integer primary key,
				  극장이름 varchar(30),
				  위치 varchar(30));

CREATE TABLE 상영관 ( 극장번호 integer,
					상영관번호 integer primary key,
					영화제목 varchar(30),
					가격 integer,
					좌석수 integer);
                    
CREATE TABLE 예약( 극장번호 integer,
				  상영관번호 integer,
				  고객번호 integer,
				  가격번호 integer primary key,
				  날짜 date);
                    
CREATE TABLE 고객( 고객번호 integer primary key,
			      이름 varchar(30),
				  주소 varchar(30));

INSERT INTO 극장 VALUES (1, '롯데', '잠실');
INSERT INTO 극장 VALUES (2, '메가', '강남');
INSERT INTO 극장 VALUES (3, '대한', '잠실');
INSERT INTO 상영관 VALUES (1, 1, '어려운 영화', 15000, 48);
INSERT INTO 상영관 VALUES (3, 1, '멋진 영화', 7500, 120);
INSERT INTO 상영관 VALUES (3, 2, '재밌는 영화', 8000, 110);
INSERT INTO 예약 VALUES (3, 2, 3, 15, '2020-09-01');
INSERT INTO 예약 VALUES (3, 1, 4, 16, '2020-09-01');
INSERT INTO 예약 VALUES (1, 1, 9, 48, '2020-09-01');
INSERT INTO 예약 VALUES (1, 1, 9, 49, '2020-09-01'); 
INSERT INTO 고객 VALUES (3, '홍길동', '강남');
INSERT INTO 고객 VALUES (4, '김철수', '잠실');
INSERT INTO 고객 VALUES (9, '박영희', '강남');

-- 1.모든 극장의 이름과 위치를 보이시오.
select 극장이름, 위치 from 극장;
 
-- 2. '잠실'에 있는 극장을 보이시오.
select * from 극장 where 위치 = '잠실';

-- 3. '잠실'에 사는 고객의 이름을 오름차순으로 보이시오.
select 이름 from 고객 where 주소 = '잠실' order by 이름 asc;

-- 4. 가격이 6,000원 이하인 영화의 극장번호, 상영관번호, 영화제목을 보이시오.
select 극장번호, 상영관번호, 영화제목 from 상영관 where 가격 <= 6000;

-- 5. 극장 위치와 고객의 주소가 같은 고객들을 보이시오.

-- 1. 극장의 수는 몇 개인가?
select count(*) '극장 수' from 상영관;

-- 2. 상영되는 영화의 평균 가격은 얼마인가?
select round(avg(가격)) from 상영관;

-- 3. 2014년 9월 1일에 영화를 관람한 고객의 수는 얼마인가?
