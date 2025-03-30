-- (3) 박지성의 총 구매액
select sum(saleprice) from orders
where custid = (select custid from customer where name = "박지성");

-- (4) 박지성이 구매한 도서의 수
select count(*) from orders where custid = 1;

-- (5) 박지성이 구매한 도서의 출판사 수
select count(distinct publisher) as "출판사 수" from book
where bookid in (select bookid from orders where custid = (select custid from customer where name = "박지성"));

-- (1) 마당서점 도서의 총 개수
select count(*) from book;

-- (2) 마당서점에 도서를 출고하는 출판사의 총 개수
select count(distinct publisher) from book;

-- (3) 모든 고객의 이름, 주소
select name, address from customer;

-- (9) 주문 금액의 총액과 주문의 평균 금액
select sum(orders.saleprice) as "총액", round(avg(orders.saleprice)) as "평균 금액"
from orders;

-- (10) 고객의 이름과 고객별 구매액
-- select customer.name, sum(

-- (11) 고객의 이름과 고객이 구매한 도서 목록
select customer.name, book.bookname
from orders left join customer on orders.custid = customer.custid
			left join book 	   on orders.bookid = book.bookid;