-- (7) 박지성이 구매하지 않은 도서
select * from book

-- (8) 주문하지 않은 고객의 이름(부속질의 사용)
-- (12) 도서의 가격(Book 테이블)과 판매가격(Orders 테이블)의 차이가 가장 많은 주문
-- (13) 도서의 판매액 평균보다 자신의 구매액 평균이 더 높은 고객의 이름
-- (1) 박지성이 구매한 도서의 출판사와 같은 출판사에서 도서를 구매한 고객의 이름
-- (2) 두 개 이상의 서로 다른 출판사에서 도서를 구매한 고객의 이름

-- (3) 전체 고객의 30% 이상이 구매한 도서
select bookname from book b1
 where (select count(book.bookid) from book join orders
		on book.bookid = orders.bookid
		where book.bookid = b1.bookid) >= 0.3 * (select count(*) from customer);
        
-- (1) 새로운 도서 (‘스포츠 세계’, ‘대한미디어’, 10000원)이 마당서점에 입고되었다. 삽입이 안될 경우 필요한 데이터가 더 있는지 찾아보자.

-- (2) ‘삼성당’에서 출판한 도서를 삭제해야 한다.
delete from book
where publisher = "삼성당";

-- (3) ‘이상미디어’에서 출판한 도서를 삭제해야 한다. 삭제가 안 될 경우 원인을 생각해보자.
delete from book
where publisher = "이상미디어";

-- (4) 출판사 ‘대한미디어’가 ‘대한출판사’로 이름을 바꾸었다
update book
set publisher = '대한출판사'
where publisher = '대한미디어';