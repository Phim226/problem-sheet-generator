from logging import error, info
from os import remove
from subprocess import CalledProcessError
from pylatex import Command, Document, Enumerate
from pylatex.utils import NoEscape
from question.question_registry import (KEYWORD_REGISTRY, QUESTION_REGISTRY,
                                        create_question)
from question.question import Question
from utilities.misc import configure_log

# TODO: Include docstrings

RED = "\033[91m"
PURPLE = "\033[35m"
RESET = "\033[0m"
PERMISSION_ERROR_STR = (
    " is being used by other processes and cannot be "
    "deleted. Close it before attempting to rerun the problem sheet "
    "generation process."
)
PROCESS_ERROR_STR =(
    " LaTeX failed to process. This is most likely due to a mistake in the "
    "LaTeX syntax, the output files can't be overwritten or an issue with "
    "your LaTeX installation (such as not having Perl installed). See the "
    "log file for more details.\n\nAn attempt will now be made to delete "
    "the output files to prevent issues when rerunning the code."
)


def _fill_preamble(
        doc: Document,
        title: str,
        author: str = "",
        date: str = ""
) -> None:
    doc.preamble.append(
        Command(
            "usepackage",
            "geometry",
            "left=2.5cm, right=2.5cm"
        )
    )  # Adjusts margin size of output pdf.
    doc.preamble.append(Command("title", title))
    doc.preamble.append(Command("author", author))
    doc.preamble.append(Command("date", date))
    doc.append(NoEscape(r"\maketitle"))

def _try_delete_file(file_name: str) -> None:
    try:
        remove(file_name)
    except PermissionError as e:
        error(
            (f"{PURPLE}{type(e).__name__}{RESET}: "
             f"{file_name}{PERMISSION_ERROR_STR}")
        )

def _generate_output_files(document: Document, name: str):
    document.generate_tex(f"output/{name}")
    document.generate_pdf(f"output/{name}", clean_tex = False)

# TODO: Change the names of the output files to include the creation date.
def create_document():
    questions = Document()
    _fill_preamble(questions, "Questions")

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

    answers = Document()
    _fill_preamble(answers, "Answers")

    with answers.create(Enumerate()) as enum:
        for i in range(n):
            enum.add_item(answers_list[i])

    try:
        _generate_output_files(questions, "questions")
        _generate_output_files(answers, "answers")
    except CalledProcessError as e:
        error(
            f"{PURPLE}{type(e).__name__}{RESET}:{PROCESS_ERROR_STR}"
        )
        _try_delete_file("output/questions.fdb_latexmk")
        _try_delete_file("output/questions.pdf")
        _try_delete_file("output/questions.tex")

        _try_delete_file("output/answers.fdb_latexmk")
        _try_delete_file("output/answers.pdf")
        _try_delete_file("output/answers.tex")

if __name__ == "__main__":
    configure_log()

    info(f"Question registry: {QUESTION_REGISTRY}")
    info(f"Keyword registry: {KEYWORD_REGISTRY}")

    create_document()