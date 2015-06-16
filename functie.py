from voorbeeldgithub_bertjan import *

a = Constant(2)
b = Constant(3)
c = a // b
print(c)
             
expr = Expression.fromString('1+2-3*4//5')
print(expr)
