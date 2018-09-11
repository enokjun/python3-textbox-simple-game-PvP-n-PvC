"""
Created on Wed Sep 07 2016

@author: Enok C.

Gameplay
"""

"""
purpose: Creating a simple game to learn how to use tkinter module
name: game-theory LTK-simplified
moves: charge, attack, defend, ult attack, heal
play-mode: player vs computer
game rules: 
	> p = player, c = computer
	> p chooses a move to make at each turn
	> both p and c has total life of 3
	> to use skills, needs to charge. when charge = 2, can use a skill:
		- heal (own: life+1; cost: charge=2)
		- ult attack (enemy: life-2; cost:charge=3)
	> depending on these combinations, these outcomes occur:
	[/ means or;  | means and;  
	first position is player1 move and second position is computer move]
		- [c,c], [c,d], [d,d], [a,d], [a,h] = nothing
		- [a,c], [u,h], [u,d] = c (life)-1
		- [u,c] = c (life)-2
		- [h,c], [h,d] = p (life)+1
		- [a,a] = p|c (life)-1
		- [u,a] = p (life)-1, c (life)-2
		- [u,u] = p|c (life)-2
   > q = quit/surrender
	> charge max = 3
	> life max = inital life
winning condition: enemy (life)<=0
"""

'''initial game setting'''
# inital game set-up parameters
in_charge = 0
max_charge = 3
h_cost = 2
u_cost = 3
in_life = 3
AI_file = [['a,c,d', 'a,c,d', 'a,c,d', 'a,d', 'a,c,d', 'a,c,d', 'a,c,d', 'd', 'a,c,d', 'a,c,d', 'a,c,d', 'd'], ['a,c,d', 'a,c,d', 'a,c,d', 'a,d', 'a,c,d', 'a,c,d', 'a,c,d', 'd', 'a,c,d', 'a,c,d', 'a,c,d', 'd'], ['a,h,d', 'a,h,d', 'a,h,d', 'a,h,d', 'a,h,d', 'a,h,d', 'a,h,d', 'h,d', 'a,h,d', 'a,h,d', 'a,h,d', 'h,d'], ['u,h,d', 'u,h,d', 'u,h,d', 'u,h,d', 'u,h,d', 'u,h,d', 'u,h,d', 'u,h,d', 'u,h,d', 'u,h,d', 'u,h,d', 'u,h,d'], ['a,c', 'a,c', 'a,c', 'a,d', 'a,c,d', 'a,c,d', 'a,c,d', 'a,d', 'a,c,d', 'a,c,d', 'a,c,d', 'a,d'], ['a,c', 'a,c', 'a,c', 'a,d', 'a,c,d', 'a,c,d', 'a,c,d', 'a,d', 'a,c,d', 'a,c,d', 'a,c,d', 'a,d'], ['a,c,h,d', 'a,c,h,d', 'a,c,h,d', 'a,h,d', 'a,c,h,d', 'a,c,h,d', 'a,c,h,d', 'h,d', 'a,c,h,d', 'a,c,h,d', 'a,c,h,d', 'h,d'], ['u', 'u', 'u', 'u,d', 'u,h', 'u,h', 'u,h', 'u,d', 'u,h', 'u,h', 'u,h', 'u,d'], ['a,c', 'a,c', 'a,c', 'a,d', 'a,c', 'a,c', 'a,c', 'a,d', 'a,c', 'a,c', 'a,c', 'a,d'], ['a,c', 'a,c', 'a,c', 'a,d', 'a,c,d', 'a,c,d', 'a,c,d', 'a,d', 'a,c,d', 'a,c,d', 'a,c,d', 'a,d'], ['a,c', 'a,c', 'a,c', 'a,d', 'a,c', 'a,c', 'a,c', 'a,d', 'a,c,d', 'a,c,d', 'a,c,d', 'a,d'], ['u', 'u', 'u', 'u', 'u', 'u', 'u', 'u,d', 'u', 'u', 'u', 'u,d']]
#'comp_reactions_v2.prn'

