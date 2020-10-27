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
