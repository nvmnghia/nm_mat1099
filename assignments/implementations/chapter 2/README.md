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
    usage: find_root.py [-h] [--override param=value [param=value ...]] [--latex] [-t num_table] [--verbose] [--info] method

    Given a function (hardcoded in function.py) and initial values, bound of absolute error,... (stored in function.py and can be overridden), approximate a root of the function using the specified method.

    positional arguments:
    method                approximation method

    optional arguments:
    -h, --help            show this help message and exit
    --override param=value [param=value ...], -o param=value [param=value ...]
                            override params in the format param=value, see function.py or -i for params' names to override
    --latex, -l           print iteration data as LaTeX tabular
    -t num_table          split iteration data into tables and display side by side, must be used with -l, default 1 table
    --verbose, -v         show log
    --info, -i            show info and required params of the method and quit
    ```

A common example command to get pretty printed LaTeX table is:

```bash
python3 find_root.py bisection -l -v
```
