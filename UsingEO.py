from Eindopdracht import *
a = Constant(2.0)
b = Constant(3.0)
d = Constant(10)
c = ( ( a + b ) + d ) + (( a + d )+ b)
e = (( a * d) / b)
g = (( d * a) / b)
f = (( a + d) * (b ** d))
print(c)
w = Expression.fromString('1*5/9+10')
z = a * b / (d + a)
print(w,z, f)
expr = Expression.fromString('1+2+3/4')
expt = Expression.fromString('1+2**3+3+4**2')
print(expr)

print(expt)
expr.expteq(expt)
print(c.evaluate())
print(e.evaluate())
print(f.evaluate())
a = Constant(2)
b = Constant(3)
x = Variable('x')
c = a + x + b
print(c)
expr = Expression.fromString('x+y**2')
expr2 = Expression.fromString( 'x**2-4')
print(expr)
print(expr2)
print(expr2.findRoot('x',-100, 100, 0.05))
print(expr2.findAllRoots('x',-10,10,0.0001))
print(c.evaluate({'x':2}))
print(expr.evaluate({'x':2, 'y':3}))
w=e+g
print(w)
