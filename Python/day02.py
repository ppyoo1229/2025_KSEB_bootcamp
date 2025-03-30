# Assignment Day 02
# v1.4) Make my_pow custom function instead of ** operator, power function and make it work.
import math


def my_pow(b, e) -> float:
    """
    A user-defined function that receives a base and exponent and returns the power result in the form of a real number
    :param b: base number
    :param e: exponent
    :return: the power result in the form of a real number
    """
    if e < 0:
        b = 1 / b
        e = e * -1

    result = 1

    i = int(e)
    f = e - i

    for _ in range(i):  # for k in range(e):
        result = result * b

    if f > 0:
        result = result * math.exp(f * math.log(b))

    return result


def is_prime(num) -> bool:
    """
    A function that returns True if it is a prime number and False if it is not a prime number
    :param num: integer number
    :return: boolean type
    """
    if num >= 2:
        i = 2
        #while i < (int(my_pow(num, 0.5)) + 1):
        while i*i < num+1:
            if num % i == 0:
                return False
            i = i + 1
    else:
        return False
    return True


#print(my_pow(2, 9))
numbers = input("Input number : ").split()  # ex) 900 1000
n1 = int(numbers[0])
n2 = int(numbers[1])

if n1 > n2:
    n1, n2 = n2, n1

j = n1
while j <= n2:
    if is_prime(j):
        print(j, end=' ')
    j = j + 1
