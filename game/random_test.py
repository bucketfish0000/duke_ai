import game_utils
from game_utils import game
import game_ctrl
from game_ctrl import controller
import argparse
import random

def main():
    gc=controller()
    i = 0
    while i < 10000000:
        i+=1
        if i%100==0: print(i)
        while(gc.state!="end"):
            #print(gc.input)
            ml=gc.game_routine(display=False)
            #print(gc.g.turns,gc.state)
            #print(gc.g.valid_moves,ml)
            #if gc.state=="take_w_move": return
            if gc.state=="idle":
                gc.input="new"
            else:
                if gc.state=="take_w_move" or gc.state=="take_b_move":
                    gc.input=random.sample(gc.g.valid_moves,1)[0]
                else:
                    gc.input=None
                
			
if __name__ == "__main__":

	main()
     