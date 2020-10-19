import sys
from argparse import ArgumentParser, Action
import logging

from tabulate import tabulate
tabulate.PRESERVE_WHITESPACE = True


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
            except :
                raise ValueError(f'Input override parameter {key} has a non-float value of {value}')

        setattr(namespace, self.dest, params)


def merge_params(override: dict):
    """
    Merge and validate method params.

    Parameters
    ----------
    override : dict
        Dictionary of parameter-value to override params from function.py.

    Returns
    -------
    dict
        Dictionary of method parameters, merged and validated.
    """

    from function import params

    # Override method params
    if override is not None:
        params.update(override)
    params['MAX_ITER'] = int(params['MAX_ITER'])

    # Validate method params
    assert params['A_1'] < params['B_1'], \
        f"A_1 = {params['A_1']}, which is larger than or equal to B_1 = {params['B_1']}"
    assert params['ERROR_BOUND'] > 0, \
        f"ERROR_BOUND = {params['ERROR_BOUND']} is smaller than or equal to 0"
    assert params['MAX_ITER'] > 0, \
        f"MAX_ITER = {params['MAX_ITER']} is smaller than or equal to 0"

    return params


METHODS = ['bisection']

# Setup parser
PROG_DESC = '''
    Given an function (hardcoded in function.py) and initial values, bound of
    absolute error,... (stored in function.py and can be overridden),
    approximate a root of the function using the specified method.
'''
parser = ArgumentParser(description=PROG_DESC)

parser.add_argument('method',
    type=str, metavar='method', choices=METHODS,
    help='approximation method')
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

args = parser.parse_args()

# Print info and quit
if args.info:
    if args.method == 'bisection':
        from algorithms.bisection import METHOD_DESC

    print(METHOD_DESC)
    sys.exit()

# Setup logging
if args.verbose:
    logging.basicConfig(level=logging.INFO)

# Perform approximation
params = merge_params(args.override)
if args.method == 'bisection':
    from algorithms.bisection import bisection
    p, T = bisection(params['A_1'], params['B_1'], params['ERROR_BOUND'], params['MAX_ITER'], return_all=args.latex)

# Print shit
if p is None:
    print('No root found.')
elif args.latex:
    print(tabulate(T, tablefmt='latex', floatfmt='.9g'))
else:
    print(p)
