import game_utils
from game_utils import game
import game_ctrl
from game_ctrl import controller
import argparse

def main():
	gc=controller()
	while(True):
		cmd = input()
		gc.input=cmd
		_=gc.game_routine(display=True)
			

if __name__ == "__main__":

	main()

