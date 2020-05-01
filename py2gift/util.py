# AUTOGENERATED! DO NOT EDIT! File to edit: 02_util.ipynb (unless otherwise specified).

__all__ = ['render_latex', 'to_formula_maybe', 'int_to_roman', 'hash_matrix', 'supplement_file_name',
           'write_multiple_categories', 'add_name', 'markdown_from_question']

# Cell

import pathlib
import re
from typing import List, Dict, Union, Optional

import numpy as np
import IPython.display
import ruamel.yaml

import gift_wrapper.core
import gift_wrapper.question

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

            return func(*args, **kwargs)
    return wrapper

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

def hash_matrix(matrix: Union[list, np.ndarray], decimal_sep_replacement: Optional[bool] = '_'):

    res = ''.join(np.vectorize(str)(np.array(matrix).flatten()))

    if decimal_sep_replacement:

        res = res.replace(r'.', decimal_sep_replacement)

    return res

assert hash_matrix([2, 3]) == '23'

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

    question_settings['name'] = 'Test'

    question = gift_wrapper.question.SvgToMarkdown(
        gift_wrapper.question.TexToSvg(question_class(**question_settings))
    )

    markdown = question.to_jupyter()

    for f in question.pre_processing_functions:

        markdown = f(markdown)

    return markdown