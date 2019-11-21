class Node:
    def __init__(self, question, true_branch, false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch

class LeafNode:
    def __init__(self, rows):
        self.predictions = rows.iloc[:,-1].value_counts()



