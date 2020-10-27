import sys
from argparse import ArgumentParser, Action
from typing import Dict, Union
import logging
from math import ceil

import regex as re

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
            except ValueError:
                raise ValueError(f'Input override parameter {key} has a non-float value of {value}')

        setattr(namespace, self.dest, params)


def merge_params(override: Dict[str, float]) -> Dict[str, Union[float, int]]:
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
        params = {**params, **override}
    params['MAX_ITER'] = int(params['MAX_ITER'])

    # Validate method params
    assert params['A_1'] < params['B_1'], \
        f"A_1 = {params['A_1']}, which is larger than or equal to B_1 = {params['B_1']}"
    assert params['ERROR_BOUND'] > 0, \
        f"ERROR_BOUND = {params['ERROR_BOUND']} is smaller than or equal to 0"
    assert params['MAX_ITER'] > 0, \
        f"MAX_ITER = {params['MAX_ITER']} is smaller than or equal to 0"

    return params


def print_latex(T: list, num_table: int) -> None:
    """
    Print iteration data as LaTeX tabular.

    Parameters
    ----------
    T : list
        List of iteration data.
    num_table : int
        Split iteration data into columns to display side by side.
    """

    if num_table != 1:
        if num_table <= 0:
            logging.warning(f'Non-positive number of side by side tables {num_table}, now print normally')
        elif num_table > len(T):
            logging.warning(f'Number of side by side tables {num_table} exceeds number of data rows {len(T)}, now print normally')
        else:
            num_row = len(T)
            num_col = len(T[0])
            row_per_side_table = int(ceil(num_row / num_table))
            table = T

            T = (
                (
                    table[i + j * row_per_side_table][k]
                    for i in [i]    # I lol'd so hardddddd
                        for j in range(num_table)
                            for k in range(num_col)
                                if i + j * row_per_side_table < num_row
                )
                for i in range(row_per_side_table)
            )

    latex = str(tabulate(T, tablefmt='latex', floatfmt='.13f'))

    # Remove trailing zeros
    trailing_zero_matcher = re.compile(
        r'''
            (?<=         # Positive (=) look behind (<), i.e. must be (positive) preceded by (look behind)
                \.\d*    # Decimal dot, followed by zero or more digit
            )
            0            # Match a SINGLE trailing zero
            (?=          # Positive (=) look ahead (no <), i.e. must be (positive) succeeded by (look ahead)
                0*\b     # Zero or more 0, followed by word boundary \b
            )
        ''',
        re.VERBOSE    # Allow free-spacing and comment
    )
    latex = re.sub(trailing_zero_matcher, ' ', latex)

    # Remove trailing decimal dot
    latex = re.sub(r'\.(?=\s)', ' ', latex)

    # Remove redundant minus sign
    latex = re.sub(r'-(?=0\s)', ' ', latex)

    # Add spacing between columns and newline
    latex = re.sub('&', ' & ', latex)
    latex = re.sub(r'\\\\', r' \\\\', latex)

    print(latex)


METHODS = ['bisection', 'fixed_point', 'newton', 'secant', 'false_position']

# Setup parser
PROG_DESC = '''
    Given a function (hardcoded in function.py) and initial values, bound of
    absolute error,... (stored in function.py and can be overridden),
    approximate a root of the function using the specified method.
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
parser.add_argument('-t',
    type=int, default=1, metavar='num_table',
    help='split iteration data into tables and display side by side, must be used with -l, default %(default)s table')

parser.add_argument('--verbose', '-v',
    action='store_true',
    help='show log')
parser.add_argument('--info', '-i',
    action='store_true',
    help='show info and required params of the method and quit')

args = parser.parse_args()

# Print info and quit
method = args.method
if args.info:
    if method == 'bisection':
        from algorithms.bisection import METHOD_DESC
    elif method == 'fixed_point':
        from algorithms.fixed_point import METHOD_DESC
    elif method == 'newton':
        from algorithms.newton import METHOD_DESC
    elif method == 'secant':
        from algorithms.secant import METHOD_DESC
    elif method == 'false_position':
        from algorithms.false_position import METHOD_DESC
    else:
        raise ValueError(f'Invalid method {method}')

    print(METHOD_DESC)
    sys.exit()

# Setup logging
if args.verbose:
    logging.basicConfig(level=logging.INFO)

# Perform approximation
params = merge_params(args.override)
if method == 'bisection':
    from algorithms.bisection import bisection as method
elif method == 'fixed_point':
    from algorithms.fixed_point import fixed_point as method
elif method == 'newton':
    from algorithms.newton import newton as method
elif method == 'secant':
    from algorithms.secant import secant as method
elif method == 'false_position':
    from algorithms.false_position import false_position as method
else:
    raise ValueError(f'Invalid method {method}')
p, T = method(**params, return_all=args.latex)

# Print shit
if p is None:
    print('Not found')
else:
    print(p)

if args.latex:
    print_latex(T, args.t)
