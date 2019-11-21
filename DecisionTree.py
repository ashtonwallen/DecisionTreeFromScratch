import numpy as np
from Question import Question, is_numeric
import pandas as pd
from math import log2
from Node import Node, LeafNode

# some inspiration for thing like printing the tree came from : https://github.com/random-forests/tutorials/blob/master/decision_tree.py


class DecisionTree:
    def __init__(self, questions):
        self.questions = questions

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

    def calc_best_info_gains(self, questions, data):
        best_gain = 0
        best_question = None

        for question in questions:
            true, false = self.partition(question, data)

            if len(true) == 0 or len(false) == 0:
                continue

            temp_gain = self.compound_entropy(question, data)
            if temp_gain > best_gain:
                best_gain = temp_gain
                best_question = question

        return best_question, best_gain

    def partition(self, split_question, rows):
        rows = pd.DataFrame(rows)

        true_df = pd.DataFrame([])
        false_df = pd.DataFrame([])

        for row in rows.iterrows():
            data = row[-1]
            if split_question.operator == '>':
                if split_question.true_or_false(data):
                    true_df.append(data)
                else:
                    false_df.append(data)
            elif split_question.operator == '==':
                if split_question.true_or_false(data):
                    true_df = true_df.append(data)
                else:
                    false_df = false_df.append(data)

        return true_df, false_df



    def build_tree(self, rows):
        temp_questions = self.questions

        question, gain = self.calc_best_info_gains(temp_questions, rows)
        if gain == 0:
            return LeafNode(rows)

        true_rows, false_rows = self.partition(question, rows)

        temp_questions = temp_questions.remove(question)

        true_branch = self.build_tree(true_rows)
        false_branch = self.build_tree(false_rows)

        return Node(question, true_branch, false_branch)

    def print_tree(self, node):
        if is_leaf_node(node):
            print("Predict", node.predictions)
            return

        print(node.question.print_str)

        print('--> True:')
        self.print_tree(node.true_branch)


        print('--> False:')
        self.print_tree(node.false_branch)

    def classify(self, row, node):
        if isinstance(node, LeafNode):
            return node.predictions

        if node.question.true_or_false(row):
            return self.classify(row, node.true_branch)
        else:
            return self.classify(row, node.false_branch)


def is_leaf_node(node):
    if isinstance(node, LeafNode):
        return True
    return False




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


def unique_questions(all_questions):
    quest_strings = []
    ret_questions = []

    for question in all_questions:
        if question.print_str not in quest_strings:
            quest_strings.append(question.print_str)
            ret_questions.append(question)

    return ret_questions

training_data = [
    ['Green', 3, 'Apple'],
    ['Yellow', 3, 'Apple'],
    ['Red', 1, 'Grape'],
    ['Red', 1, 'Grape'],
    ['Yellow', 3, 'Lemon']
]

train_df = pd.DataFrame(training_data, columns=['Color', 'Diameter', 'Fruit'])
columns = train_df.columns

all_questions = unique_questions(generate_all_questions(train_df))
d = DecisionTree(all_questions)
root_node = d.build_tree(train_df)

d.print_tree(root_node)


print("\nTESTING SET TITANIC --------------------------------------------: ")

print('Loading Titanic Dataset...')
testing_df = pd.read_csv('test.csv')
final_df = testing_df.drop(columns=['Name', 'Ticket']).fillna(0)

print("Generating Unique Questions...")
all_questions = unique_questions(generate_all_questions(final_df))
titanic_tree = DecisionTree(all_questions)
print("Building Tree (this might take a while)...")
titanic_root_node = titanic_tree.build_tree(final_df)

print("Printing Tree...")
titanic_tree.print_tree(titanic_root_node)

print("PASSENGER : SURVIVED")
for index, row in final_df.iterrows():
    classification = titanic_tree.classify(row, titanic_root_node)
    outcome = ''
    if classification[0] == 1:
        outcome = 'SURVIVED'
    else:
        outcome = 'PERISHED'

    print(str(row['PassengerId']) + ':' + outcome)
