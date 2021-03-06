# Find root by approximation

## Introduction

This is the implementations for root approximation algorithms for system of
linear equations taught in

- Chapter 2 of the book Numerical Analysis, 9th edition of Richard L. Burden and
  J. Douglas Faires.
- Chapter of the book Advanced Engineering Mathematics of Erwin Kreyszig

## Installation

`cd` to the [`chapter 2`](/) folder, and run the following command:

```bash
pip3 install -r requirements.txt
```

## Usage

1. Write the augmented matrix of the system in [`A.txt`](A.txt) in the default
   format of `numpy`'s [`savetxt`][1] i.e. space-separated format.
2. Run [`find_root`](find_root.py) with the name of the solving/approximation
   method.

    ```bash
    usage: find_root.py [-h] [--override param=value [param=value ...]] [--latex] [--decimal_places decimal_places] [--verbose] [--info] method

    Given an augmented matrix of a system of linear equations (stored in A.txt), initial guess, ..., solve accurately or approximate a root of the system using the specified method.

    positional arguments:
      method                approximation method [gauss_elim, gauss_jordan]

    optional arguments:
      -h, --help            show this help message and exit
      --override param=value [param=value ...], -o param=value [param=value ...]
                            override params in the format param=value, see function.py or -i for params' names to override
      --latex, -l           print iteration data as LaTeX tabular
      --decimal_places decimal_places, -d decimal_places
                            number of decimal places when printing (not affecting accuracy), default to 5
      --verbose, -v         show log
      --info, -i            show info and required params of the method and quit
    ```

## Implementation

Several points to check if a new method is implemented:

- Note: comments & code use 0-based but printing uses 1-based index.
- Unlike chapter 2, where many params are shared between methods, the methods in
  this chapter only share 1, 2 params, so a file dedicated to providing default
  params like `function.py` is not necessary.


  [1]: https://numpy.org/doc/stable/reference/generated/numpy.savetxt.html