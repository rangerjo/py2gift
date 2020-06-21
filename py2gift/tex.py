# AUTOGENERATED! DO NOT EDIT! File to edit: 01_tex.ipynb (unless otherwise specified).

__all__ = ['to_formula_maybe', 'join', 'gaussian_pdf', 'q_function_approximation', 'partwise_function', 'from_number',
           'from_matrix', 'dot_product', 'total_probability', 'enumerate_math', 'enumerate_assignments', 'expand']

# Cell
import functools
from typing import Union, Iterable, List, Optional, Tuple

import numpy as np

# Cell

def to_formula_maybe(func):

    def wrapper(*args, **kwargs):

        if ('to_formula' in kwargs) and (kwargs['to_formula']):

            kwargs.pop('to_formula')

            return f'${func(*args, **kwargs)}$'

        else:

            if ('to_formula' in kwargs):

                # it must also be popped out
                kwargs.pop('to_formula')

            return func(*args, **kwargs)

    functools.update_wrapper(wrapper, func)

    return wrapper

# Cell
def join(strings_list: List[str], nexus: str = 'and', to_formula: bool = True):
    """
    Enumerates the strings in a list, optionally enclosing every element between `$`s.

    **Parameters**

    - `strings_list`: list

        A list with the strings to be joined.

    - `nexus`: str

        Text between the second to last and last elements.

    - `to_formula`: bool, optional

        If True every string will be enclosed in '$'s.

    **Returns**

    - `out`: str

        TeX compatible string.
    """

    if to_formula:

        delimiter = '$'

    else:

        delimiter = ''

    return delimiter + f'{delimiter}, {delimiter}'.join(strings_list[:-1]) + f'{delimiter} {nexus} {delimiter}{strings_list[-1]}{delimiter}'

# Cell
@to_formula_maybe
def gaussian_pdf(x: str = 'x', mean: str = r'\mu', variance: str = r'\sigma^2') -> str:
    """
    Returns a string representing the probability density function for a Gaussian distribution.

    **Parameters**

    - `x`: str

        The random variable.

    - `mean`: str, optional

        The mean of the random variable.

    - `variance`: str, optional

        The variance of the random variable.

    **Returns**

    - `out`: str

        TeX compatible string.
    """

    return r'\frac{1}{\sqrt{2\pi ' + variance + r'}}e^{-\frac{(' + x + '-' + mean + r')^2}{2' + variance + r'}}'

# Cell
@to_formula_maybe
def q_function_approximation(x: str = 'x') -> str:
    """
    Returns a string representing the Stirling approximation for the Q function.

    **Parameters**

    - `x`: str

        The argument of the Q function.

    **Returns**

    `out`: str

        TeX compatible string.
    """

    return f'Q({x}) \\approx \\frac{{1}}{{2}} e^{{-\\frac{{{x}^2}}{{2}}}}'

# Cell
@to_formula_maybe
def partwise_function(function: str, parts: List[Tuple[str, str]], add_zero_otherwise: bool = True) -> str:
    """
    Returns a string representing the definition a part-wise mathematical function.

    **Parameters**

    - `function`: str

        The name of the function.
    - `parts`: list

        Each element is a tuple yields whose 1st element is the value of the function and whose second is a condition stating where the 1st applies.
    - `add_zero_otherwise`: bool

        If True, one last part stating "0, otherwise" is added.

    **Returns**

    `out`: str
        TeX compatible string.
    """

    res = f'{function}='

    res += '\\begin{cases}\n'

    for p in parts:

        res += f'{p[0]},& {p[1]} \\\\'

    if add_zero_otherwise:

        res += r'0,& \text{otherwise}'

    res += r'\end{cases}'

    return res

# Cell
@to_formula_maybe
def from_number(n: Union[int, float], prefix: str = '', precision: int = 3, fixed_point_format: bool = False) -> str:
    """
    Returns a string for a given number.

    **Parameters**

    - `n`: int or float

        The number.
    - `prefix`: str

        A string to be prepended to the number.
    - `precision`: int

        Number of decimals (ignored if the number is an integer).
    - `fixed_point_format`: bool

        If True, a fixed-point format (f) is used regardless of the actual type.

    **Returns**

    - `out`: str

        TeX compatible string.
    """

    format_specifier = f'.{precision}{"f" if fixed_point_format else "g"}'

    return f'{prefix}{n:{format_specifier}}'

# Cell
@to_formula_maybe
def from_matrix(m: Union[list, np.ndarray], float_point_precision: int = 3) -> str:
    """
    Returns a string for a given array or matrix.

    **Parameters**

    - `m`: list or ndarray

        A numpy array or a list.

    - `float_point_precision`: int

        Number of decimals (ignored if the number is an integer).

    **Returns**

    - `out`: str

        TeX compatible string.
    """

    format_from_number = lambda x: f'.{float_point_precision}g' if (type(x) == np.float64) or (type(x) == float) else f'd'

    if isinstance(m[0], (list, np.ndarray)):

        return r'\begin{bmatrix}' + r' \\ '.join(
            [(r' & '.join([f'{e:{format_from_number(m[0][0])}}' for e in row])) for row in m]) + r'\end{bmatrix}'

    else:

        return r'\begin{bmatrix}' + r' & '.join([f'{e:{format_from_number(m[0])}}' for e in m]) + r'\end{bmatrix}'

