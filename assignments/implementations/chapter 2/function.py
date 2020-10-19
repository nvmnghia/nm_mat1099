import math


"""
Add the function to find root for, and parameters of the root-finding method here.
"""


params = {
    # 2 initial values...
    'A_1': math.pi / 2,
    'B_1': math.pi,

    # or 1, depends on the method
    'P_0': 0,

    # Upper bound for absolute error
    'ERROR_BOUND': 10**(-5),

    # Max number of iteration
    'MAX_ITER': 1000,
}


def f(x: float) -> float:
    """
    Univariate function to find root for.

    Parameters
    ----------
    x : float
        The number at which the value of the function is calculated.

    Returns
    -------
    float
        The value of the function at x.
    """

    return x - 2 * math.sin(x)


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

    return x


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
        The initial approximation to start searching.
'''

DESC_ERROR_BOUND = '''
    ERROR_BOUND : float
        The upper bound for absolute error.
'''

DESC_MAX_ITER = '''
    MAX_ITER : int
        Maximum number of iteration allowed.
'''

DESC_DERIVATIVE = '''
    The derivative of the function must be known (implemented in function.py).
'''
