# process ---
# start w dataset
# generate all questions
# determine best question to ask -> first splitting point
# test rows against condition to split the data (false node, true node)
# if no data to separate two different things, pick randomly

# ----

# information gain
#


import pandas as pd
from numbers import Number


class Question:
    def __init__(self, column, value, operator):
        self.column = column
        self.value = value
        self.operator = operator

    def answer(self):
        pass

    def print_question(self):
        if is_numeric(self.value):
            print('Is ' + str(self.column) + ' ' + self.operator + ' ' + str(self.value))
        else:
            print('Is ' + str(self.column) + ' == ' + str(self.value))



def is_numeric(value):
    return isinstance(value, Number)
