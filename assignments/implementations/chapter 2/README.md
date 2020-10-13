# Find root by approximation

## Introduction

This is the implementations for root approximation algorithms taught in Chapter
2 of the book Numerical Analysis, 9th edition of Richard L. Burden and J.
Douglas Faires.

## Installation

`cd` to the [`chapter 2`](/) folder, and run the following command:

```bash
pip3 install -r requirements.txt
```

## Usage

1. Implement the function and parameters of the root-finding process in
   [`function.py`](function.py).
2. Run [`find_root.py`](find_root.py) with the name of the approximation method.

   ```bash
   $ python3 find_root.py -h

   usage: find_root.py [-h] [--override [OVERRIDE [OVERRIDE ...]]] [--latex] [--verbose] {bisection}

   Given an function (hardcoded in function.py) and initial values, bound of absolute error,... (stored in function.py and can be overridden), approximate a root of the function using the specified method.

   positional arguments:
     {bisection}           Approximation method

   optional arguments:
     -h, --help            show this help message and exit
     --override [OVERRIDE [OVERRIDE ...]], -o [OVERRIDE [OVERRIDE ...]]
                           Override parameters in the format param=value, see function.py for parameters' names to override
     --latex, -l           Print as LaTeX tabular
     --verbose, -v         Print information during iteration
   ```

A common example command to get pretty printed LaTeX table is:

```bash
python3 find_root.py bisection -l -v
```
