from numbers import Number


class Question:
    def __init__(self, column, value, operator):
        self.column = column
        self.value = value
        self.operator = operator
        self.print_str = 'Is ' + str(self.column) + ' ' + self.operator + ' ' + str(self.value)

    def true_or_false(self, data):
        col_val = data[self.column]
       # print(str(type(col_val)) + ' ' + str(col_val) + " : " + str(type(self.value)) + str(self.value))
        if is_numeric(col_val) and is_numeric(self.value):
            return col_val > self.value
        else:
            return col_val == self.value




def is_numeric(value):
    return isinstance(value, Number)
