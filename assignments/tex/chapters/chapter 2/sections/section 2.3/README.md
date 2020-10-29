# Calculation tips

Calculation is performed on a fx-570ES PLUS.

## Newton method

## Secant method

> 1. Prepare
>    1. Assign $p_0$ to $\textbf{X}$
>    2. Calculate $f(p_0)$ by $\textbf{X}$ *AND* assign it to $\textbf{A}$
>    3. Assign $\textbf{X}$ to $\textbf{Y}$
>    4. Assign $p_1$ to $\textbf{X}$
>    5. Calculate $f(p_1)$ by $\textbf{X}$ *AND* assign it to $\textbf{A}$
>
> 2. Repeat
>    1. Assign $\textbf{A} * (\textbf{X} - \textbf{Y}) / (\textbf{A} - f(\textbf{Y}))$ to $\textbf{D}$
>    2. Assign $\textbf{X}$ to $\textbf{Y}$
>    3. Calculate $p$ by $\textbf{X} - \textbf{D}$ *AND* assign it to $\textbf{X}$
>    4. Calculate $f(p)$ by $\textbf{X}$
>    5. If $abs(D) - error$ negative, quit.

## Method of False Position

The same as Secant method, just some difference in assigning $\textbf{Y}$ in the `Repeat` part.

> 1. Prepare
>    1. Assign $p_0$ to $\textbf{X}$
>    2. Calculate $f(p_0)$ by $\textbf{X}$ *AND* assign it to $\textbf{A}$
>    3. Assign $\textbf{X}$ to $\textbf{Y}$
>    4. Assign $p_1$ to $\textbf{X}$
>    5. Calculate $f(p_1)$ by $\textbf{X}$ *AND* assign it to $\textbf{A}$
>
> 2. Repeat
>    1. Assign $\textbf{A} * (\textbf{X} - \textbf{Y}) / (\textbf{A} - f(\textbf{Y}))$ to $\textbf{D}$
>    2. Assign $\textbf{X}$ to $\textbf{C}$
>    3. Calculate $p$ by $\textbf{X} - \textbf{D}$ *AND* assign it to $\textbf{X}$
>    4. Calculate $f(p)$ by $\textbf{X}$
>    5. If $f(p)$ and $f(p_1)$ have different signs, assign $\textbf{C}$ to $\textbf{Y}$
>    6. If $abs(D) - error$ negative, quit.
