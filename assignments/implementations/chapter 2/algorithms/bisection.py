from math import ceil, log2
import logging
from typing import NamedTuple, List

# Parameters could be overridden in find_root.py, so they're not imported here.
from function import f, DESC_F, DESC_A_1, DESC_B_1, DESC_ERROR_BOUND, DESC_MAX_ITER


METHOD_DESC = f'''
    A bracketing root-finding method.
    The search range is halved until the zero is found.

    f must be continuous, and there exists a < b for which f(a)f(b) < 0.
    The zero lies in [a, b]. Each iteration returns the midpoint p of [a, b] as the approximation,
    and use it with a if f(a)f(p) < 0, or b otherwise, as the interval for the next iteration.

    Functions
    ---------
    {DESC_F}

    Parameters
    ----------
    {DESC_A_1}
    {DESC_B_1}
    {DESC_ERROR_BOUND}
    {DESC_MAX_ITER}
'''


class BisectionIterData(NamedTuple):
    """
    NamedTuple holding iteration data of one iteration for Bisection method.
    """

    # iteration number (>= 1)
    n: int
    # lower bound
    a: float
    # upper bound
    b: float
    # approximated value
    p: float
    # value of f at p
    f_p: float


def bisection(A_1: float, B_1: float, ERROR_BOUND: float, MAX_ITER: int, return_all=False, **kwargs) -> List[BisectionIterData]:
    """
    Approximate a zero of f using bisection method.

    Parameters
    ----------
    A_1 : float
        The lower bound of the interval to search for.
    B_1 : float
        The upper bound of the interval to search for.
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
    T : List[BisectionIterData]
        List of iteration data. Only returned if return_all is true, else None is returned.
    """

    logging.info(f'Searching interval [A_1, B_1] = [{A_1}, {B_1}]')
    logging.info(f'Maximum absolute error ERROR_BOUND = {ERROR_BOUND}')

    a = A_1
    b = B_1

    try:
        f_a = f(a)
        f_b = f(b)
    except ArithmeticError as ae:
        logging.error(f'Arithmetic error during prepare: {ae}')
        print(ae)
        return None, None

    if same_sign(f_a, f_b):
        logging.warning(f'f(A_1) = {f_a} and f(B_1) = {f_b} have the same sign')
        return None, None
    logging.info(f'f(A_1) = {f_a} and f(B_1) = {f_b} have the opposite signs')

    N = int(ceil(log2((B_1 - A_1) / ERROR_BOUND)))
    if N > MAX_ITER:
        logging.info(f'Number of iteration is restricted to MAX_ITER = {MAX_ITER} instead of {N}')
        N = MAX_ITER
    else:
        logging.info(f'Number of iteration is {N}')

    p = (a + b) / 2
    T = [None for j in range(N)] if return_all else None

    for i in range(1, N + 1):
        p = (a + b) / 2

        try:
            f_p = f(p)
        except ArithmeticError as ae:
            logging.error(f'Arithmetic error at iteration {i}: {ae}')
            print(ae)
            return None, T

        if return_all:
            T[i - 1] = BisectionIterData(n=i, a=a, b=b, p=p, f_p=f_p)

        if same_sign(f_p, f_a):
            a = p
            f_a = f_p
        else:
            b = p
            f_b = f_p

    return p, T


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
