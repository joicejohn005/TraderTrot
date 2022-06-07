def count(list1, l, r):
    return len(list(x for x in list1 if l <= x <= r)) 
# driver code
list1 = [0, 0, 10, 20, 30, 40, 50, 40, 40, 60, 70, 100, 120, 130, 500, 1000, 2000, 3002]
l = 0
r = 0
l2 = 1
r2 = 90
l3= 91
r3=732
l4=733
r4 = 40000
mode = []

x= count(list1, l, r)
y= count(list1, l2, r2)
z= count(list1, l3, r3)
w = count(list1, l4, r4)

mode.append(x)
mode.append(y)
mode.append(z)
mode.append(w)

x = max(mode)
if (x == mode[0]):
    print("day")
elif (x == mode[1]):
    print("sw")
elif (x == mode[0]):
    print("po")
elif (x == mode[0]):
    print("in")