import copy

matches = [[1,2],[1,3],
              [5,6],[5,2],
              [3,4],[3,1],
              [4,6],[4,3],
              [2,1],[2,5],
              [6,5],[6,4]]

#===============================================================================
# 
# matches = [['a', 'f'], ['a', 'b'], 
#            ['b', 'a'], ['b', 'd'], 
#            ['c', 'd'], ['c', 'e'], 
#            ['d', 'c'], ['d', 'b'], 
#            ['e', 'c'], ['e', 'f'], 
#            ['f', 'a'], ['f', 'e']]
#===============================================================================
#===============================================================================
#matches = [['a', 'd'], ['a', 'e'], ['a', 'i'], ['a', 'f'], ['a', 'h'], ['a', 'g'], ['b', 'i'], ['b', 'c'], ['b', 'j'], ['b', 'e'], ['b', 'h'], ['b', 'f'], ['c', 'b'], ['c', 'g'], ['c', 'f'], ['c', 'e'], ['c', 'j'], ['c', 'd'], ['d', 'a'], ['d', 'i'], ['d', 'h'], ['d', 'j'], ['d', 'c'], ['d', 'e'], ['e', 'a'], ['e', 'c'], ['e', 'b'], ['e', 'd'], ['e', 'f'], ['e', 'h'], ['f', 'g'], ['f', 'c'], ['f', 'a'], ['f', 'i'], ['f', 'e'], ['f', 'b'], ['g', 'f'], ['g', 'c'], ['g', 'h'], ['g', 'j'], ['g', 'a'], ['g', 'i'], ['h', 'd'], ['h', 'j'], ['h', 'g'], ['h', 'a'], ['h', 'e'], ['h', 'b'], ['i', 'b'], ['i', 'd'], ['i', 'j'], ['i', 'a'], ['i', 'f'], ['i', 'g'], ['j', 'i'], ['j', 'h'], ['j', 'b'], ['j', 'd'], ['j', 'g'], ['j', 'c']]

#matches = [['a', 'j'], ['a', 'c'], ['a', 'h'], ['a', 'i'], ['a', 'g'], ['a', 'b'], ['b', 'c'], ['b', 'd'], ['b', 'a'], ['b', 'h'], ['b', 'e'], ['b', 'f'], ['c', 'b'], ['c', 'a'], ['c', 'f'], ['c', 'g'], ['c', 'j'], ['c', 'h'], ['d', 'b'], ['d', 'j'], ['d', 'e'], ['d', 'f'], ['d', 'g'], ['d', 'i'], ['e', 'h'], ['e', 'd'], ['e', 'b'], ['e', 'f'], ['e', 'g'], ['e', 'i'], ['f', 'c'], ['f', 'd'], ['f', 'i'], ['f', 'e'], ['f', 'g'], ['f', 'b'], ['g', 'c'], ['g', 'a'], ['g', 'j'], ['g', 'd'], ['g', 'f'], ['g', 'e'], ['h', 'e'], ['h', 'a'], ['h', 'c'], ['h', 'b'], ['h', 'j'], ['h', 'i'], ['i', 'a'], ['i', 'f'], ['i', 'h'], ['i', 'j'], ['i', 'd'], ['i', 'e'], ['j', 'a'], ['j', 'c'], ['j', 'd'], ['j', 'g'], ['j', 'h'], ['j', 'i']]

################# THE TOTAL VARIETY OF OPTIONS NEEDS TO BE EQUAL TO THE NUMBER OF ELEMENTS LEFT


stand = [[1],[5],[3],[4],[2],[6]]
#stand = [['a'],['b'],['c'],['d'],['e'],['f']]
#stand = [['a'],['b'],['c'],['d'],['e'],['f'],['g'],['h'],['i'],['j']]

pod = {}
npod = {}
for row in matches:
    if row[0] in npod:
        npod[row[0]].append(row[1])
    else:
        npod[row[0]]=[row[1]]

# Construct a dict with players and all of their potential opponents
for player in stand:
    if not player[0] in pod:
        pod[player[0]]=[];
    for potential in stand:
           if potential[0]==player[0]:
               continue
           if not potential[0] in npod[player[0]]:
               pod[player[0]].append(potential[0])

print " Current standings {}".format(stand)
print "List of all potential opponents for each player {}".format(pod)     
print "List of all current played opponents for each player   {}".format(npod)


lop = []

