import sys
import logging

import numpy as np
np.seterr(all='raise')

from parser_setup import parser
from utils import mat2str, set_decimal_places


args = parser.parse_args()
method = args.method

# Print info and quit
if args.info:
    if method == 'gauss_elim':
        from algorithms.gauss_elim import METHOD_DESC
    elif method == 'gauss_jordan':
        from algorithms.gauss_jordan import METHOD_DESC
    else:
        raise ValueError(f'Invalid method {method}')
    print(METHOD_DESC)
    sys.exit()

# Setup logging
if args.verbose:
    logging.basicConfig(level=logging.INFO)

set_decimal_places(args.decimal_places)

# Perform solving/approximation
A = np.loadtxt('A.txt')
if method == 'gauss_elim':
    from algorithms.gauss_elim import gauss_elim as fmethod
elif method == 'gauss_jordan':
    from algorithms.gauss_jordan import gauss_jordan as fmethod
else:
    raise ValueError(f'Invalid method {method}')
x = fmethod(A, print_latex=args.latex, **(args.override if args.override else {}))
print(mat2str(x, args.latex))
