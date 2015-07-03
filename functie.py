from bertjan import *
import time

a = Constant(2)
b = Constant(3)
c = Constant(-2)
d = a + b
e = c - b

print(d)
print(d.evaluate())
print(e)
print(abs(e.evaluate()))

f = abs(e.evaluate()) == d.evaluate()
fu = d == e

print(f)
print(fu)

expr = Expression.fromString('x**2-4')             
expr2 = Expression.fromString('4-1**2-10/4*5+2') 	

print(expr.evaluate({'x':5}))
print(expr2)


g = expr.evaluate({'x':2,'y':10}) == expr2.evaluate()
h = expr == expr2

i = expr.expteq(expr)
j = expr.expteq(expr2)

print(g)
print(h)

print(i)
print(j)

T1 = time.perf_counter()

hoep = expr.findAllRoots('x', -100, 100, 0.001)
print(hoep)

T2 = time.perf_counter()
print(T2 - T1, 'seconds')
