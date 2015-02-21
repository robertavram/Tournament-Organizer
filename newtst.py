import random
import string

def create_lop(n):
    result = {}
    lresult =[]
    for i in range(n):
        result[string.ascii_lowercase[i]]=[]
        lresult.append(string.ascii_lowercase[i])
    return result, lresult

dop, lop = create_lop(10)
print dop, lop
print "\n"
def create_matches(dop,lop,n):
    not_a_choice = []
    goon =True
    while goon:
        goon=False
        for i in range(len(lop)):
            if len(dop[lop[i]])>=n:
                continue
            for key in dop:
                if len(dop[key]) >= n:
                    not_a_choice.append(key)
            
            l_of_choices = list(set(lop[0:i]+lop[i+1:]) - set(dop[lop[i]]) - set(not_a_choice))
            if l_of_choices:
                opponent = random.choice(l_of_choices)
                dop[lop[i]].append(opponent)
                dop[opponent].append(lop[i])
        for key in dop:
            if len(dop[key]) < n:
                goon = True
    return dop, lop


newdop, newlop = create_matches(dop, lop, 6)

#print newdop;
#print newlop;

mylist = []
for el in lop:
    for op in dop[el]:
        mylist.append([el,op])
print mylist;