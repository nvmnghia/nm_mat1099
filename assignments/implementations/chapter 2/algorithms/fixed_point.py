import logging
from typing import NamedTuple, List

from function import g, DESC_G, DESC_P_0, DESC_ERROR_BOUND, DESC_MAX_ITER


METHOD_DESC = f'''
    A fixed-point-finding method, not a root-finding one.
    g is applied on the initial value, and its output is used as input in the next iteration.

    Some basic sufficient conditions for convergence:
    - g is continuous on [a, b], g(x) is in between g(a), g(b) for all x in [a, b]:  p exists on [a, b]
    - In addition, g is differentiable on (a, b), |g(x)| < 1 for all x in [a, b]:    p is unique on [a, b]

    Note that g is used, not f, as the algorithm cannot automagically find zero of f by finding fixed point of g.

    Functions
    ---------
    {DESC_G}

    Parameters
    ----------
    {DESC_P_0}
    {DESC_ERROR_BOUND}
    {DESC_MAX_ITER}
'''


class FixedPointIterData(NamedTuple):
    """
    NamedTuple holding data of one iteration for fixed-point method.
    """

    # iteration number (>= 0)
    n: int
    # approximated value
    p: float


def fixed_point(P_0: float,  ERROR_BOUND: float, MAX_ITER: int, return_all=False, **_) -> List[FixedPointIterData]:
    """
    Approximate a fixed point of g using fixed-point method.

    Parameters
    ----------
    P_0 : float
        The initial approximation to start searching.
    ERROR_BOUND : float
        The upper bound for absolute error.
    MAX_ITER : int
        Maximum number of iteration allowed.
    return_all : bool, optional
        Whether the iteration data T is returned or not, default to False.

    Returns
    -------
    p : float
        The fixed point found.
    T : List[FixedPointIterData]
        List of iteration data. Only returned if return_all is true, else None is returned.
    """

    logging.info('Using function g')
    logging.info(f'Initial value P_0 = {P_0}')
    logging.info(f'Maximum absolute error ERROR_BOUND = {ERROR_BOUND}')
    logging.info(f'Max number of iteration MAX_ITER = {MAX_ITER}')

    # Prepare
    p_0 = P_0
    p = p_0

    T = [FixedPointIterData(n=0, p=p)] if return_all else None

    found = False

    # Run
    for i in range(1, MAX_ITER + 1):
        try:
            p = g(p_0)
        except ArithmeticError as ae:
            logging.error(f'Arithmetic error at iteration {i}: {ae}')
            print(ae)
            return None, T

        if return_all:
            T.append(FixedPointIterData(n=i, p=p))

        if abs(p - p_0) < ERROR_BOUND:
            found = True
            break
        p_0 = p

    if not found:
        logging.warn(f'Max number of iteration MAX_ITER = {MAX_ITER} reached but no fixed point found')
        return None, T
    else:
        return p, T
