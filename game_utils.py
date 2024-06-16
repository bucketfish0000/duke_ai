import numpy as np
import json
import copy

class unit:
	name=""
	moves=[{},{}]
	side=0
	player=-1

	def __init__(self,name,moves,player):
		self.name=name
		self.moves=copy.deepcopy(moves)
		self.side=0
		self.player=player
		self.make_tuple()
	def make_tuple(self):
		for side in self.moves:
			for t in side.keys():
				ml=[]
				for m in side[t]:
					ml.append(tuple(m))
				side.update({t:ml})

	def rotate(self):
		for side in self.moves:
			for t in side.keys():
				ml=[]
				for m in side[t]:
					t_2 = (-m[0],-m[1])
					ml.append(t_2)
				side.update({t:ml})
        

class game:
	def __init__(self,unit_path,translate_path):
		self.board_arr=np.full([6,6],'_')
		self.board_dict={} #{position:unit obj}
	    
		#initialize both decks
		self.deck=[]
		self.deck.append(['F','P','P','P','K','S','W','C','G','E','N','A','R','T','B','L'])
		np.random.shuffle(self.deck[0])
		self.deck[0]=np.concatenate((['D','F','F'],self.deck[0]))
	    
		self.deck.append(['f','p','p','p','k','s','w','c','g','e','n','a','r','t','b','l'])
		np.random.shuffle(self.deck[1])
		self.deck[1]=np.concatenate((['d','f','f'],self.deck[1]))

		self.turns=0 #num of turns
		self.winner=None #if winning and who is winner
		self.player=0 #white first
		self.moves=np.array([]) #format:[[white,black],[white,black],...] 
	    #each move is <unit>+<grid>+<movement>+<dest>. 
	    #e.g.: Ka4ma9 means white knight at a4 moves to a9 (this is off-rule gibberish sadhfgjhsd) i need a parser
	    #type of move: m(movement-whether move,jump,slide,js, djsgajf), x(strike, without moving), o(enter, spawning next to duke), i(instruct/command)
		self.wasted=[] #queue of deadbodies
		self.unit_dict=self.load_dict(unit_path)
		self.names=self.load_dict(translate_path)
		self.valid_moves=[]

	def clear(self):
		self.board_arr=np.full([6,6],'_')
		self.board_dict={} #{position:unit obj}

		self.deck=[]
		self.deck.append(['F','P','P','P','K','S','W','C','G','E','N','A','R','T','B','L'])
		np.random.shuffle(self.deck[0])
		self.deck[0]=np.concatenate((['D','F','F'],self.deck[0]))
	    
		self.deck.append(['f','p','p','p','k','s','w','c','g','e','n','a','r','t','b','l'])
		np.random.shuffle(self.deck[1])
		self.deck[1]=np.concatenate((['d','f','f'],self.deck[1]))

		self.turns=0 #num of turns
		self.winner=None #if winning and who is winner
		self.player=0 #white first
		self.moves=np.array([]) #format:[[white,black],[white,black],...] 
	    #each move is <unit>+<grid>+<movement>+<dest>. 
	    #e.g.: Ka4ma9 means white knight at a4 moves to a9 (this is off-rule gibberish sadhfgjhsd) i need a parser
	    #type of move: m(movement-whether move,jump,slide,js, djsgajf), x(strike, without moving), o(enter, spawning next to duke), i(instruct/command)
		self.wasted=[] #queue of deadbodies

		
	def check_win(self):
		if (self.board_arr.contains('d')==False): self.winner=1
		elif (self.board_arr.contains('D')==False):self.winner=0

	#utils
	def position(self,coord=None,pair=None):
    # a1<=>(0,0) and so on
		if (coord is None and pair is not None):
			x,y=pair
			return chr(x+65)+str(y+1) 
		elif pair is None and coord is not None:
			return ord(coord[0]) - 65, int(coord[1]) - 1
		else:
			return
			#raise ValaueError("incorrect values")
	        
	def rot_around(self,pair):
		return [0-pair[0],0-pair[1]]
	def is_occupied(self,pos):
		return (self.board_arr[pos] != '_')
	def is_white(self,pos):
		return(self.board_arr[pos].isupper())
	def is_black(self,pos):
		return(self.board_arr[pos].islower())
	def is_friendly(self,player,pos):
		if (player==0): 
			return self.is_white(pos)
		else: 
			return self.is_black(pos)
			
	def is_inbound(self,dest):
		return (dest[0]>=0) and (dest[0]<=5) and (dest[1]>=0) and (dest[1]<=5)
	
	def load_dict(self,path):
		with open(path, 'r') as json_file:
			return json.load(json_file)
        
	#game in action funcs
	def draw_from_deck(self,player,pos):
		#draw a unit from deck and put at position (checked to be valid)
		
		#mark thing on the board
		self.board_arr[pos]=self.deck[player][0]
		#construct unit obj from name and put in board dict
		new_name=self.names[self.deck[player][0].upper()]
		new_moves=self.unit_dict[new_name]
		new_unit=unit(name=new_name,moves=new_moves,player=player)
		if player == 1: 
			new_unit.rotate() #black units be flipped around before put in
		#link unit to board pos
		self.board_dict.update({pos:new_unit})
		self.deck[player]=self.deck[player][1:]

	def move_unit(self,start,dest):
		#move a unit from start grid to dest grid (the move is checked to be valid)
		
		#remove any enemy units in dest
		if self.board_arr[dest] != '_':
			self.wasted.append(self.board_arr[dest])
			self.board_dict.pop(dest)
			self.board_arr[dest] = '_'
			
		self.board_dict.update({dest:self.board_dict[start]})
		self.board_dict.pop(start)
		
		self.board_arr[dest] = self.board_arr[start]
		self.board_arr[start] = '_'
		
	def get_valid_moves(self,player):
		#the assumption: each unit on board would also be recorded in the board dict
		vl=[]
		#cmd_tiles=[]
		####
		'''
		do position+unit move offsets and check
		conditions:
			1.within bound;
			2.destn not occupied by friendly
			3.not hindered by units (for slide and move)
		after normal movement check, look up for commanding tiles and put additional cmd movement in
		'''
		#can only place duke on T1
		if self.turns == 0:
			if self.player==0: vl=["oF1","oF2","oF3","oF4","oF5","oF6"]
			if self.player==1: vl=["oA1","oA2","oA3","oA4","oA5","oA6"]
			return vl
		#do normal movement check	
		for tile_start in self.board_dict.keys(): #--tuple
			if (self.board_dict[tile_start].player != player): continue
			u=self.board_dict[tile_start]
			u_name=self.board_arr[tile_start]
			u_loc=self.position(coord=None,pair=tile_start)
			for move_type in u.moves[u.side].keys():
				if (self.turns<3):
					if move_type =='o':
						u_op='o'
						for tar in u.moves[u.side][move_type]:
							dest = (tar[0]+tile_start[0],tar[1]+tile_start[1])
							if (self.is_inbound(dest)) and self.is_occupied(dest)==False:
								u_tar=self.position(coord=None,pair=dest)
								u_move=u_op+u_tar
								vl.append(u_move)
					else:
						continue
					return vl
				if move_type =='o':
					u_op='o'
					if move_type =='o':
						u_op='o'
						for tar in u.moves[u.side][move_type]:
							dest = (tar[0]+tile_start[0],tar[1]+tile_start[1])
							if (self.is_inbound(dest)) and self.is_occupied(dest)==False:
								u_tar=self.position(coord=None,pair=dest)
								u_move=u_op+u_tar
								vl.append(u_move)
				elif move_type == 'm':
					u_op='m'
					for tar in u.moves[u.side][move_type]:
						dest = (tar[0]+tile_start[0],tar[1]+tile_start[1])
						#print(dest)
						if (dest[0]<0 or dest[0]>5 or dest[1]<0 or dest[1]>5) or self.is_friendly(player,dest):
							#move cannot end up in out-of-bound or friendly tiles
							continue
						#move cannot be hindered
						#print(dest)
						hindered=False
						line_cast=(tar[0]!=0,tar[1]!=0) #using the features that all official "move"s are on same line/row or on diag
						check_dest=tile_start
						while (check_dest != dest and self.is_inbound(check_dest)):
							check_dest=(check_dest[0]+line_cast[0],check_dest[1]+line_cast[1])
							if self.is_inbound(check_dest) and self.is_occupied(check_dest): hindered=True
						#print(dest,hindered)
						if (hindered): break
						#anything reaching this line would be valid slide moves, translate and put into vl 
						u_tar=self.position(coord=None,pair=dest)
						#		'K'    "a4" 'm'  'a5'
						u_move=u_name+u_loc+u_op+u_tar
						vl.append(u_move)
						
				elif move_type == 'j':
					u_op='m'
					for tar in u.moves[u.side][move_type]:
						dest = (tar[0]+tile_start[0],tar[1]+tile_start[1])
						if (dest[0]<0 or dest[0]>5 or dest[1]<0 or dest[1]>5) or self.is_friendly(player,dest):
							#jump cannot end up in out-of-bound or friendly tiles
							continue
						#anything reaching this line would be valid slide moves, translate and put into vl 
						u_tar=self.position(coord=None,pair=dest)
						#		'K'    "a4" 'm'  'a5'
						u_move=u_name+u_loc+u_op+u_tar
						vl.append(u_move)
				
				elif move_type == 's':#resolve destiniations of sliding
					u_op='m'
					for direction in u.moves[u.side][move_type]:
						dest=tile_start
						dest=(dest[0]+direction[0],dest[1]+direction[1])
						hindered=False
						while (self.is_inbound(dest) and hindered==False):
							#can keep location if is within bound, empty
							print(dest)
							if (self.is_friendly(player,dest)):
								hindered=True
								break  
							elif (self.is_occupied(dest)):
								hindered=True
							u_tar=self.position(coord=None,pair=dest)
							#		'K'    "a4" 'm'  'a5'
							u_move=u_name+u_loc+u_op+u_tar
							vl.append(u_move)
							dest=(dest[0]+direction[0],dest[1]+direction[1])

				elif move_type == 'l':
					u_op='m'
					for direction in u.moves[u.side][move_type]:
						dest=tile_start
						while (self.is_inbound(dest)): 
							#can keep location if is within bound, empty
							dest=(dest[0]+direction[0],dest[1]+direction[1])
							if (self.is_friendly(player,dest)):
								continue
							#anything reaching this line would be valid slide moves, translate and put into vl                       
							u_tar=self.position(coord=None,pair=dest)
							#		'K'    "a4" 'm'  'a5'
							u_move=u_name+u_loc+u_op+u_tar
							vl.append(u_move)
				elif move_type == 'k':
					u_op='x'
					for tar in u.moves[u.side][move_type]:
						dest = (tar[0]+tile_start[0],tar[1]+tile_start[1])
						if (dest[0]<0 or dest[0]>5 or dest[1]<0 or dest[1]>5) or self.is_friendly(player,dest) or (self.is_occupied(dest)!=True):
							#strike cannot end up in out-of-bound or or empty or friendly tiles
							break
						#anything reaching this line would be valid slide moves, translate and put into vl 
						u_tar=self.position(coord=None,pair=dest)
						#		'K'    "a4" 'm'  'a5'
						u_move=u_name+u_loc+u_op+u_tar
						vl.append(u_move)
					
							
		
		for tile_start in self.board_dict.keys(): #--tuple
			u=self.board_dict[tile_start]
			u_name=self.board_arr[tile_start]
			u_loc=self.position(coord=None,pair=tile_start)
			for move_type in u.moves[u.side].keys():
				if move_type == 'c':
					for cmd in u.moves[u.side][move_type]:
						dest = (cmd[0]+tile_start[0],cmd[1]+tile_start[1])
						if not(dest[0]<0 or dest[0]>5 or dest[1]<0 or dest[1]>5) and self.is_friendly(player,dest):
							#valid command, look for friendly moves under command
							for friendly_move in vl:
								if (friendly_move[1:3]==self.position(coord=None,pair=dest)) and (friendly_move[3] != 'c'):
									u_move==u_name+u_loc+'i'+friendly_move
									vl.append(u_move)				
		####
		self.valid_moves=vl
		return vl
		
	def execute_moves(self,player,move_str,flip=True):
		#execute move from string representing move
		if (move_str not in self.valid_moves):
			raise Exception("move is not valid")
		else:
			if move_str[0]=='o':#spawn
				self.draw_from_deck(player,pos=self.position(coord=move_str[1:],pair=None))
			else:
				init=self.position(coord=move_str[1:3],pair=None)
				if move_str[3]=='i':#command
					self.execute_moves(move_str[4:],flip=False)
				else:
					start=self.position(coord=move_str[1:3],pair=None)
					dest=self.position(coord=move_str[4:6],pair=None)
					if move_str[3]=='m':#move
						init=dest
						self.move_unit(start,dest)
					elif move_str[3]=='x': #take
						self.wasted.append(self.board_arr[dest])
						self.board_dict.pop(dest)
						self.board_arr[dest]='_'
				if flip==True:
					self.board_dict[init].side ^=1
		return
					
				
				