def mk_pair(player, i):
    found_pair=False
    pos_to_move = 0
    while not found_pair:
        
        found_pair = True
        tpod = copy.deepcopy(pod)
        nplayer = stand[i+1+pos_to_move][0]
        print "checking player {} against {}".format(player,nplayer)
        print "beggining tpod = {} ".format(tpod)
        print "beggining pod = {}".format(pod)
        if nplayer in npod[player]:
            print "player {} has already played {}".format(player, nplayer)
            found_pair=False
            pos_to_move += 1
            continue
        
        tpod.pop(player,None)
        tpod.pop(nplayer,None)
        
        
        print "temp pl opt dict {}".format(tpod)
        for key in tpod:
            if player in tpod[key]:
                tpod[key].remove(player)
            if nplayer in tpod[key]:
                tpod[key].remove(nplayer)
        
        print "temp pl opt dict -after rem {}".format(tpod)
        #=======================================================================
        # for key in tpod:
        #     if len(tpod[key])<1:
        #         print "player {} with list: {}".format(key,tpod[key])
        #         pos_to_move += 1
        #         found_pair = False
        #         break
        # if not found_pair:
        #     print "going to next player"
        #     continue
        #=======================================================================
        
        ##### COUNT THE TOTAL VARIETY OF OPTIONS IF TOTAL VARIETY < NUMBER OF PLAYERS LEFT WE'RE SCREWED
        
        ##### THERE CANNOT BE ....
        #=======================================================================
        # variety_list = []
        # variety_count = 0
        # for key in tpod:
        #     variety_count +=1
        #     for pl in tpod[key]:
        #         if pl not in variety_list:
        #             variety_list.append(pl)
        # print "variety list = {} and variety count = {}".format(variety_list,variety_count)      
        # 
        # if len(variety_list) != variety_count:
        #     found_pair = False
        #     pos_to_move += 1;
        #     print "not a good variety vs options left"
        #     continue
        # 
        #=======================================================================
        #### DOESNT WORK.. THERE CANNOT BE TWO SINGLE OPTION PLAYERS THAT REFER TO THE SAME PLAYER
        no_good = False
        #=======================================================================
        # one_option_list = []
        # for key in tpod:
        #     if len(tpod[key])==1:
        #        if tpod[key][0] in one_option_list:
        #            no_good = True
        #            break
        #        else:
        #            one_option_list.append(tpod[key][0])
        # if no_good:
        #     found_pair = False
        #     pos_to_move += 1
        #     print "a single player is the only option for multiple people"
        #     continue
        #=======================================================================
        
        option_dict = {}
        for key in tpod:
            # number of options
            n_options = len(tpod[key])
            
            # Check to see if there are any players left with no options
            if not tpod[key]:
                no_good = True
                break
            
            try:
               option_dict[n_options]
               #now try to see if the option set is in the dict
               if (set(tpod[key]) in option_dict[n_options]):
                   #check to see if there already are n other elements with only the same n choices:
                   if len(option_dict[n_options]) >= n_options:
                       #not a good pair.. blow up;
                       no_good = True
                       break
                   else:
                       option_dict[n_options].append(set(tpod[key]))
            except KeyError:
                option_dict[n_options] = [set(tpod[key])]
        
        print "Option Dict = {}".format(option_dict)         
        if no_good:
            found_pair = False
            pos_to_move += 1
            print "a single player is the only option for multiple people"
            continue
        
        
        pod.pop(player,None)
        pod.pop(nplayer,None)
        for key in pod:
            if player in pod[key]:
                pod[key].remove(player)
            if nplayer in pod[key]:
                pod[key].remove(nplayer)
        
        
            
        if found_pair:
            # Add pair to list
            lop.append((player,nplayer))
            # Move people in standings
            print "Found Pair {0} {1}".format(player,nplayer)
            oldindex = i + 1 + pos_to_move
            stand.insert(i + 1, stand.pop(oldindex))
    return True


i = 0
while i < (len(stand)):
    player = stand[i][0];
    print "Player {}".format(player)
    print "Stand {}".format(stand)
    print "teams {}".format(lop)
    found_pair=False
    pos_to_move = 0
    print "new                    \n \n"
    ############ remember to check if somehow we reach the end before we can find the proper pairs
    if mk_pair(player, i):
        i+=2
        
    
    
print lop
    #===========================================================================
    # while not found_pair:
    #     #try to see if he played the next player
    #     try:
    #         nplayer = stand[i + 1 + pos_to_move][0]
    #     except IndexError:
    #         if not pos_to_move:
    #             # This means that we've reached the end of the list, number of players is odd
    #             i += 2;
    #             break;
    #         raise Exception("Some of the players played all the other ones, this is one round too many")
    #     if player in pod:
    #         if nplayer in pod[player]:
    #             pos_to_move += 1
    #             continue
    #         else:
    #             # Found a pair
    #             print "Found Pair {0} {1}".format(player,nplayer)
    #             oldindex = i + 1 + pos_to_move
    #             stand.insert(i + 1, stand.pop(oldindex))
    #             i += 2
    #             found_pair = True
    #             print stand
    #===========================================================================
    