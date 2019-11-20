import numpy as np
from Question import Question, is_numeric
import pandas as pd

class DecisionTree:
    def __init__(self, questions):
        self.questions = questions
        self.root_node = None
        self.info_gains = {} # dict, question to info gain

        # comes in as 5 oranges, 4 apples, 2 lemons
        # pass to simple_ent ([5,4,2])
    def simple_entropy(self, target_num_list):
        ret_sum = 0
        for num in target_num_list:
            prob = num / np.sum(target_num_list)
            ret_sum = ret_sum - prob * np.log(prob)

        return ret_sum


    def compound_entropy(self, question, data):
        # probabity of color == green * simple_entropy(counts of fruits where color is 'green')
        # second part: ^ + probability color != green * simpleentropy(counts of fruits not green)

        # FULL FORMULA: P(color == 'Green') * simple_entropy([counts <<OF FRUIT>> where fruit == 'green']) + P (color != 'green) * simple_entropy([counts where fruit !== 'green'])
        for target in np.unique(data[-1]):
            print(target)


    def calc_info_gains(self):
        # IG(color=='green') = s_entropy(count_target) - complex_entropy(question, data)
        pass





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


training_data = [
        ['Green', 3, 'Apple'],
        ['Yellow', 3, 'Apple'],
        ['Red', 1, 'Grape'],
        ['Red', 1, 'Grape'],
        ['Yellow', 3, 'Lemon']
    ]


train_data = pd.DataFrame(training_data, columns=['Color', 'Diameter', 'Fruit'])
columns = train_data.columns

all_questions = np.unique(generate_all_questions(train_data))

d = DecisionTree(all_questions)

#for question in all_questions:
    #question.print_question()

#for question in all_questions:
   # d.compound_entropy(question, train_data)

