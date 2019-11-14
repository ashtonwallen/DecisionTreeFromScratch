import numpy as np
from math import log

class DecisionTree:
    def __init__(self, questions):
        self.questions = questions
        self.root_node = None
        self.info_gains = {} # dict, question to info gain

    def entropy(self, p_rows, q_rows):
        total = p_rows + q_rows
        prob_p = p_rows/total
        prob_q = q_rows/total

        return -(prob_p) * log(prob_p) - (prob_q) * log(prob_q)


    def info_gains(self, question, data):
        #system gain
        pass

d = DecisionTree([])
print(d.entropy(2,5))

