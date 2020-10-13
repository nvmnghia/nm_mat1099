import sys
from argparse import ArgumentParser, Action
import logging

from tabulate import tabulate
tabulate.PRESERVE_WHITESPACE = True

# Parameters
from function import params


class ParseParams(Action):
    """
    Parse key=value into {'key': float(value)}.
    Used to parse override parameters.
    """
    def __call__(self, parser, namespace, values, option_string):
        params = {}
        for value in values:
            key, value = value.split('=')
            params[key] = float(value)

        setattr(namespace, self.dest, params)


# Setup parser
desc = '''
    Given an function (hardcoded in function.py) and initial values, bound of
    absolute error,... (stored in function.py and can be overridden),
    approximate a root of the function using the specified method.
'''
parser = ArgumentParser(description=desc)

parser.add_argument('method',
    choices=['bisection'],
    help='Approximation method')
parser.add_argument('--override', '-o',
    nargs='*',     # Gather all arguments for -o into a list
    action=ParseParams,
    help="Override parameters in the format param=value, see function.py for parameters' names to override")

parser.add_argument('--latex', '-l',
    action='store_true',
    help='Print as LaTeX tabular')
parser.add_argument('--verbose', '-v',
    action='store_true',
    help='Print information during iteration')

args = parser.parse_args()

# Override params
if args.override is not None:
    params.update(args.override)
params['MAX_ITER'] = int(params['MAX_ITER'])

# Validate params
assert params['A_1'] < params['B_1'], \
    f"A_1 = {params['A_1']}, which is larger than or equal to B_1 = {params['B_1']}"
assert params['ERROR_BOUND'] > 0, \
    f"ERROR_BOUND = {params['ERROR_BOUND']} is smaller than or equal to 0"
assert params['MAX_ITER'] > 0, \
    f"MAX_ITER = {params['MAX_ITER']} is smaller than or equal to 0"

# Setup logging
if args.verbose:
    logging.basicConfig(level=logging.INFO)

# Perform approximation
if args.method == 'bisection':
    from algorithms.bisection import bisection
    del params['P_0']
    p, H, T = bisection(**params, return_all=args.latex)

# Print shit
if p is None:
    print('No root found.')
elif args.latex:
    print(tabulate(T, tablefmt='latex', floatfmt='.9g'))
else:
    print(p)
