from logging import error, info
from os import remove
from subprocess import CalledProcessError
from pylatex import Document, Command, Enumerate
from pylatex.utils import NoEscape
from question.question_registry import create_question, QUESTION_REGISTRY, KEYWORD_REGISTRY
from question.question import Question
from utilities.misc import configure_log


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


def fill_preamble(
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

def try_delete_file(file_name: str) -> None:
    try:
        remove(file_name)
    except PermissionError as e:
        error(
            (f"{PURPLE}{type(e).__name__}{RESET}: "
             f"{file_name}{PERMISSION_ERROR_STR}")
        )

def create_document():
    pass

# TODO: Have output files saved in a dedicated folder.
# TODO: Change the names of the output files to include the creation date.
if __name__ == "__main__":
    print(f"Question registry: {QUESTION_REGISTRY}")
    print(f"Keyword registry: {KEYWORD_REGISTRY}")

    configure_log()

    questions = Document()
    fill_preamble(questions, "Line Integral Questions")

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
    # TODO: Create answer document.
    with questions.create(Enumerate()) as enum:
        for i in range(n):
            question: Question = create_question(
                "vector_calculus",
                "line_integral"
            )
            enum.add_item(question.generate_question_latex())
            answers_list.append(question.generate_answer())
            info(f"Answer: {question.generate_answer()}")

    try:
        questions.generate_tex("output/questions")
        questions.generate_pdf("output/questions", clean_tex=False)
    except CalledProcessError as e:
        error(
            f"{PURPLE}{type(e).__name__}{RESET}:{PROCESS_ERROR_STR}"
        )
        try_delete_file("output/questions.fdb_latexmk")
        try_delete_file("output/questions.pdf")
        try_delete_file("output/questions.tex")