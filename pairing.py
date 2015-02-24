import copy

def mk_pair(player, i, pod, npod,stand):
    found_pair = False
    pos_to_move = 0
    while not found_pair:
        found_pair = True
        tpod = copy.deepcopy(pod)
        nplayer = stand[i + 1 + pos_to_move]
        
        if nplayer in npod[player]:
            #print "player {} has already played {}".format(player, nplayer)
            found_pair = False
            pos_to_move += 1
            continue
        
        tpod.pop(player, None)
        tpod.pop(nplayer, None)
        
        for key in tpod:
            if player in tpod[key]:
                tpod[key].remove(player)
            if nplayer in tpod[key]:
                tpod[key].remove(nplayer)
        
        no_good = False
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
            
        if no_good:
            found_pair = False
            pos_to_move += 1
            print "Pair cannot be set, would create a gridlock ({}, {})".format(player, nplayer)
            continue
        
        
        pod.pop(player,None)
        pod.pop(nplayer,None)
        for key in pod:
            if player in pod[key]:
                pod[key].remove(player)
            if nplayer in pod[key]:
                pod[key].remove(nplayer)
        
        
        my_pair = False   
        if found_pair:
            # Add pair to list
            my_pair = (player,nplayer)
            # Move people in standings
            print "Found Pair {0} {1}".format(player,nplayer)
            oldindex = i + 1 + pos_to_move
            stand.insert(i + 1, stand.pop(oldindex))
    return (my_pair, stand)

def complex_pairing(matches, stand):
    print "STANDINGS ARE: {}".format(stand)
    # Create new vars Player Option Dictionary (pod) and player matches dictionary (npod)
    pod = {}
    npod = {}
    # Here we store all the players(values - list) that the player(key) has played.
    for row in matches:
        if row[0] in npod:
            npod[row[0]].append(row[1])
        else:
            npod[row[0]]=[row[1]]
    
    # Here we store all the options(values - list) that the player(key) has.
    for player in stand:
        if not player in pod:
            pod[player]=[];
        for potential in stand:
               if potential==player:
                   continue
               if not potential in npod[player]:
                   pod[player].append(potential)
    
    print "MATCH OPTIONS ARE: {}".format(pod)
    
    # New variable List Of Pairs(lop)
    lop = []
    
    # Loop through all the players and find a pair for each.
    i = 0
    while i < (len(stand)):
        player = stand[i];
        found_pair=False
        pos_to_move = 0
        my_pair, stand = mk_pair(player, i, pod, npod, stand);
        lop.append(my_pair)
        i+=2
        if not my_pair:
            raise Error("Cannot find a possible pair for player {}".format(player))
    
    return lop

