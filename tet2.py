a = [0,1,2,3,4]
b = [0,1]
c = [4]
d = [1,0]

print list(set(a)-set(b)-set(c))

print (set(b) == set(d))

dd = {3:[set([2,5,3]),set([1,3,4])],
      2:[[1,2]],
      1:[[2],[1]]}

print (set([3,2,4]) in dd[3])


