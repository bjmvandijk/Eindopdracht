from V3gitub import *
a = Constant(2.0)
b = Constant(3.0)
d=Constant(10)
c = ( ( a + b ) + d ) + (( a + d )+ b)
e = (( a*d)/(b))
g = (( d*a)/(b))
f = ( a+ (b**d))
#print(type(c),type(a-b))
print(c)
w=Expression.fromString('1*5/9+10')
z= a*b/(d+a)
print(w,z)
#print(c==e)
#print(type(e),type(g))
#print(e==g, g==e)
e.opeq(g)
c.opeq(f)
expr = Expression.fromString('1+2+3/4')
expt = Expression.fromString('1+2**3+3+4**2')
print(expr)
print(expt)
#print(c.minimal())

print(c.evaluate())
print(e.evaluate())
print(f.evaluate())
#print(c.minimum())

a = Constant(2)
b = Constant(3)

x = Variable('x')
c = a+x + b

print(c)
#print(c.minimum())
expr = Expression.fromString('x+y**2')
expr2= Expression.fromString( 'x**2-10')
print(expr)
print(expr2)
expr.opeq(expr2, {'x':4, 'y':5}) #,{'x':10}
print(type(expr), 'type expr')

print(expr2.findRoot('x',0.05,-100, 100))
print(expr2.findAllRoots('x',0.05,-100,100))
print(expr2, 'expr2')
print(c.evaluate({'x':2}))

print(expr.evaluate({'x':2, 'y':3}))
w=e+g
print(w)