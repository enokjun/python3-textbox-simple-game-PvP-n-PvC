# python3-textbox-simple-game-PvP-n-PvC
PvP or PvC text input games in Python3

# Game rules
purpose: Creating a simple game to learn how to use tkinter module

name: game-theory LTK-simplified

moves: charge, attack, defend, ult attack, heal

play-mode: player vs computer (PvC) or player vs player (PvP)

game rules: 
> p = player, c = computer

> p chooses a move to make at each turn

> both p and c has total life of 3

> to use skills, needs to charge. when charge = 2, can use a skill:
	
	- heal (own: life+1; cost: charge=2)
	
	- ult attack (enemy: life-2; cost:charge=3)

> depending on these combinations, these outcomes occur:
	[/ means or;  | means and; first position is player1 move and second position is computer move]
	
	- [c,c], [c,d], [d,d], [a,d], [a,h] = nothing
	
	- [a,c], [u,h], [u,d] = c (life)-1
	
	- [u,c] = c (life)-2
	
	- [h,c], [h,d] = p (life)+1
	
	- [a,a] = p|c (life)-1
	
	- [u,a] = p (life)-1, c (life)-2
	
	- [u,u] = p|c (life)-2
   
   	- q = quit/surrender
	
> charge max = 3

> life max = inital life

> winning condition: enemy (life)<=0
