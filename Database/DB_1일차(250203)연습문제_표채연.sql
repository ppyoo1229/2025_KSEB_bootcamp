-- (1) 도서번호가 1인 도서의 이름
select bookname from book
where bookid = 1;

-- (2) 가격이 20,00원 이상인 도서의 이름
select bookname from book
where price >= 20000;

-- (4) 2014년 7월 4일~7월 7일 사이에 주문받은 도서의 주문번호
select bookid from orders
where orderdate between date_format("2014-07-04","%Y-%m-%d") and date_format("2014-07-07","%Y-%m-%d");

-- (5) 2014년 7월 4일~7월 7일 사이에 주문받은 도서를 제외한 도서의 주문번호
select bookid from orders
where orderdate not between date_format("2014-07-04","%Y-%m-%d") and date_format("2014-07-07","%Y-%m-%d");

-- (6) 성이 ‘김’ 씨인 고객의 이름과 주소
select name, address from customer
where name like '김%';

-- (7) 성이 ‘김’ 씨이고 이름이 ‘아’로 끝나는 고객의 이름과 주소
select name, address from customer
where name like '김%아';