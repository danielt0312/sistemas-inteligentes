
a_list = []
L = [2, 'a', 4, (1,2)]
T = (2, 'a', 4, [1,2])

print (L)
L[1] = False
print (L)
L[3] = [1,4,6]
print (T)
exit()

def quotient_and_remainder(x, y):
	q = x // y
	r = x % y
	return (q, r)

b = quotient_and_remainder(4,5)

a = (1, "K", True, 1.5, b)
for element in a:
	print (element)
	print (type(element))

exit()

print (type(a))
print (a[0], a[1])
print (type(a[0]),type(a[1]))
print (len(a))


def h (y):
	global x
	x += 1
	print (str(x))

x = 10
h(-50)

def func_a(a=1):
	print ('inside func_a'+str(a))
def func_b(y):
	print ('inside func_b')
	return y
def func_c(z):
	print ('inside func_c')
	return z()
#

print (func_a(10))
print (5 + func_b(2))
print (func_c(func_a))
