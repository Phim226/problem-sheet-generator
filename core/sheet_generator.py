from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.ui.question_configurer import SheetConfig
from logging import error, info
from os import remove
from subprocess import CalledProcessError
from pylatex import Document, Enumerate
from core.sheet import AnswerSheet, QuestionSheet
from core.question.question_registry import create_question
from core.question.question import Question


# TODO: Include docstrings
# TODO: Update name of files to delete based on inputted filenames
class SheetGenerator():


    def __init__(self, config: SheetConfig):
        self._question_sheet: QuestionSheet = QuestionSheet(
            title = config.problem_title,
            file_name = config.problem_filename,
            author = config.author,
            date = config.date,
            margin = (config.margin_left, config.margin_right)
        )
        self._answer_sheet: AnswerSheet = AnswerSheet(
            title = config.answer_title,
            file_name = config.answer_filename,
            author = config.author,
            date = config.date,
            margin = (config.margin_left, config.margin_right)
        )

    # TODO: Change the names of the output files to include the creation date.
    def generate(self, num_questions: int = 1, generate_tex: bool = True):
        questions = self._question_sheet.document

        answers_list = []
        with questions.create(Enumerate()) as enum:
            for i in range(num_questions):
                question: Question = create_question(
                    "multivariable_calculus",
                    "line_integral",
                    **{"subtopic": "scalar_field"}
                )
                enum.add_item(question.question)
                answers_list.append(question.answer)
                info(f"Answer: {question.answer}")

        answers = self._answer_sheet.document

        with answers.create(Enumerate()) as enum:
            for i in range(num_questions):
                enum.add_item(answers_list[i])

        try:
            self._generate_output_files(questions, self._question_sheet.file_name, not generate_tex)
            self._generate_output_files(answers, self._answer_sheet.file_name, not generate_tex)
        except CalledProcessError as e:
            msg = (
                " LaTeX failed to process. This is most likely due to a mistake in the LaTeX syntax,"
                " the output files can't be overwritten or an issue with your LaTeX installation"
                " (such as not having Perl installed). See the log file for more details.\n\nAn"
                " attempt will now be made to delete the output files to prevent issues when"
                " rerunning the code."
            )
            error(f"{type(e).__name__}:{msg}")

            self._delete_files()

    @staticmethod
    def _generate_output_files(document: Document, name: str, clean_tex: bool = False):
        document.generate_pdf(f"output/{name}", clean_tex = clean_tex)

    @staticmethod
    def _delete_files():
        files = [
            "output/questions.fdb_latexmk", "output/questions.pdf", "output/questions.tex",
            "output/answers.fdb_latexmk", "output/answers.pdf", "output/answers.tex"
        ]
        for file in files:
            try:
                remove(file)
            except PermissionError as e:
                msg = (
                    " is being used by other processes and cannot be deleted. Close it before"
                    " attempting to rerun the problem sheet generation process."
                )
                error(f"{type(e).__name__}: {file}{msg}")
            except FileNotFoundError:
                continue