# Cell
@to_formula_maybe
def dot_product(
    lhs_template: str, lhs: list, rhs_template: str, rhs: list, product_operator: str = '',
    addition_operator: str = '+') -> str:
    """
    Returns a string for the dot product of two vectors, regardless of whether they are symbols or numbers.

    **Parameters**

    - `lhs_template`: str

        Left-hand side template; it should include a replacement field ({}) that will be replaced by one of
        the elements in `lhs`

    - `lhs`: list

        Left-hand side elements.

    - `rhs_template`: str

        Right-hand side template; it should include a replacement field ({}) that will be replaced by one of
        the elements in `rhs`

    - `rhs`: list

        Right-hand side elements.

    - `product_operator`: str

        Symbol to be used as product operator.

    - `addition_operator`: str

        Symbol to be used as addition operator.

    **Returns**

    - `out`: str

        TeX compatible string.
    """

    return addition_operator.join([lhs_template.format(l) + product_operator + rhs_template.format(r) for l,r in zip(lhs, rhs)])

# Cell
@to_formula_maybe
def total_probability(fixed_symbol: str, varying_symbol_template: str, n: int, start_at: int = 1) -> str:
    """
    Returns a string for law of total probability.

    **Parameters**

    - `fixed_symbol`: str

        The symbol that stays the same in the summation.

    - `varying_symbol_template`: str

        A template for the varying symbol that includes a replacement field (`{}`) for the index.

    - `n`: int

        The number of values for the varying symbol.

    - `start_at`: int

        The index at which `varying_symbol_template`starts.

    **Returns**

    - `out`: str

        TeX compatible string.
    """

    return '+'.join([f'p({fixed_symbol},{varying_symbol_template.format(i)})' for i in range(start_at, start_at+n)])

# Cell

def enumerate_math(
    numbers_list: List[float], assigned_to: Optional[str] = None, nexus: Optional[str] = 'and',
    precision: Optional[int] = 3, start_at: Optional[int] = 1) -> str:
    """
    Builds a $\TeX$ string from a list of numbers in which each one is printed after (optionally) being assigned to an indexed variable that follows a given pattern.

    **Parameters**

    - `numbers_list`:  list of floats

        The elements to be enumerated.

    - `assigned_to`: str, optional

        Some text with a replacement field (this means that any { or } must be escaped by doubling it).

    - `nexus`: str, optional

        The text joining the second to last and last elements.

    - `precision`: int

        The number of decimal places.

    - `start_at`: int

        The index of the first element that enters the enumeration.

    **Returns**

    - `out`: str

        TeX compatible string.
    """

#     format_specifier = f'.{precision}f'
    format_specifier = f'.{precision}g'

    strings_list = [f'{e:{format_specifier}}' for e in numbers_list]

    if assigned_to:

        strings_list = [assigned_to.format(i_s) + ' = ' + s for i_s, s in enumerate(strings_list, start_at)]

    return join(strings_list, nexus=nexus)

# Cell
def enumerate_assignments(
    lhs_template: str, rhs_template: str, rhs: List[float], nexus: str = 'and', precision: int = 3, start_at: int = 1) -> str:
    """
    Constructs a enumeration of assignments from left-hand-side and right-hand-side templates and right-hand-side values. It's similar to `enumerate_math` when the argument `assigned_to` is passed to the latter, but more general since the right-hand expression is also obtained from a template.

    **Parameters**

    - `lhs_template`:  str

        Text with a replacement field that will be replaced by an index.

    - `rhs_template`: str

         Text with a replacement field that will be replaced by one of the corresponding elements in rhs.

    - `rhs`: list of `float`

        Elements to be enumerated.

    - `nexus`: str, optional

        The text joining the second to last and last elements.

    - `precision`: int

        The number of decimal places.

    - `start_at`: int

        The index of the first element that enters the enumeration.


    **Returns**

    - `out`: str

        TeX compatible string.
    """

    return join([f'{lhs_template} = {rhs_template}'.format(i, r) for i, r in enumerate(rhs, start_at)])

# Cell

def expand(template: str, n: int, to_math: bool = False, nexus: str = 'and', start_at: int = 1) -> str:
    """
    Expand a symbol according to a pattern.

    >>> util.expand('s_{}', 3, True)
    '$s_1$, $s_2$ and $s_3$'

    ***Parameters***

    - `template` : str

        String with a *single* replacement field ({})
    - `n` : int

        Requested number of terms
    - `to_math` : bool

        If `True`, every output term is enclosed between $'s
    - `nexus` : str

        String joining the second to last and last terms.
    - `start_at`: int

        The number at which indexes start.

    **Returns**

    - `out`: str

        TeX compatible string.
    """

    return join([template.format(i) for i in range(start_at, start_at + n)], to_formula=to_math)

assert expand('s_{}', 3, True) == '$s_1$, $s_2$ and $s_3$'