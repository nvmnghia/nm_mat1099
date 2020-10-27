import math


"""
Add the function to find root for, and parameters of the root-finding method here.
"""


params = {
    # Search range
    'A_1': 0,
    'B_1': 1,

    # 1 initial value,...
    'P_0': 0.0067,

    # or 2, depends on the method
    'P_1': 1,

    # Upper bound for absolute error
    'ERROR_BOUND': 10**(-6),

    # Max number of iteration
    'MAX_ITER': 1000,
}


def f(x: float) -> float:
    """
    Univariate function to find zero for.

    Parameters
    ----------
    x : float
        The number at which the value of the function is calculated.

    Returns
    -------
    float
        The value of the function at x.
    """

    return 1 - (1 + x)**(-360) - 135 * x


def df(x: float) -> float:
    """
    Derivative of f.

    Parameters
    ----------
    x : float
        The number at which the derivative of the function is calculated.

    Returns
    -------
    float
        The derivative of the function at x.
    """

    return 360 * (1 + x)**(-361) - 135


def g(p: float) -> float:
    """
    Fixed-point sequence generator.

    Parameters
    ----------
    p : float
        The number at which the value of the function is calculated.

    Returns
    -------
    float
        The value of the function at x.
    """

    return 300 - 80.425 * p - 201.0625 * (1 - math.e**(-0.4 * p))


DESC_A_1 = '''
    A_1 : float
        The lower bound of the interval to search for.
'''

DESC_B_1 = '''
    B_1 : float
        The upper bound of the interval to search for.
'''

DESC_P_0 = '''
    P_0 : float
        The (first) initial approximation to start searching.
'''

DESC_P_1 = '''
    P_1 : float
        The second initial approximation to start searching.
'''

DESC_ERROR_BOUND = '''
    ERROR_BOUND : float
        The upper bound for absolute error.
'''

DESC_MAX_ITER = '''
    MAX_ITER : int
        Maximum number of iteration allowed.
'''

DESC_F = '''
    f
        Univariate function to find zero for.
'''

DESC_DF = '''
    df
        Derivative of f.
'''

DESC_G = '''
    g
        Univariate function to find fixed point for (not f).
'''
