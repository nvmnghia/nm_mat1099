import logging
from logging import exception
from typing import NamedTuple, List

from function import f, df, DESC_F, DESC_DF, DESC_P_0, DESC_ERROR_BOUND, DESC_MAX_ITER


METHOD_DESC = f'''
    A derivative-based root-finding method, fast but may diverge.
    A good initial approximation p_0 is needed. p = p_0 - f(p_0) / df(p_0) is an approximation
    and used as p_0 of the next iteration.

    Functions
    ---------
    {DESC_F}
    {DESC_DF}

    Parameters
    ----------
    {DESC_P_0}
    {DESC_ERROR_BOUND}
    {DESC_MAX_ITER}
'''


class NewtonIterData(NamedTuple):
    """
    NamedTuple holding data of one iteration for Newton method.
    """

    # iteration number (>= 1)
    n: int
    # approximated value
    p: float
    # value of f at p
    f_p: float
    # derivative of f at p
    df_p: float


def newton(P_0: float,  ERROR_BOUND: float, MAX_ITER: int, return_all=False, **_) -> List[NewtonIterData]:
    """
    Approximate a zero of f using Newton's method.

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
        The zero found.
    T : List[FixedPointIterData]
        List of iteration data. Only returned if return_all is true, else None is returned.
    """

    logging.info('Using function f, df')
    logging.info(f'Initial value P_0 = {P_0}')
    logging.info(f'Maximum absolute error ERROR_BOUND = {ERROR_BOUND}')
    logging.info(f'Max number of iteration MAX_ITER = {MAX_ITER}')

    # Prepare

    T = [] if return_all else None
    try:
        p_0 = P_0
        f_p = f(p_0)
        df_p = df(p_0)
        if return_all:
            T.append(NewtonIterData(n=0, p=p_0, f_p=f_p, df_p=df_p))
    except ArithmeticError as ae:
        logging.error(f'Arithmetic error during preparation: {ae}')
        print(ae)
        return None, T

    p = p_0
    found = False

    # Run
    for i in range(1, MAX_ITER + 1):
        try:
            delta = f_p / df_p
            p = p - delta
            f_p = f(p)
            df_p = df(p)
        except ArithmeticError as ae:
            logging.error(f'Arithmetic error at iteration {i}: {ae}')
            print(ae)
            return None, T

        if return_all:
            T.append(NewtonIterData(n=i, p=p, f_p=f_p, df_p=df_p))

        if abs(delta) < ERROR_BOUND:
            found = True
            break
        p_0 = p

    if not found:
        logging.warn(f'Max number of iteration MAX_ITER = {MAX_ITER} reached but no zero found')
        return None, T
    else:
        return p, T
