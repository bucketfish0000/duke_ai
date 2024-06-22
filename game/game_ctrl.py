import game_utils
from game_utils import game

class controller:
    def __init__(self,unit="units.json",translate="translate.json"):
        self.g = game(unit,translate)
        self.state="idle"
        self.next="idle"
        self.input=None

    def game_routine(self,display=True):
        
        cmd=self.input
        self.input=None

        if ((self.state=="wait_w_move"))and(cmd != "moves"):
            self.g.valid_moves=self.g.get_valid_moves(0)
            self.state="take_w_move"
        if ((self.state=="wait_b_move"))and(cmd != "moves"):
            self.g.valid_moves=self.g.get_valid_moves(1)
            self.state="take_b_move"

        if self.state=="idle":
            if (cmd==None):return
            self.g.clear()
            self.g.player=0
            if (display): print(self.g.board_arr)
            if cmd=="new":
                self.next="wait_w_move"
            else: self.next="idle"
        elif self.state=="wait_w_move":
            if (cmd==None):return
            self.g.valid_moves=self.g.get_valid_moves(0)
            if (cmd=="moves"):
                print(self.g.valid_moves)
            self.next="take_w_move"

            ml=self.g.valid_moves
            print(ml)
            return ml
        elif self.state=="take_w_move":
            if (cmd==None):return
            self.g.execute_moves(player=self.g.player,move_str=cmd)
            if (display): 
                print(self.g.board_arr)
            self.g.player ^=1
            self.g.check_win()
            if self.g.winner!=None:
                self.next="end"
            else:
                self.next="wait_b_move"
        elif self.state=="wait_b_move":
            if (cmd==None):return
            self.g.valid_moves=self.g.get_valid_moves(1)
            if (cmd=="moves"):
                print(self.g.valid_moves)
            self.next="take_b_move"
            return(self.g.valid_moves)
        elif self.state=="take_b_move":
            if (cmd==None):return
            self.g.execute_moves(player=self.g.player,move_str=cmd)
            if (display): 
                print(self.g.board_arr)
            self.g.player ^=1
            self.g.check_win()
            if self.g.winner!=None:
                self.next="end"
            else:
                self.next="wait_w_move"
                self.g.turns+=1
        elif self.state=="end":
            if cmd=="initiate":
                self.state="idle"
                self.next="idle"
                return self.g.winner
            if (display): print(self.g.board_arr) 
        
        self.state=self.next
        
>>>>>>> d33d80e3a67599b1e6db5303592aa3ccea508bcf
