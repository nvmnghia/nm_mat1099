import sys
import math
import logging

# Parameters could be overridden in find_root.py, so they're not imported here.
from function import f


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


def bisection(A_1:float, B_1: float, ERROR_BOUND: float, MAX_ITER: int, return_all=False):
    """
    Approximate a zero of f using bisection method.

    Parameters
    ----------
    A_1 : float
        The lower bound of the range to search for.
    B_1 : float
        The upper bound of the range to search for.
    ERROR_BOUND : float
        The upper bound for absolute error.
    MAX_ITER : int
        Maximum number of iteration allowed.
    return_all : bool, optional
        Whether the iteration data T is returned or not, default to False.

    Returns
    -------
    p : float
        The zero found.
    H : list[str]
        List of header string for printing iteration data. Only returned if return_all is true, else None is returned.
    T : list[list]
        2D list representing iteration data: [n, a, b, p, f]. Only returned if return_all is true, else None is returned.
    """

    logging.info(f'Searching range is [A_1, B_1] = [{A_1}, {B_1}], maximum absolute error is {ERROR_BOUND}')

    a = A_1
    b = B_1
    f_a = f(a)
    f_b = f(b)

    if same_sign(f_a, f_b):
        logging.warning(f'f(A_1) = {f_a} and f(B_1) = {f_b} have the same sign')
        return None, None, None
    logging.info(f'f(A_1) = {f_a} and f(B_1) = {f_b} have the opposite signs')

    N = int(math.ceil(math.log((B_1 - A_1) / ERROR_BOUND, 2)))
    if N > MAX_ITER:
        logging.info(f'Number of iteration is restricted to MAX_ITER = {MAX_ITER} instead of {N}')
        N = MAX_ITER
    logging.info(f'Number of iteration is {N}')

    if return_all:
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
        # Spaces are intentional. If this header is to be used,
        # set tabulate.PRESERVE_WHITESPACE and use latex_raw table format.
        # H = ['\(n\)  ', '{\(a_n\)}  ', '{\(b_n\)}  ', '{\(p_n\)}  ', '{\(f(p_n)\)}  ']
        H = None
        return p, H, T
    else:
        return p, None, None
