
l7= []
N = 120000
for i in range(1,N):
    l7.append(i)
print(len(l7))
l2 = list(filter(lambda x: x%2 == 0 , l7))
ptc2 = (100 * (len(l2)/N))
print(str(len(l2)) +" ;" +  str(100 * (len(l2)/N)))
l3 = list(filter(lambda x: x%3 == 0 , l7))
ptc3 = (100 * (len(l3)/N))
print(str(len(l3)) +" ;" +  str(100 * (len(l3)/N)))
l5 = list(filter(lambda x: x%5 == 0 , l7))
ptc5 = (100 * (len(l5)/N))
print(str(len(l5)) +" ;" +  str(100 * (len(l5)/N)))
ll7 = list(filter(lambda x: x%7 == 0 , l7))
ptc7 = (100 * (len(ll7)/N))
print(str(len(ll7)) +" ;" +  str(100 * (len(ll7)/N)))
l11 = list(filter(lambda x: x%11 == 0 , l7))
ptc11 = (100 * (len(l11)/N))
print(str(len(l11)) +" ;" +  str(100 * (len(l11)/N)))

l235 = list(filter(lambda x: x%2 == 0 or x%3 == 0 or x%5 == 0 , l7))
ptc235 = (100 * (len(l235)/N))
print("len235 ="+str(len(l235)) +" ;" +  str(100 * (len(l235)/N)))

print((100/N )*((N/2)) )
print((100/N )*((N/3)) )
print((100/N )*((N/5)) )
print((100/N )*((N/7)) )
print((100/N )*((N/11)) )



