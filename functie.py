from Eindopdracht import *

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

print(f)

             
expr = Expression.fromString('10*0.5-3+20')
expr2 = Expression.fromString('4*5+2')
#print(expr.evaluate({'x':5}))

#print(c.evaluate())
print(expr.evaluate())
print(expr2.evaluate())

g = expr.evaluate() == expr2.evaluate()

print(g)

#expr2= Expression.fromString('1*x-5/10+8-5*30//10')
#print(expr2)
#print(expr2.evaluate({'x':3}))