"This code can be used to test Firstversion.py"

from Firstversion import *

a = Constant(2.0)
b = Constant(3.0)
d=Constant(10)
c = ( ( a + b ) + d ) + (( a + d )+ b)
e = (( a * d) / b)
g = (( d * a) / (b))
f = ( a + (b ** d))
print(c)
w=Expression.fromString('1*5/9+10')
z= a * b / (d + a )
print(w,z)
expr = Expression.fromString('1+2+3/4')
expt = Expression.fromString('1+2**3+3+4**2')
print(expr)
print(expt)
print(c.minimum())
print(c.evaluate())
print(e.evaluate())
print(f.evaluate())
print(c.minimum())
a = Constant(2)
b = Constant(3)
x = Variable('x')
c = a + x + b
print(c)
print(c.minimum())
expr = Expression.fromString('x+y**2')
expr2 = Expression.fromString( 'x**2-10')
print(expr)
print(expr2)