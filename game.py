import numpy as np
import json

class unit:
    name=""
    moves=[[],[]]
    position=(0,0)
    side=0
    def __init__(self,name,moves):
       self.name=name
       self.moves=moves
       self.side=0
        

class game:

	def __init__(self):
	    self.board_arr=np.full([6,6],'_')
	    self.biard_dict=dict()
	    #initialize both decks
	    #d-duke,f-footman,p-pikeman,k-knight,s-seer,w-wizard,c-champion,
	    #g-dragoon,e-general,n-captain(marshal),a-assassin,r-ranger,t-priest,b-bowman,l-longbowman
	    self.whitequeue=['F','P','P','P','K','S','W','C','G','E','N','A','R','T','B','L']
	    np.random.shuffle(self.whitequeue)
	    self.whitequeue=np.concatenate((['D','F','F'],self.whitequeue))
	    
	    self.blackqueue=['f','p','p','p','k','s','w','c','g','e','n','a','r','t','b','l']
	    np.random.shuffle(self.blackqueue)
	    self.blackqueue=np.concatenate((['d','f','f'],self.blackqueue))
	    
	    self.turns=0 #num of turns
	    self.winner=None #if winning and who is winner
	    self.curr_player=0 #white first
	    self.moves=np.array([]) #format:[[white,black],[white,black],...] 
	    #each move is <unit>+<grid>+<movement>+<dest>. 
	    #e.g.: Ka4ma9 means white knight at a4 moves to a9 (this is off-rule gibberish sadhfgjhsd) i need a parser
	    #type of move: m(movement-whether move,jump,slide,js, djsgajf), c(capture, without moving), e(enter, spawning next to duke) 
	    self.wasted=np.array([]) #queue of deadbodies
	    
	#utils
	def position(self,coord=None,pair=None):
	    # a1<=>(0,0) and so on
	    if (coord is None and pair is not None):
	        x,y=pair
	        return chr(x+97)+str(y+1) 
	    elif (pair is None and coord is not None):
	        return (ord(coord[0])-97,int(coord[2])-1)
	    else:
	        raise ValaueError("incorrect values")
	#game in action funcs
	

