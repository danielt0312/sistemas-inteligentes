def h(y):
    global x
    x += 1
    print(str(x))

def func_a(a=1):
    print ('inside func_a' + str(a))
    return 'x'

def func_b(y):
    print ('inside func_b')
    return y

def func_c(z):
    print ('inside func_c')
    return z()

"""
x = 10
h(-100)
print('x: ' + str(x))
"""

def quotient_and_remainder(x, y):
    q = x // y
    r = x % y
    return (q, r)

tupla = (1, False, 'xd', 1.4, (1, 2))

l = [1, 2, False, (1, 2)]
l[3] = [1,2]
print(l)

L = [1,2,3,4]
print(L)
L.append((1,2,3))
L.extend([1,2,3])
L.remove(1)
L.pop()
del(L[0])

print(L)

"""
for element in tupla:
    print(element, type(element))
"""

#print (func_a(10))
#print (5 + func_b(2))
#print (func_c(func_a))