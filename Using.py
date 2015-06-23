from Voorbeeldgitub import *
a = Constant(2.0)
b = Constant(3.0)
d=Constant(10)
c = ( ( a + b ) + d ) + (( a + d )+ b)
e= (( a*d)/(b))
f=( a+ (b**d))
print(type(c),type(a-b))
print(c)
expr = Expression.fromString('1+2+3/4')

print(expr)


print(c.evaluate())
print(e.evaluate())
print(f.evaluate())
print(c.minimum())

a = Constant(2)
b = Constant(3)

x = Variable('x')
c = a*x + b
print(c)
print(c.minimum())
expr = Expression.fromString('x+y**2')
expr2= Expression.fromString( '1*x-5/10')
print(expr)
print(expr2)
print(type(expr), 'type expr')


expr2= Expression.fromString( '1*x-5/10')
print(expr2, 'expr2')
print(c.evaluate({'x':2}))

print(expr.evaluate({'x':2, 'y':3}))