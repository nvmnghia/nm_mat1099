import sys
import math
from argparse import ArgumentParser

from tabulate import tabulate


# 2 initial values
A_1 = 0.2
B_1 = 0.3
if A_1 >= B_1:
    print(f'A_1={A_1}, which is larger than or equal to B_1={B_1}')
    sys.exit(1)

# Upper bound for error
ERROR_BOUND = 10**(-5)
if ERROR_BOUND <= 0:
    print(f'ERROR_BOUND={ERROR_BOUND} is smaller than or equal to 0')
    sys.exit(1)

# Max number of iteration
MAX_ITER = 1000

# If absolute value of a number is smaller than ZERO_BOUND, consider it zero
# Currently not used in this script
ZERO_BOUND = 10**(-9)


def f(x: float):
    """
    Univariate function to calculate zero for.

    Parameters
    ----------
    x : float
        The number at which the value of the function is calculated.

    Returns
    -------
    float
        The value of the function at x.
    """

    return x * math.cos(x) - 2 * x**2 + 3 * x - 1


def same_sign(n1: float, n2: float) -> bool:
    """
    Check if 2 numbers have the same sign.

    Parameters
    ----------
    n1, n2 : float
        2 numbers to be checked.

    Returns
    -------
    bool
        Whether the 2 numbers have the same sign.
    """

    return (n1 > 0) == (n2 > 0)    # Dumb me didn't use ()


def bisection(return_all=False):
    """
    Approximate a zero of f using bisection method.

    Parameters
    ----------
    return_all : bool, optional
        Whether the array of A, B, P, F is returned or not, default to False.

    Returns
    -------
    p : float
        The zero found.
    T : list[list]
        List of list representing iteration data: [n, a, b, p, f].
    """

    a = A_1
    b = B_1
    f_a = f(a)
    f_b = f(b)

    if same_sign(f_a, f_b):
        if return_all:
            return None, None
        else:
            return None

    N = math.ceil(math.log((B_1 - A_1) / ERROR_BOUND, 2))
    if N > MAX_ITER:
        print(f'Number of iteration is restricted to MAX_ITER={MAX_ITER}')
        N = MAX_ITER

    if return_all:
        # Only calculate these arrays if return_all is True
        T = [[0 for i in range(5)] for j in range(N)]

    for i in range(N):
        p = (a + b) / 2
        f_p = f(p)

        if return_all:
            T[i][0] = i + 1
            T[i][1] = a
            T[i][2] = b
            T[i][3] = p
            T[i][4] = f_p

        if same_sign(f_p, f_a):
            a = p
            f_a = f_p
        else:
            b = p
            f_b = f_p

    if return_all:
        return p, T
    else:
        return p


desc = '''
    Given an function, 2 initial values, and bound of absolute error (all need to be hardcoded in this script),
    approximate a zero of the function between the 2 values using bisection method.
'''
parser = ArgumentParser(description=desc)
parser.add_argument('--latex', '-l',
    action='store_true',
    help='Print as LaTeX tabular')
args = parser.parse_args()

if args.latex:
    p, T = bisection(return_all=True)
    if p is None:
        print(f'No zero found in [a, b]=[{A_1}, {B_1}]')
        sys.exit(1)
    else:
        print(tabulate(T, tablefmt='latex'))

else:
    p = bisection()
    if p is None:
        print(f'No zero found in [a, b]=[{A_1}, {B_1}]')
        sys.exit(1)
    else:
        print(p)
