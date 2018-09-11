"""
Created on Wed Sep 07 2016
pvp version created on Sat Jan 06 2018

@author: Enok C.

Gameplay
"""
"""
purpose: Creating a simple game to learn how to use tkinter module
name: game-theory LTK-simplified
moves: charge, attack, defend, ult attack, heal
play-mode: player1 vs player2
game rules: 
	> p1 = player1, p2 = player2
	> p1 and p2 chooses a move to make at each turn
	> both p1 and p2 has total life of 3
	> to use skills, needs to charge. when charge = 2, can use a skill:
		- heal (own: life+1; cost: charge=2)
		- ult attack (enemy: life-2; cost:charge=3)
	> depending on these combinations, these outcomes occur for the player:
	[/ means or;  | means and;  
	first position is player1 move and second position is player2 move]
		- [c,c], [c,d], [d,d], [a,d], [a,h] = nothing
		- [a,c], [u,h], [u,d] = p2 (life)-1
		- [u,c] = p2 (life)-2
		- [h,c], [h,d] = p1 (life)+1
		- [a,a] = p1|p2 (life)-1
		- [u,a] = p1 (life)-1, p2 (life)-2
		- [u,u] = p1|p2 (life)-2
	> q = quit/surrender
	> charge max = 3
	> life max = 3
winning condition: enemy (life)<=0
"""

'''initial game setting'''
# inital game set-up parameters
in_charge = 0
max_charge = 3
in_life = 3

'''player setting'''
# check player input
def player(info,in_life,max_charge):
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
                        if move in ['ult attack','u'] and charge >= 3:
                            break
                        elif move in ['ult attack','u'] and charge < 3:
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
        elif move in ['heal','h'] and charge < 2:
            print('not enough charge to use heal(h): you need at least 2 charges') 
            print()
            while True:
                move = input("input your move\n [attack(a), defend(d), charge(c), heal(h), ult attack(u) or quit(q)]:  ")
                print()
                if move not in ['heal','h','ult attack','u']:
                    break
                
        # when move input is 'h' and charge is enough
        elif move in ['heal','h'] and charge >= 2:
            charge -= 2
            break
                    
        # when move input is 'u' and charge is not enough
        elif move in ['ult attack','u'] and charge < 3:
            print('not enough charge to use ult attack(u): you need min 3 charge') 
            print()
            while True:
                move = input("input your move\n [attack(a), defend(d), charge(c), heal(h), ult attack(u) or quit(q)]:  ")
                print()
                if move not in ['ult attack','u']:
                    break
        
        # when move input is 'u' and charge is enough
        elif move in ['ult attack','u'] and charge >= 3:
            charge -= 3
            break
                
        # when move input is wrong or not among possible moves      
        else:
            print('wrong input')
            print()
            move = input("input your move\n [attack(a), defend(d), charge(c), heal(h), ult attack(u) or quit(q)]:  ")
            
    # sort output
    info = [life,charge]
    
    return info, move

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

def play_game(in_charge,in_life):
       
    while True:
        # initial game setting
        p1_info = [in_life, in_charge]
        p2_info = [in_life, in_charge]
        
        print('\ngame rules-------------------------------------')
        print('> p1 = player1, p2 = pla1ayer2\n> p1 and p2 chooses a move to make at each turn')
        print('> both p1 and p2 has total life of 3')
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
        print('winning condition: enemy (life)<=0 or one of the player quits')
        print()
        
        print('\n game start\n')
        
        # play the game
        while True:
            for n in range(0,5):
                print()
                
            # player1 move
            print('player1-------------------------------------')
            p1_info, p1_move = player(p1_info,in_life,max_charge)
            
            for n in range(0,40):
                print()
            
            # player2 move
            print('player2-------------------------------------')
            p2_info, p2_move = player(p2_info,in_life,max_charge)
            
            for n in range(0,40):
                print()
                
            if p1_move in ['quit','q'] and p2_move not in ['quit','q']:
                print("player1's move =  %s" %p1_move)
                print('\nPlayer2 won!!\n')
                break
            elif p1_move not in ['quit','q'] and p2_move in ['quit','q']:
                print("player2's move =  %s" %p2_move)
                print('\nPlayer1 won!!\n')
                break
            elif p1_move in ['quit','q'] and p2_move in ['quit','q']:
                print("player1's move =  %s" %p1_move)
                print("player2's move =  %s" %p2_move)
                print('\nDraw!!\n')
                break
                
            # match outcome
            p1_info, p2_info, match = match_outcome(p1_info, p1_move, p2_info, p2_move)
    
            # display
            print("\nplayer1's move =  %s" %match[0])
            print("player2's move =  %s" %match[1])
            print("\nplayer1: [life, charge] = [%i,%i]" %(p1_info[0],p1_info[1]))
            print("player2: [life, charge] = [%i,%i]" %(p2_info[0],p2_info[1]))  
                
            # check game progress and end result
            if p1_info[0] > 0 and p2_info[0] <= 0:
                print('\nPlayer1 won!!\n')
                break
            elif p1_info[0] <= 0 and p2_info[0] > 0:
                print('\nPlayer2 won!!\n')
                break
            elif p1_info[0] <= 0 and p2_info[0] <= 0:
                print('\nDRAW!\n')
                break
            elif p1_info[0] > 0 and p2_info[0] > 0:
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
play_game(in_charge,in_life)