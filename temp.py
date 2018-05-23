#! /usr/bin/env python
# _*_ coding:utf-8 _*_






with open("./temp.list", "r") as doc:
    data = doc.read().split("\n")

#print data
data = filter(lambda x: x, data)
data = map(float, data)
data.sort()


avg = sum(data) / len(data)

max_ = data[int(len(data) * 0.99)]

min_ = min(data)

frag = map(lambda x: x-avg, data)

big = filter(lambda x: x>0, frag)
print big
small = filter(lambda x: x<=0, frag)
print small
quota_sum = 100 * len(data)

print avg, max_, min_
print 
print sum(big)/quota_sum, sum(small)/ quota_sum

