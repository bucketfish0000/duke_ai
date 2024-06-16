import game_utils
from game_utils import game
import game_ctrl
from game_ctrl import controller
import argparse

def main():
	gc=controller()
	while(True):
		cmd = input()
		if (cmd=="moves"):
			print(gc.g.get_valid_moves(gc.g.player))
		else:
			gc.proceed(cmd,display=True)
			

if __name__ == "__main__":

	main()

