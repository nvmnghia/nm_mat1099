import logging
from math import ceil
from typing import Callable, List, Iterable

import regex as re    # package regex, as it allows free-spacing

from tabulate import tabulate
tabulate.PRESERVE_WHITESPACE = True


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


config = {
    'decimal_places': None
}

def set_decimal_places(n: int):
    """
    Set number of decimal place in printing.
    Parameters
    ----------
    n : int
        Number of decimal places.
    """

    logging.info(f'Printing with {n} decimal places')
    config['decimal_places'] = n


def print_latex(T: list, num_table: int) -> None:
    """
    Print iteration data as LaTeX tabular.

    Parameters
    ----------
    T : list
        List of iteration data.
    num_table : int
        Split iteration data into columns to display side by side.
    """

    if num_table != 1:
        if num_table <= 0:
            logging.warning(f'Non-positive number of side by side tables {num_table}, now print normally')
        elif num_table > len(T):
            logging.warning(f'Number of side by side tables {num_table} exceeds number of data rows {len(T)}, now print normally')
        else:
            num_row = len(T)
            num_col = len(T[0])
            row_per_side_table = int(ceil(num_row / num_table))
            table = T

            T = (
                (
                    table[i + j * row_per_side_table][k]
                    for i in [i]    # I lol'd so hardddddd
                        for j in range(num_table)
                            for k in range(num_col)
                                if i + j * row_per_side_table < num_row
                )
                for i in range(row_per_side_table)
            )

    latex = str(tabulate(T, tablefmt='latex', floatfmt=f".{config['decimal_places']}f"))

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

    print(latex)


def print_float(f: float) -> str:
    """
    Format multiplier for Gauss Elimination and related methods

    Parameters
    ----------
    s : float
        The number to be formatted:
        - strip trailing zero: 1.0 to '1'

    Returns
    -------
    str
        The formated number in string
    """

    s = f"%.{config['decimal_places']}f" % f

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
    s = re.sub(trailing_zero_matcher, '', s)

    # Remove trailing decimal dot
    s = re.sub(r'\.(?=\s)', '', s)

    return s
