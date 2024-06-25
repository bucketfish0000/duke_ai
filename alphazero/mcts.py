import math
import typing
import numpy as np
import tensorflow as tf


class MCTS():
    def __init__(self,observation,f,g,h):
        self.f = f #prediction
        self.h = h #representation
        self.g = g #dynamics
        self.root = f(observation)
        self.Ns = {}
        self.Ps = {}
        self.Es = {}
        self.Vs = {}

    def clear_tree(self):
        None
    
    def root_init(self):
        None