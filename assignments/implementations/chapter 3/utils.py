from typing import Callable, List
from collections.abc import Iterable

import numpy as np
from tabulate import tabulate
import regex as re


def is_valid_augmented(A: np.ndarray) -> bool:
    """
    Check if the given matrix is an augmented matrix
    of a solvable system of equation.
    A valid one should be of the size n x (n + 1).

    Parameters
    ----------
    A : np.ndarray
        The matrix to be checked.

    Returns
    -------
    bool
        Whether A is a valid augmented matrix or not.
    """

    return len(A) + 1 == len(A[0])


mat2str: Callable[[np.ndarray, bool], str] = lambda M, latex: \
    to_latex(M) if latex else str(M)


def to_latex(M: np.ndarray) -> str:
    """
    Convert matrix to LaTeX representation.

    Parameters
    ----------
    m : np.ndarray
        The matrix to be printed.

    Returns
    -------
    str
        The string represent the matrix in LaTeX.
    """

    latex = str(tabulate(M, tablefmt='latex', floatfmt='.5f'))

    # Filter content line only (avoid tabular,...)
    latex = '\n'.join(
        filter(
            lambda line: line.endswith('\\'),
            latex.splitlines()
        )
    )

    # Remove trailing zeros
    trailing_zero_matcher = re.compile(
        r'''
            (?<=         # Positive (=) look behind (<), i.e. must be (positive) preceded by (look behind)
                \.\d*    # Decimal dot, followed by zero or more digit
            )
            0            # Match a SINGLE trailing zero
            (?=          # Positive (=) look ahead (no <), i.e. must be (positive) succeeded by (look ahead)
                0*\b     # Zero or more 0, followed by word boundary \b
            )
        ''',
        re.VERBOSE    # Allow free-spacing and comment
    )
    latex = re.sub(trailing_zero_matcher, ' ', latex)

    # Remove trailing decimal dot
    latex = re.sub(r'\.(?=\s)', ' ', latex)

    # Remove redundant minus sign
    latex = re.sub(r'-(?=0\s)', ' ', latex)

    # Add spacing between columns and newline
    latex = re.sub('&', ' & ', latex)
    latex = re.sub(r'\\\\', r' \\\\', latex)

    # Remove excessive whitespaces
    # e.g. from
    # 8     \\
    # 9.2   \\
    # to
    # 8    \\
    # 9.2  \\

    # Split row into cells
    split_cells: Callable[[str], List[str]] = lambda row: \
        row[: len(row) - 2].split('&')

    # Merge cells into row
    merge_cells: Callable[[Iterable[str]], str] = lambda cells: \
        '&'.join(cells) + r'\\'

    # Split data into columns
    split_columns: Callable[[str], Iterable[str]] = lambda latex: \
        zip(*map(split_cells, latex.splitlines()))

    # Merge rows into string, reversing split_columns
    merge_columns: Callable[[Iterable[str]], str] = lambda columns: \
        '\n'.join(map(merge_cells, zip(*columns)))

    # Find the number of trailing spaces
    num_of_trailing_spaces: Callable[[str], int] = lambda cell: \
        len(cell) - len(cell.rstrip())

    # Find the number of excess spaces in each row
    find_excess_spaces: Callable[[Iterable[str]], int] = lambda column: \
        min((num_of_trailing_spaces(cell) for cell in column)) - 2    # Mandatory 2 trailing spaces

    def strip_excess_spaces(column):
        num_of_excess_spaces = find_excess_spaces(column)
        return map(lambda cell: cell[: len(cell) - num_of_excess_spaces], column)

    latex = merge_columns(map(strip_excess_spaces, split_columns(latex)))

    return(latex)
