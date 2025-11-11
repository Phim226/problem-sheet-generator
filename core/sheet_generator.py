from logging import error, info
from os import remove
from subprocess import CalledProcessError
from pylatex import Document, Enumerate
from core.sheet import AnswerSheet, QuestionSheet
from core.question.question_registry import create_question
from core.question.question import Question

# TODO: Include docstrings
class SheetGenerator():


    def __init__(self):
        self._answer_sheet: AnswerSheet = AnswerSheet("Answers")
        self._question_sheet: QuestionSheet = QuestionSheet("Questions")

    @staticmethod
    def _generate_output_files(document: Document, name: str, clean_tex: bool = False):
        document.generate_pdf(f"output/{name}", clean_tex = clean_tex)

    @staticmethod
    def _try_delete_file(file_name: str) -> None:
        try:
            remove(file_name)
        except PermissionError as e:
            msg = (
                " is being used by other processes and cannot be deleted. Close it before attempting"
                " to rerun the problem sheet generation process."
            )
            error(f"{type(e).__name__}: {file_name}{msg}")
        except FileNotFoundError:
            return

    # TODO: Change the names of the output files to include the creation date.
    def generate_sheets(self):
        questions = self._question_sheet.document

        n = 1
        # TODO: Implement inputting desired number of questions.
        """ while True:
            n = input("Enter number of questions:")
            try:
                n = int(n)
                break
            except:
                print("That is not a valid input. Please try again.") """

        answers_list = []
        with questions.create(Enumerate()) as enum:
            for i in range(n):
                question: Question = create_question(
                    "vector_calculus",
                    "line_integral",
                    **{"subtopic": "vector_field"}
                )
                enum.add_item(question.question)
                answers_list.append(question.answer)
                info(f"Answer: {question.answer}")

        answers = self._answer_sheet.document

        with answers.create(Enumerate()) as enum:
            for i in range(n):
                enum.add_item(answers_list[i])

        try:
            self._generate_output_files(questions, self._question_sheet.file_name)
            self._generate_output_files(answers, self._answer_sheet.file_name)
        except CalledProcessError as e:
            msg = (
                " LaTeX failed to process. This is most likely due to a mistake in the LaTeX syntax,"
                " the output files can't be overwritten or an issue with your LaTeX installation"
                " (such as not having Perl installed). See the log file for more details.\n\nAn"
                " attempt will now be made to delete the output files to prevent issues when"
                " rerunning the code."
            )
            error(f"{type(e).__name__}:{msg}")

            self._try_delete_file("output/questions.fdb_latexmk")
            self._try_delete_file("output/questions.pdf")
            self._try_delete_file("output/questions.tex")

            self._try_delete_file("output/answers.fdb_latexmk")
            self._try_delete_file("output/answers.pdf")
            self._try_delete_file("output/answers.tex")


