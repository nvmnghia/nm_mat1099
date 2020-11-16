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
    Given an augmented matrix of a system of linear equations (stored in A.txt),
    initial guess, ..., solve accurately or approximate a root of the system
    using the specified method.
'''
parser = ArgumentParser(description=PROG_DESC)

parser.add_argument('method',
    type=str, metavar='method', choices=METHODS,
    help='approximation method [%(choices)s]')
parser.add_argument('--override', '-o',
    nargs='+', metavar='param=value',
    action=ParseParams,
    help="override params in the format param=value, see function.py or -i for params' names to override")

parser.add_argument('--latex', '-l',
    action='store_true',
    help='print iteration data as LaTeX tabular')

parser.add_argument('--verbose', '-v',
    action='store_true',
    help='show log')
parser.add_argument('--info', '-i',
    action='store_true',
    help='show info and required params of the method and quit')
