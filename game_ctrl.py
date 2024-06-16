import game_utils
from game_utils import game

class controller:
    def __init__(self,unit="units.json",translate="translate.json"):
        self.g = game(unit,translate)
        self.state="idle"
    
    def proceed(self,op,display=False):
        if self.state=="idle":
            self.g.clear()
            self.g.player=0
            if (display): print(self.g.board_arr)
            if op=="new":
                self.state="white_move"
                return
        elif self.state=="white_move":
            #op is move taken
            #self.g.turns+=1
            self.g.player=0
            self.g.valid_moves=self.g.get_valid_moves(0)
            self.g.execute_moves(player=0,move_str=op)
            if (display): 
                print(self.g.board_arr)
            if self.g.winner!=None:
                self.state="end"
            else:
                self.state="black_move"
            return
        elif self.state=="black_move":
            self.g.player=1
            self.g.valid_moves=self.g.get_valid_moves(1)
            self.g.execute_moves(player=1,move_str=op)
            if (display): 
                print(self.g.board_arr)
            if self.g.winner!=None:
                self.state="end"
            else:
                self.state="white_move"
                self.g.turns+=1
            return
        elif self.state=="end":
            if  op=="initiate":
                self.state="idle"
                return self.g.winner
            if (display): print(self.g.board_arr)
        return