# previous version:
#[['a,c,d', 'a,c,d', 'a,d', 'c,d', 'a,c,d', 'a,d', 'c,d', 'a,c,d', 'a,d'], ['a,d,h', 'a,h', 'h', 'a,d,h', 'a,h', 'h', 'a,d,h', 'a,h', 'h'], ['u,h', 'u,h', 'u', 'u,h', 'u,h', 'u', 'u,h', 'u,h', 'u'], ['a,c,d', 'a,c,d', 'c,d', 'a,c,d', 'a,c,d', 'c,d', 'a,c,d', 'a,c,d', 'c,d'], ['a,c,d,h', 'a,c,d,h', 'h', 'a,c,d,h', 'a,c,d,h', 'h', 'a,c,d,h', 'a,c,d,h', 'h'], ['u,h', 'u,h', 'u,h', 'u,h', 'u,h', 'u,h', 'u,h', 'u,h', 'u,h'], ['a,c', 'a,c', 'a,c', 'a,c,d', 'a,c,d', 'c,d', 'a,c', 'a,c,d', 'c,d'], ['a,c', 'a,c', 'a,c', 'a,c,d', 'a,c,d', 'c,h', 'a,c,d', 'c,d', 'c,h'], ['u', 'u', 'u', 'u,d', 'u,d', 'u,d', 'u,d', 'u,d', 'u,d']]
#'comp_reactions.prn'


'''player setting'''
# check player input
def player(info,in_life,max_charge,h_cost,u_cost):
    # sort input
    life = info[0]  
    charge = info[1]
    
    # make a move
    move = input("input your move\n [attack(a), defend(d), charge(c), heal(h), ult attack(u) or quit(q)]:  ")
    print()
    while True:
        # when move input is 'h' and life is max
        if life == in_life:
            if move in ['heal','h']:            
                print('your life level is full') 
                print()
                while True:
                    move = input("input your move\n [attack(a), defend(d), charge(c), heal(h), ult attack(u) or quit(q)]:  ")
                    print()
                    if move not in ['heal','h']:
                        if move in ['ult attack','u'] and charge >= u_cost:
                            break
                        elif move in ['ult attack','u'] and charge < u_cost:
                            print('not enough charge to use ult attack(u): you need min charge = 3')
                            print()
                            continue
                        elif move in ['attack','a','defend','d','charge','c','quit','q']:
                            break
                    else:
                        print('your life level is full') 
                        print()
                        continue
                        
        # when move input is 'a' or 'd'
        if move in ['attack','a','defend','d','quit','q']:
            break
        
        # when move input is 'c' and charge didn't reach max limit
        elif move in ['charge','c'] and charge < max_charge:
            charge += 1
            break
        
        # when move input is 'c' and charge reached max limit
        elif move in ['charge','c'] and charge == max_charge:
            print('you are not allowed to charge more than %i' %max_charge)
            print()
            while True:
                move = input("input your move\n [attack(a), defend(d), charge(c), heal(h), ult attack(u) or quit(q)]:  ")
                print()
                if move not in ['c','charge']:
                    break
                
        # when move input is 'h' and charge is not enough
        elif move in ['heal','h'] and charge < h_cost:
            print('not enough charge to use heal(h): you need at least 2 charges') 
            print()
            while True:
                move = input("input your move\n [attack(a), defend(d), charge(c), heal(h), ult attack(u) or quit(q)]:  ")
                print()
                if move not in ['heal','h','ult attack','u']:
                    break
                
        # when move input is 'h' and charge is enough
        elif move in ['heal','h'] and charge >= h_cost:
            charge -= h_cost
            break
                    
        # when move input is 'u' and charge is not enough
        elif move in ['ult attack','u'] and charge < u_cost:
            print('not enough charge to use ult attack(u): you need min 3 charge') 
            print()
            while True:
                move = input("input your move\n [attack(a), defend(d), charge(c), heal(h), ult attack(u) or quit(q)]:  ")
                print()
                if move not in ['ult attack','u']:
                    break
        
        # when move input is 'u' and charge is enough
        elif move in ['ult attack','u'] and charge >= u_cost:
            charge -= u_cost
            break
                
        # when move input is wrong or not among possible moves      
        else:
            print('wrong input')
            print()
            move = input("input your move\n [attack(a), defend(d), charge(c), heal(h), ult attack(u) or quit(q)]:  ")
            
    # sort output
    info = [life,charge]
    
    return info, move

