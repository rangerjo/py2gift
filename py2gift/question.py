# AUTOGENERATED! DO NOT EDIT! File to edit: 03_question.ipynb (unless otherwise specified).

__all__ = ['pre_process_string_template', 'QuestionGenerator', 'NumericalQuestionGenerator',
           'MultipleChoiceQuestionGenerator', 'MultipleChoiceTheoreticalQuestionGenerator']

# Cell

import abc
import string
import re
from typing import List, Union, Optional, Tuple

import numpy as np

# Cell

def pre_process_string_template(text: str) -> str:

    text = text.replace('$', '$$')
    text = text.replace('!', '$')

    return text

# Cell

class QuestionGenerator(metaclass=abc.ABCMeta):

    def __init__(
            self, unprocessed_statement: string.Template, unprocessed_feedback: string.Template, time: Optional[int] = None,
            prng: np.random.RandomState = np.random.RandomState(42)) -> None:

        self.prng = prng

        # For the sake of "retrocompatibility", it is attempted to guess the format...
        # if "$$" is not present in the passed statement (new format)...
        if unprocessed_statement.template.find('$$') == -1:

            self.unprocessed_statement = string.Template(pre_process_string_template(unprocessed_statement.template))
            self.unprocessed_feedback = string.Template(pre_process_string_template(unprocessed_feedback.template))

        # if there is some "$$" (old format)...
        else:

            self.unprocessed_statement = unprocessed_statement
            self.unprocessed_feedback = unprocessed_feedback


        self.time = time

        self.statement = None

        # try...
        try:

            # ...to get the final string with no substitutions
            self.feedback = self.unprocessed_feedback.substitute()

        # some substitutions are needed to get the final string
        except KeyError:

            self.feedback = None

    @property
    @abc.abstractmethod
    def class_name(self) -> str:

        pass

    # this is the method to be defined by the user
    @abc.abstractmethod
    def setup(self, **kwargs):

        pass

    def partially_assemble_question(self, statement: str, feedback: str) -> dict:

        question = dict()

        question['class'] = self.class_name
        question['statement'] = statement
        question['feedback'] = feedback

        if self.time:

            question['time'] = str(self.time)

        return question

    def __call__(self, **kwargs):

        # arguments are passed directly to `setup`
        self.setup(**kwargs)

        assert self.statement is not None
        assert isinstance(self.statement, str), f'statement {self.statement} is not a string'

        assert self.feedback is not None
        assert isinstance(self.feedback, str), f'feedback {self.feedback} is not a string'

# Cell

class NumericalQuestionGenerator(QuestionGenerator):

    def __init__(
            self, unprocessed_statement: string.Template, unprocessed_feedback: string.Template,  time: Optional[int] = None,
            prng: np.random.RandomState = np.random.RandomState(42)) -> None:

        super().__init__(unprocessed_statement, unprocessed_feedback, time, prng)

        self.solution = None
        self.error = None

    @property
    def class_name(self) -> str:

        return 'Numerical'

    def assemble_question(self, statement: str, feedback: str, solution: float, error: Optional[float] = None) -> dict:

        question = self.partially_assemble_question(statement, feedback)

        # some yaml "writers" (e.g., ruamel.yaml) don't play well with numpy floats
        if type(solution) == np.float64:

            solution = solution.item()

        question['solution'] = dict()
        question['solution']['value'] = solution

        if error is None:

            # 10% margin
            error = solution * 0.1

        question['solution']['error'] = error

        return question

    def __call__(self, **kwargs):

        super().__call__(**kwargs)

        assert self.solution is not None
        assert self.error is not None

        return self.assemble_question(
            statement=self.statement, feedback=self.feedback, solution=self.solution, error=self.error)

# Cell

class MultipleChoiceQuestionGenerator(QuestionGenerator):

    def __init__(
            self, unprocessed_statement: Union[str, string.Template], unprocessed_feedback: Union[str, string.Template], time: Optional[int] = None,
            prng: np.random.RandomState = np.random.RandomState(42)) -> None:

        super().__init__(unprocessed_statement, unprocessed_feedback, time, prng)

        self.right_answer = None
        self.wrong_answers = None

    @property
    def class_name(self) -> str:

        return 'MultipleChoice'

    def assemble_question(
            self, statement: str, feedback: str, perfect_answer: str,
            wrong_answers: Union[List[str], List[Tuple[str, float]]]) -> dict:

        question = self.partially_assemble_question(statement, feedback)

        question['answers'] = dict()

        if self.right_answer:

            question['answers']['perfect'] = perfect_answer

        question['answers']['wrong'] = wrong_answers

        return question

    def __call__(self, **kwargs):

        super().__call__(**kwargs)

        if self.right_answer:

            assert isinstance(self.right_answer, str), f'right answer {self.right_answer} is not a string'

        assert self.wrong_answers is not None

        # in order to check that every wrong answer is different
        wrong_answers_texts = []

        for e in self.wrong_answers:

            assert isinstance(e, str) or isinstance(e, list)

            if isinstance(e, list):

                wrong_answers_texts.append(e[0])

                assert isinstance(e[0], str)
                assert isinstance(e[1], int) or isinstance(e[1], float)

            else:

                wrong_answers_texts.append(e)

        # all the answers are different
        assert np.unique(wrong_answers_texts).size == np.array(wrong_answers_texts).size, f'all the wrong answers are not different: {wrong_answers_texts}'


        return self.assemble_question(
            statement=self.statement, feedback=self.feedback, perfect_answer=self.right_answer,
            wrong_answers=self.wrong_answers)

# Cell

class MultipleChoiceTheoreticalQuestionGenerator(MultipleChoiceQuestionGenerator):

    def setup(self, right_answer: str, wrong_answers: List[str]):

        self.statement = self.unprocessed_statement.safe_substitute()
        self.feedback = self.unprocessed_feedback.safe_substitute()

        self.right_answer = right_answer
        self.wrong_answers = wrong_answers