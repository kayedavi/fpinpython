# Functions get passed around so often in FP that it's
# convenient to have syntax for constructing a function
# *without* having to give it a name
from chapter02.my_module import absolute_value, factorial, format_result

if __name__ == '__main__':
    print(format_result('absolute value', -42, absolute_value))
    print(format_result('factorial', 7, factorial))
    print(format_result('increment', 7, lambda x: x + 1))