'''computer setting'''
def sort_c_AI(AI_file):
    
    #create AI for computer's moves
    c_AI = open(AI_file,'r')
    c_act = c_AI.readlines()
    
    # sort the data into lists 
    c_move_list = []   
    for i in range(len(c_act)):
        temp_row1 = list(c_act[i]) # turn all elements into individual strings
        
        # find each lists for columns- aka. find ' '
        nonBlank = [] # index for where blanks are located
        for j in range(len(temp_row1)):
            if temp_row1[j] not in ['\n',' ']:
                nonBlank.append(j)
        
        x = [] # start of the col 
        y = [] # end of the col
        for k in range(len(nonBlank)):
            if k == 0:
                x.append(nonBlank[k])
            elif nonBlank[k]-nonBlank[k-1] != 1:
                x.append(nonBlank[k])
                y.append(nonBlank[k-1])
        if len(x)-len(y) == 1:
            y.append(nonBlank[-1])
        
        # join each as string and put into a list
        temp_row2 = []
        for k in range(len(x)):
            col = ''.join(temp_row1[(x[k]):(y[k]+1)])
            #col = ''.join(temp_row1[(x[k]+1):(y[k]+1)])
            temp_row2.append(col)
        
        # append sorted list as row
        c_move_list.append(temp_row2)
     
    return c_move_list

def computer(p_info, c_info, c_move_list, in_life, max_charge, h_cost, u_cost):
    from random import choice
    
    # define row & col for each scenario
    row = 4*(c_info[0]-1) + c_info[1]
    col = 4*(p_info[0]-1) + p_info[1]

    # extract the row & col for move list
    c_move_opt = c_move_list[row][col]
    c_move_opt_list = list(c_move_opt)
    try:
        while ',' in c_move_opt_list:
            c_move_opt_list.remove(',')
    except:
        pass
    
    # remove 'h' when life is max & 'c' when charge is max
    if c_info[0] == in_life or c_info[1] < h_cost:
        if 'h' in c_move_opt_list:
            c_move_opt_list.remove('h')
    if c_info[1] < u_cost:
        if 'u' in c_move_opt_list:
            c_move_opt_list.remove('u')
    if c_info[1] == max_charge:
        if 'c' in c_move_opt_list:
            c_move_opt_list.remove('c')

    #print(row)
    #print(col)
    #print(c_move_opt_list)
        
    # choose a move
    c_move = choice(c_move_opt_list)
       
    # when move input is 'c' and charge didn't reach max limit
    if c_move in ['charge','c'] and c_info[1] < max_charge:
        c_info[1] += 1
    # when move input is 'h' and charge is enough
    elif c_move in ['heal','h'] and c_info[1] >= h_cost:
        c_info[1] -= h_cost
    # when move input is 'u' and charge is enough
    elif c_move in ['ult attack','u'] and c_info[1] >= u_cost:
        c_info[1] -= u_cost 
     
    return c_info, c_move       

''' game play '''
def match_outcome(c_info, c_move, p_info, p_move):
    # sort input data
    c_life = c_info[0]
    p_life = p_info[0]
    match = [c_move, p_move]
    
    '''outcome'''
    # no outcome 
    if match in [['a','h'],['c','c'],['d','d'],['a','d'],['c','d']]:
        pass
    
    # computer looses one life
    elif match in [['c','a'],['h','u'],['d','u']]:
        c_life -= 1
    # player looses one life
    elif match in [['a','c'],['u','h'],['u','d']]:
        p_life -= 1
    # both player and computer looses one life
    elif match == ['a','a']:
        c_life -= 1
        p_life -= 1
    
    # computer looses one life and player loose two lives
    elif match == ['u','a']:
        c_life -= 1
        p_life -= 2
    # computer looses two lives and player loose one life
    elif match == ['a','u']:
        c_life -= 2
        p_life -= 1
    
    # computer looses two lives
    elif match in ['c','u']:
        c_life -= 2
    # player looses two lives
    elif match in ['u','c']:
        p_life -= 2
    # both player and computer looses two lives
    elif match == ['u','u']:
        c_life -= 2
        p_life -= 2
    
    # computer gains one life
    elif match in [['h','c'],['h','d']]:
        c_life += 1
    # player gains one life
    elif match in [['c','h'],['d','h']]:
        p_life += 1
    # both player and computer gains one life
    elif match == ['h','h']:
        c_life += 1
        p_life += 1
    
    c_info[0] = c_life 
    p_info[0] = p_life        
    
    return c_info, p_info, match

