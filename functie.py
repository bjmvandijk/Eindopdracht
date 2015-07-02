from Eindopdracht import *
import time

a = Constant(2)
b = Constant(3)
c = Constant(-2)
d = a + b
e = c - b

#print(d)
#print(d.evaluate())
#print(e)
#print(abs(e.evaluate()))

f = abs(e.evaluate()) == d.evaluate()

#print(f)

#expr = Expression.fromString('(x-2)**2-4')             
expr = Expression.fromString('10*0.5/x-3+20**y')
expr2 = Expression.fromString('4-1**2-10/4*5+2') 	# 4 - 1^2 - 10/(4*5) + 2

expr3 = Expression.fromString('1+3*x')
expr4 = Expression.fromString('2+2')
#print(expr.evaluate({'x':5}))
print(expr2)

#print(c.evaluate())
#print(expr.evaluate())
print(expr2.evaluate())

g = expr.evaluate({'x':2,'y':10}) == expr3.evaluate({'x':2})
h = expr == expr3
#i = expr3 == expr3

print(g)

print(h)
#print(i)
#T1 = time.perf_counter()

#hoep = expr.findAllRoots('x', -10, 10, 0.01)               #lambda x: math.sin(x),1,5,.0001)
#print(hoep)

#T2 = time.perf_counter()
#print(T2 - T1, 'seconds')
#expr2= Expression.fromString('1*x-5/10+8-5*30//10')
#print(expr2)
#print(expr2.evaluate({'x':3}))
