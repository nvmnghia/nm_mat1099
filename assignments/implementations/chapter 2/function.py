import math


"""
Add the function to find root for, and parameters of the root-finding process here.
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


def f(x: float):
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
