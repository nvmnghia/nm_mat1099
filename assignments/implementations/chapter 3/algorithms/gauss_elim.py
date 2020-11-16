import logging

import numpy as np

from utils import is_valid_augmented, mat2str


METHOD_DESC = '''
    A direct, accurate solving method.

    The augmented matrix is transformed to a lower triangular matrix,
    by eliminating unknowns x_i in ith equation.

    Parameters
    ----------
    A : np.ndarray
        The augmented matrix of the system of equation.
    swap_row : bool
        Enable row swapping. Default True.
'''


def gauss_elim(A: np.ndarray, swap_row=True, print_latex=True, **_) -> np.ndarray:
    """
    Solve the system using Gauss elimination method, with row swapping.

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
        The unique solution of the system.
    """

    if not is_valid_augmented(A):
        logging.error(f'Invalid augmented matrix size: {A.shape} instead of (n, n+1)')
        return None
    logging.info(f'Matrix A is a valid augmented matrix:\n{mat2str(A, print_latex)}')
    logging.info(f"Row swapping {'enabled' if swap_row else 'disabled'}")

    # Note: Comments & printing use 1-based index
    # but the implementation uses 0-based

    # Elimination
    N = len(A)
    for i in range(N - 1):
        # Eliminate x_i (pivot)
        a_i = A[i][i]

        # Swap if needed
        if a_i == 0:
            if swap_row:
                # Find the equation with the first non-zero parameter of x_i
                index_of_first_nonzero = next((_i for _i in range(i, N) if A[_i][i] != 0), None)
                if index_of_first_nonzero is None:
                    logging.error(f'System has no unique solution (either no solution or infinite number of solutions)')
                    return None

                # Swap the found equation with the current one
                A[[i, index_of_first_nonzero]] = A[[index_of_first_nonzero, i]]
                a_i = A[i][i]

                logging.info(f'Swapped row {i + 1} with {index_of_first_nonzero + 1}')
            else:
                logging.error(f'Cannot solve without swapping rows')
                return None

        # Eliminate x_i from E_{i+1} onwards
        for _i in range(i + 1, N):
            if A[_i][i] == 0:
                continue

            m = A[_i][i] / a_i
            A[_i] = A[_i] - m * A[i]

            logging.info(f"E_{_i + 1} := E_{_i + 1} - {f'{m}' if m >= 0 else f'({m})'} E_{i + 1}")

        logging.info(f'Eliminated x_{i + 1}, A becomes:\n{mat2str(A, print_latex)}')

    # Back substitution
    P = A[:, :N]    # Parameter matrix
    b = A[:, N]
    x = np.zeros((N, 1))
    for i in range(N - 1, -1, -1):
        if P[i][i] == 0:
            logging.error(f'Parameter A[{i}][{i}] = 0, system has no unique solution (either no solution or infinite number of solutions)')
            return None
        x[i] = (b[i] - np.dot(P[i], x)) / P[i][i]

    return x
