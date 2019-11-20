import numpy as np
from Question import Question, is_numeric
import pandas as pd
from math import log2
from Node import Node


class DecisionTree:
    def __init__(self, questions, data):
        self.questions = questions
        self.data = data
        self.root_node = None
        self.info_gains = {}

    def simple_entropy(self, target_num_list):
        ret_sum = 0
        for num in target_num_list:
            prob = num / np.sum(target_num_list)
            if prob == 0:
                continue
            ret_sum = ret_sum - prob * log2(prob)

        return ret_sum

    def compound_entropy(self, question, data):
        # FULL FORMULA: P(color == 'Green') * simple_entropy([counts <<OF FRUIT>> where fruit == 'green']) + P (color != 'green) * simple_entropy([counts where fruit !== 'green'])
        occurances = data[question.column].value_counts()
        target_occ = occurances.loc[question.value]
        all_occurances = sum(occurances)
        prob = target_occ / all_occurances
        non_targ_occ = all_occurances - target_occ
        prob_not = non_targ_occ / all_occurances

        target_fruit_dict = {}
        non_target_dict = {}

        for index, row in data.iterrows():
            targ = row[-1]
            if targ not in target_fruit_dict:
                target_fruit_dict[targ] = 0
                non_target_dict[targ] = 0

                if row[question.column] is question.value:
                    target_fruit_dict[targ] += 1
                else:
                    non_target_dict[targ] += 1

            elif row[question.column] is question.value:
                target_fruit_dict[targ] += 1

            elif row[question.column] is not question.value:
                non_target_dict[targ] += 1

        return prob * self.simple_entropy(list(target_fruit_dict.values())) + prob_not * self.simple_entropy(
            list(non_target_dict.values()))

    def calc_info_gains(self):
        for question in all_questions:
            self.info_gains[question] = self.compound_entropy(question, train_data)

        self.info_gains = dict(sorted(self.info_gains.items(), key=lambda x: x[1], reverse=True))

    def build_tree(self):
        self.root_node = Node(list(self.info_gains.keys())[0] )
        self.root_node.true_branch, self.root_node.false_branch = self.partition(self.root_node.question, self.data)

        print('TRUE BRANCH: ---------------')
        for item in self.root_node.true_branch:
            print(item)

        print('FALSE BRANCH: ---------------')
        for item in self.root_node.false_branch:
            print(item)


    def partition(self, split_question, rows):
        true_arr = []
        false_arr = []

        for row in rows.iterrows():
            if split_question.operator is '>=':
                if row[1][split_question.column] > split_question.value:
                    true_arr.append
                    continue
            else:

                if row[1][split_question.column] == split_question.value:
                    true_arr.append(row)
                    continue
            false_arr.append(row)

        return true_arr, false_arr

    def print_tree(self):
        pass


def generate_all_questions(train_df):
    questions = []

    for col in train_df.columns:
        for row in train_df[col]:
            if is_numeric(row):
                operator = '>='
            else:
                operator = '=='

            temp_question = Question(col, row, operator)
            questions.append(temp_question)

    return questions


def unique_questions(all_questions):
    quest_strings = []
    ret_questions = []

    for question in all_questions:
        if question.print_str not in quest_strings:
            quest_strings.append(question.print_str)
            ret_questions.append(question)

    return ret_questions


raw_data = [
    ['Green', 3, 'Apple'],
    ['Yellow', 3, 'Apple'],
    ['Red', 1, 'Grape'],
    ['Red', 1, 'Grape'],
    ['Yellow', 3, 'Lemon']
]

train_data = pd.DataFrame(raw_data, columns=['Color', 'Diameter', 'Fruit'])
columns = train_data.columns

all_questions = unique_questions(generate_all_questions(train_data))
d = DecisionTree(all_questions, train_data)
d.calc_info_gains()
d.build_tree()
d.print_tree()
