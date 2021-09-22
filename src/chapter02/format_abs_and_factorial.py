# Now we can use our general `formatResult` function
# with both `abs` and `factorial`
from chapter02.my_module import absolute_value, format_result, factorial

if __name__ == '__main__':
    print(format_result('absolute value', -42, absolute_value))
    print(format_result('factorial', 7, factorial))
