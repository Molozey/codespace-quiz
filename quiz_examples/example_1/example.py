# https://stackoverflow.com/questions/15541404/python-string-interning
import random
import string
import sys

L = 2
N = 1

print("1 .   " + "=====" * 30)
###

first_str = "AA"
sec_str = "AA"
print(id(first_str), id(sec_str), first_str is sec_str, first_str == sec_str)
print(first_str, sec_str)
print("2 .   " + "=====" * 30)

###

first_str = "A" * L
sec_str = "A" * L
print(id(first_str), id(sec_str), first_str is sec_str, first_str == sec_str)
print(first_str, sec_str)
print("3 .   " + "=====" * 30)

###


###

first_str = sys.intern("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" * 300)
sec_str = sys.intern("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" * 300)
print(id(first_str), id(sec_str), first_str is sec_str, first_str == sec_str)
print(first_str[:10], sec_str[:10])
print("4 .   " + "=====" * 30)


###
random.seed(0)
first_str = "".join(random.choices(string.ascii_letters + string.digits, k=L))
random.seed(0)
sec_str = "".join(random.choices(string.ascii_letters + string.digits, k=L))
print(id(first_str), id(sec_str), first_str is sec_str, first_str == sec_str)
print(first_str, sec_str)
print("5.   " + "=====" * 30)

###
first_str = None
sec_str = None or 0
print(id(first_str), id(sec_str), first_str is sec_str, first_str == sec_str)
print(first_str, sec_str)
print("=====" * 30)
