import sys
from typing import Dict, Union
import logging

from parser_setup import parser
from utils import print_float, print_latex, set_decimal_places


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

set_decimal_places(args.decimal_places)

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
    print_float(p)

if args.latex:
    print_latex(T, args.t)
