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
        self.print_str = self.question_to_str()

    def question_to_str(self):
        return 'Is ' + str(self.column) + ' ' + self.operator + ' ' + str(self.value)




def is_numeric(value):
    return isinstance(value, Number)
