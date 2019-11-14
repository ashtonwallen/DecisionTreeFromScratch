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


training_data = [
    ['Green', 3, 'Apple'],
    ['Yellow', 3, 'Apple'],
    ['Red', 1, 'Grape'],
    ['Red', 1, 'Grape'],
    ['Yellow', 3, 'Lemon']
]


def generate_all_questions(train_df):
    questions = []

    for col in train_df.columns:
        for row in train_df[col]:
            if is_numeric(row):
                operator = '>'
            else:
                operator = '=='

            temp_question = Question(col, row, operator)
            questions.append(temp_question)

    return questions


def is_numeric(value):
    return isinstance(value, Number)


train_data = pd.DataFrame(training_data, columns=['Color', 'Diameter', 'Fruit'])
columns = train_data.columns

all_questions = generate_all_questions(train_data)
real_questions = []

for question in all_questions:
    question.print_question()