def play_game(in_charge, in_life, max_charge, h_cost, u_cost, AI_file):
    # computer possible moves    
    c_move_list = AI_file #sort_c_AI(AI_file) 
    
    while True:
        # initial game setting
        p_info = [in_life, in_charge]
        c_info = [in_life, in_charge]
        
        print('\ngame rules-------------------------------------')
        print('> p = player, c = computer\n> p and c chooses a move to make at each turn')
        print('> both p and c has total life of 3')
        print('> to use skills, needs to charge. when you have enough charge, can use a skill:\n - heal (own: life+1; cost: charge=2)\n - ult attack (enemy: life-2; cost:charge=3)')
        print('> depending on these combinations, these outcomes occur for the player:\n[| means and; 1st position is player1 move and 2nd position is player2 move]')
        print('- [c,c], [c,d], [d,d], [a,d], [a,h] = nothing')
        print('- [a,c], [u,h], [u,d] = p2 (life)-1')
        print('- [u,c] = p2 (life)-2')
        print('- [h,c], [h,d] = p1 (life)+1')
        print('- [a,a] = p1|p2 (life)-1')
        print('- [u,a] = p1 (life)-1, p2 (life)-2')
        print('- [u,u] = p1|p2 (life)-2')
        print('> charge max limit is 3')
        print('> life max limit is 3')
        print('winning condition: enemy (life)<=0 or the player quits')
        print()
        print('\n game start\n')

        # play the game
        while True:
            # player's move
            print('-------------------------------------')
            p_info, p_move = player(p_info,in_life,max_charge, h_cost, u_cost)
    
            # computer's move
            c_info, c_move = computer(p_info, c_info, c_move_list, in_life, max_charge, h_cost, u_cost)
            
            if p_move in ['quit','q']:
                print("player's move =  %s" %p_move)
                print('\nComputer won!!\n')
                break
            
            # match outcome
            c_info, p_info, match = match_outcome(c_info, c_move, p_info, p_move)
            
            # display
            print("\ncomputer's move =  %s" %match[0])
            print("player's move =  %s" %match[1])
            print("\ncomputer: [life, charge] = [%i,%i]" %(c_info[0],c_info[1]))
            print("player: [life, charge] = [%i,%i]" %(p_info[0],p_info[1]))
    
            # check game progress and end result
            if p_info[0] <= 0 and c_info[0] > 0:
                print('\nComputer won\n')
                break
            elif p_info[0] > 0 and c_info[0] <= 0:
                print('\nCongratulaition!! You have won!\n')
                break
            elif c_info[0] <= 0 and p_info[0] <= 0:
                print('\nDRAW!\n')
                break
            elif c_info[0] > 0 and p_info[0] > 0:
                continue
       
        # replay
        replay = input("replay? [y,n]:    ")
        if replay == 'y':
            continue
        elif replay == 'n':
            print("see you again - later!")
            break
        else:
            print("wrong input")
            while replay not in ['y','n']:
                replay = input("replay? [y,n]:    ")
            if replay == 'y':
                continue
            elif replay == 'n':
                print("\nplay again - later!\n")
                break
               
'''play the game'''  
#c_move = sort_c_AI(AI_file)
#print(c_move)
play_game(in_charge, in_life, max_charge, h_cost, u_cost, AI_file)