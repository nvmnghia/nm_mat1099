from algorithms.gauss_elim import METHOD_DESC
import logging

import numpy as np

from utils import format_multiplier, is_valid_augmented, mat2str


METHOD_DESC = '''
    A direct, accurate solving method.

    The augmented matrix is transformed to a diagonal matrix,
    by eliminating unknown x_i in all equation but the ith one.
    Equivalent to Gauss Elimination gauss_elim.

    Parameters
    ----------
    A : np.ndarray
        The augmented matrix of the system of equation.
    swap_row : bool
        Enable row swapping. Default True.
'''


def gauss_jordan(A: np.ndarray, swap_row=True, print_latex=True, **_) -> np.ndarray:
    """
    Solve the system using Gauss-Jordan method, with row swapping by default.

    Parameters
    ----------
    A : np.ndarray
        The augmented matrix of the system of equation.
    swap_row : bool
        Enable row swapping. Default True.
    print_latex : bool, optional
        When printing matrix, print it in LaTeX.

    Returns
    -------
    x : np.ndarray
        The unique solution of the system, in column vector form.
    """

    if not is_valid_augmented(A):
        logging.error(f'Invalid augmented matrix size: {A.shape} instead of (n, n+1)')
        return None
    logging.info(f'Matrix A is a valid augmented matrix:\n{mat2str(A, print_latex)}')
    logging.info(f"Row swapping {'enabled' if swap_row else 'disabled'}")

    # Note: comments & code use 0-based
    # but printing uses 1-based index

    # Elimination
    N = len(A)
    for i in range(N):
        # Eliminate x_i
        a_i = A[i][i]

        # Swap if needed
        if a_i == 0:
            if swap_row:
                # Find the equation with the first non-zero parameter of x_i
                index_of_first_nonzero = next(
                    (_i for _i in range(i + 1, N) if A[_i][i] != 0),
                    None)
                if index_of_first_nonzero is None:
                    logging.error(f'No nonzero A[{i + 1}][>={i + 1}] found. System has no unique solution (either no solution or infinite number of solutions)')
                    return None

                # Swap the found equation with the current one
                A[[i, index_of_first_nonzero]] = A[[index_of_first_nonzero, i]]
                a_i = A[i][i]

                logging.info(f'Swapped row {i + 1} with {index_of_first_nonzero + 1}')
            else:
                logging.error(f'Cannot solve without swapping rows')
                return None

        # Eliminate x_i from all equation but E_i
        for _i in range(N):
            if _i == i or A[_i][i] == 0:
                continue

            m = A[_i][i] / a_i
            A[_i] = A[_i] - m * A[i]

            logging.info(f"E_{_i + 1} := E_{_i + 1} - {format_multiplier(m)} E_{i + 1}")

        logging.info(f'Eliminated x_{i + 1}, A becomes:\n{mat2str(A, print_latex)}')

    # Solve x
    d = np.diag(A)
    b = A[:, N]
    try:
        x = np.divide(b, d)
    except FloatingPointError:
        logging.error(f'Floating point error, possibly divide by zero. System has no unique solution (either no solution or infinite number of solutions).')
        return None

    return x.reshape(-1, 1)
