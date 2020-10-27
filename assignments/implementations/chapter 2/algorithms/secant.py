import logging
from typing import NamedTuple, List
from utils import same_sign

from function import f, DESC_F, DESC_P_0, DESC_P_1, DESC_ERROR_BOUND, DESC_MAX_ITER


METHOD_DESC = f'''
    Functions
    ---------
    {DESC_F}

    Parameters
    ----------
    {DESC_P_0}
    {DESC_P_1}
    {DESC_ERROR_BOUND}
    {DESC_MAX_ITER}
'''


class SecantIterData(NamedTuple):
    """
    NamedTuple holding iteration data of one iteration for Secant method.
    """

    # iteration number (>= 0)
    n: int
    # approximated value
    p: float
    # value of f at p
    f_p: float


def secant(P_0: float, P_1: float, ERROR_BOUND: float, MAX_ITER: int, return_all=False, **_) -> List[SecantIterData]:
    """
    Approximate a zero of f using Secant method.

    Parameters
    ----------
    P_0 : float
        The first initial approximation to start searching.
    P_1 : float
        The second initial approximation to start searching.
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
    T : List[SecantIterData]
        List of iteration data. Only returned if return_all is true, else None is returned.
    """

    logging.info('Using function f')
    logging.info(f'Initial value P_0 = {P_0}, P_1 = {P_1}')
    logging.info(f'Maximum absolute error ERROR_BOUND = {ERROR_BOUND}')
    logging.info(f'Max number of iteration MAX_ITER = {MAX_ITER}')

    # Prepare
    T = [] if return_all else None
    try:
        p_0 = P_0
        f_p_0 = f(p_0)
        if return_all:
            T.append(SecantIterData(n=0, p=p_0, f_p=f_p_0))

        p_1 = P_1
        f_p_1 = f(p_1)
        if return_all:
            T.append(SecantIterData(n=1, p=p_1, f_p=f_p_1))
    except ArithmeticError as ae:
        logging.error(f'Arithmetic error during preparation: {ae}')
        print(ae)
        return None, T

    found = False
    p = p_1    # Not needed, just a placeholder to avoid Pylance unbound warning

    # Run
    for i in range(2, MAX_ITER + 1):
        try:
            delta = f_p_1 * (p_1 - p_0) / (f_p_1 - f_p_0)
            p = p_1 - delta
            f_p = f(p)
        except ArithmeticError as ae:
            logging.error(f'Arithmetic error at iteration {i}: {ae}')
            print(ae)
            return None, T

        if return_all:
            T.append(SecantIterData(n=i, p=p, f_p=f_p))

        if abs(delta) < ERROR_BOUND:
            found = True
            break

        p_0 = p_1
        f_p_0 = f_p_1
        p_1 = p
        f_p_1 = f_p

    if not found:
        logging.warn(f'Max number of iteration MAX_ITER = {MAX_ITER} reached but no zero found')
        return None, T
    else:
        return p, T
