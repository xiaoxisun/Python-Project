#!/usr/bin/python

print "Hello, python"
print "say hey, I am starting Python again, but learn basic practise basic a lot"

myint=7
myfloat=7.0
mystring= 'hello this\'s my string haha'

print myint
print myint+myint
print myfloat

print mystring+mystring
print myint+myfloat

mylist=[]
mylist.append(1)
mylist.append(2)

print mylist[0]

for x in mylist:
    print x
    print mystring


x_list=[1,2,3,4,5,6,7,8,9,10]
y_list=[2,3,4,5,6,7,3,2,2,'test']

for x in x_list:
    print x
for y in y_list:
    print y

big_list=(x_list+y_list)*10

for x in big_list:
    print x
    
