# AUTOGENERATED! DO NOT EDIT! File to edit: 02_util.ipynb (unless otherwise specified).

__all__ = ['render_latex', 'to_formula_maybe', 'AccessorEndowedClass', 'int_to_roman', 'hash_matrix', 'hash_number',
           'hash_string', 'extract_class_settings', 'write_multiple_categories', 'supplement_file_name', 'add_name',
           'markdown_from_question', 'generator_to_markdown', 'latex_to_markdown',
           'wrong_numerical_solutions_from_correct_one']

# Cell

import pathlib
import re
import sys
from typing import List, Dict, Union, Optional

import numpy as np
import IPython.display
import ruamel.yaml
import yaml
import pandas as pd
from pandas.core.accessor import _register_accessor as register_accessor

import gift_wrapper.core
import gift_wrapper.question
import gift_wrapper.image
import py2gift.core
import py2gift.question

# Cell

def render_latex(text: str) -> str:

    return IPython.display.Markdown(re.sub(r'\$([^\$]*)\$', '$' + '\\\Large ' + r'\1' + '$', text))

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
    return wrapper

# Cell
class AccessorEndowedClass:

    _accessors = set()

# Cell

# taken from https://www.w3resource.com/python-exercises/class-exercises/python-class-exercise-1.php
def int_to_roman(num: int) -> str:
    """
    Returns an integer number in roman format.
    """

    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num

assert int_to_roman(12) == 'XII'
assert int_to_roman(9) == 'IX'

# Cell

def hash_matrix(matrix: Union[list, np.ndarray], decimal_sep_replacement: Optional[bool] = '_') -> str:

    res = ''.join(np.vectorize(str)(np.array(matrix).flatten()))

    if decimal_sep_replacement:

        res = res.replace(r'.', decimal_sep_replacement)

    return res

assert hash_matrix([2, 3]) == '23'

# Cell

def hash_number(number: Union[float, np.float64], decimal_sep_replacement: Optional[bool] = '_') -> str:

    res = str(number)

    if decimal_sep_replacement:

        res = res.replace(r'.', decimal_sep_replacement)

    return res

assert hash_number(2.3) == '2_3'

# Cell

def hash_string(s: str) -> str:

    return ''.join(x for x in s if x.isalnum())

# Cell

def extract_class_settings(category_name: Union[str, list], class_name: str, settings: dict):

    category_found = False

    for cat in settings['categories']:

        if cat['name'] == category_name:

            category_found = True

            for cls in cat['classes']:

                if cls['name'] == class_name:

                    return cls

    else:

        if category_found:

            print(f'cannot find the requested class, {class_name}')
            sys.exit(1)

        else:

            print(f'cannot find the requested category, {category_name}')
            sys.exit(1)

# Cell

def write_multiple_categories(
        category_questions: Dict[str, List[dict]], pictures_base_directory: str, output_file: str = 'out.yaml') -> None:
    """
    Writes a file suitable as input to `gift-wrapper`.

    Parameters
    ----------
    category_questions : dict
        Every key is the name of a category, and every value is a list of questions
        (every question is itself a dictionary).
    pictures_base_directory : str
        The "pictures base directory" parameter that must be passed to `gift-wrapper`
    output_file : str
        Output file

    """

    file = dict()
    file['pictures base directory'] = pictures_base_directory
    file['categories'] = []

    for category_name, questions in category_questions.items():

        file['categories'].append({'name': category_name, 'questions': questions})

    yaml = ruamel.yaml.YAML()
    yaml.indent(sequence=4, offset=2)

    with open(output_file, 'w') as f:

        yaml.dump(file, f)

# Cell

def supplement_file_name(file: Union[str, pathlib.Path], sup: str) -> pathlib.Path:
    """
    Adds a string between the file name in a path and the suffix.

    Parameters
    ----------
    file : str
        File name
    sup : str
        String to be added

    Returns
    -------
    out: pathlib.Path
        "Supplemented" file

    """

    file = pathlib.Path(file)

    # the `suffix` is incorporated into the file name
    return file.with_name(file.stem + f'_{sup}' + file.suffix)

assert supplement_file_name('/a/b/quixote.tex', 'foo') == pathlib.Path('/a/b/quixote_foo.tex')

# Cell

def add_name(questions: List[dict], base_name: str) -> List[dict]:
    """
    Adds a name to every question based on a pattern.

    Parameters
    ----------
    questions : list
        List of questions; every question is a dictionary.
    question_base_name : str
        All the questions will be given this name and a different (Roman) number.

    Returns
    -------
    out: list
        List with the same questions after adding the corresponding name to each one.

    """

    res = []

    for i_q, q in enumerate(questions):

        res.append({**q, 'name': f'{base_name} {int_to_roman(i_q + 1)}'})

    return res

assert add_name([{'k1': 'aa', 'k2': 1}, {'k3': 'pi', 'foo': 'variance'}], 'Viterbi') == [
    {'k1': 'aa', 'k2': 1, 'name': 'Viterbi I'}, {'k3': 'pi', 'foo': 'variance', 'name': 'Viterbi II'}]

# Cell

def markdown_from_question(question_settings: dict, question_class: gift_wrapper.question.HtmlQuestion) -> str:

    # `None` values for width and height are assumed
    question_settings['images_settings'] = {'width': None, 'height': None}

    # the class is removed from the dictionary so that it doesn't get passed to the initializer
    del question_settings['class']

    # latex formulas are not checked
    question_settings['check_latex_formulas'] = False

    question_settings['history'] = {'already compiled': set()}

    question_settings['latex_auxiliary_file'] = '__latex__.tex'

    question_settings['name'] = 'Test'

    question = gift_wrapper.question.SvgToMarkdown(
        gift_wrapper.question.TexToSvg(question_class(**question_settings))
    )

    markdown = question.to_jupyter()

    for f in question.pre_processing_functions:

        markdown = f(markdown)

    return markdown

# Cell

def generator_to_markdown(settings_file: str, category: str, cls: py2gift.question.QuestionGenerator):

    with open(settings_file) as yaml_data:

        settings = yaml.load(yaml_data, Loader=yaml.FullLoader)

    question_settings = py2gift.core.build_question(cls, category, settings)
    question_class = getattr(gift_wrapper.question, question_settings['class'])

    return markdown_from_question(question_settings, question_class)

# Cell

def latex_to_markdown(input_file: Union[str, pathlib.Path], delete_input_file_afterwards: bool = False) -> str:

    output_file = gift_wrapper.image.pdf_to_svg(gift_wrapper.image.tex_to_pdf(input_file))

    suffixes = ['.aux', '.log', '.pdf']

    if delete_input_file_afterwards:

        suffixes.append('.tex')

    for suffix in suffixes:

        file_to_delete = output_file.with_suffix(suffix)

        if file_to_delete.exists():

            file_to_delete.unlink()

    return r'![](' + output_file.as_posix() + ')'

# Cell

def wrong_numerical_solutions_from_correct_one(
    solution: float, n: int, min_sep: float, max_sep: float, lower_bound: float, upper_bound: float,
    precision: int = 4, to_str: bool = True, prng: np.random.RandomState = np.random.RandomState(42)) -> Union[List[float], List[str]]:

    assert (solution - min_sep > lower_bound) or (solution + min_sep < upper_bound)

    res = []

    current = solution

    while len(res) < n:

        steps = prng.uniform(min_sep, max_sep, size=2)

        next_values = [v.round(precision) for v in [current + steps[0], current - steps[1]]  if lower_bound < v < upper_bound]

        res.extend(next_values)

    if to_str:

        res = [str(e) for e in res]

    return res[:n]