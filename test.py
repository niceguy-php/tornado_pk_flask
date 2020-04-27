from sympy import *

l = [(10,2),(7,5),(6,6)]


#定义变量
x = Symbol('x')
y = Symbol('y')
print(solve([l[0][0]+l[1][0]+l[2][0]+x-y-(l[0][1]+l[1][1]+l[2][1]),],[x,y]))