from argparse import ArgumentParser, Action

from algorithms import METHODS


class ParseParams(Action):
    """
    Parse key=value into {'key': float(value)}.
    Used to parse override parameters.
    """
    def __call__(self, parser, namespace, values, option_string):
        params = {}
        for value in values:
            if value.count('=') != 1:
                raise ValueError(f'Input override parameter {value} is not of the form key=value')

            key, value = value.split('=')
            try:
                params[key] = float(value)
            except ValueError:
                raise ValueError(f'Input override parameter {key} has a non-float value of {value}')

        setattr(namespace, self.dest, params)

# Setup parser
PROG_DESC = '''
    Given a function (hardcoded in function.py) and initial values, bound of
    absolute error,... (stored in function.py and can be overridden),
    approximate a root of the function using the specified method.
'''
parser = ArgumentParser(description=PROG_DESC)

parser.add_argument('method',
    type=str, choices=METHODS, metavar='method',
    help='approximation method [%(choices)s]')
parser.add_argument('--override', '-o',
    nargs='+', metavar='param=value',
    action=ParseParams,
    help="override params in the format param=value, see function.py or -i for params' names to override")

parser.add_argument('--latex', '-l',
    action='store_true',
    help='print iteration data as LaTeX tabular')
parser.add_argument('-t',
    type=int, default=1, metavar='num_table',
    help='split iteration data into tables and display side by side, must be used with -l, default %(default)s table')
parser.add_argument('--decimal_places', '-d',
    type=int, choices=range(1, 18), default=5,
    metavar='decimal_places',
    help='number of decimal places when printing (not affecting accuracy), default to %(default)s')

parser.add_argument('--verbose', '-v',
    action='store_true',
    help='show log')
parser.add_argument('--info', '-i',
    action='store_true',
    help='show info and required params of the method and quit')
