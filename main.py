import logging
import subprocess
import os
from pylatex import Document, Command, Enumerate
from pylatex.utils import NoEscape
from question.question_registry import create_question
from question.questions import Question
from utils import configure_log


RED = "\033[91m"
PURPLE = "\033[35m"
RESET = "\033[0m"
PERMISSION_ERROR_STR = " is being used by other processes and cannot be deleted. Close it before attempting to rerun the problem sheet generation process."
PROCESS_ERROR_STR =" LaTeX failed to process. This is mostly likely due to a mistake in the LaTeX syntax, the output files can't be overwritten or an " \
    "issue with your LaTeX installation (such as not having Perl installed). See the log file for more details.\n\nAn attempt will now be made to delete " \
    "the output files to prevent issues when rerunning the code."


def fill_preamble(doc: Document, title: str, author: str = "", date: str ="") -> None:
    doc.preamble.append(Command("usepackage",
                                "geometry",
                                "left=2.5cm, right=2.5cm"))  # Adjusts margin size of output pdf.
    doc.preamble.append(Command("title",
                                 title))
    doc.preamble.append(Command("author",
                                author))
    doc.preamble.append(Command("date",
                                date))
    doc.append(NoEscape(r"\maketitle"))

def try_delete_file(file_name: str) -> None:
    try:
        os.remove(file_name)
    except PermissionError as e:
        logging.error(f"{PURPLE}{type(e).__name__}{RESET}: {file_name}{PERMISSION_ERROR_STR}")

if __name__ == "__main__":
    configure_log()
    doc = Document()
    question: Question = create_question("vector_calculus", "line_integral")
    fill_preamble(doc, "Line Integral Questions")
    n=1
    """ while True:
        n = input("Enter number of questions:")
        try:
            n = int(n)
            break
        except:
            print("That is not a valid input. Please try again.") """
    with doc.create(Enumerate()) as enum:
        for i in range(n):
            enum.add_item(question.generate_question_latex())

    try:
        doc.generate_tex("output")
        doc.generate_pdf("output", clean_tex=False)
    except subprocess.CalledProcessError as e:
        logging.error(f"{PURPLE}{type(e).__name__}{RESET}:{PROCESS_ERROR_STR}")
        try_delete_file("output.fdb_latexmk")
        try_delete_file("output.pdf")
        try_delete_file("output.tex")