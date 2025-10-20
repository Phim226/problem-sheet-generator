from pylatex import Document, Command, Enumerate
from pylatex.utils import NoEscape
from sympy.abc import t
from sympy.vector import CoordSys3D, ParametricRegion, vector_integrate
from question_registry import create_question, Question
import sympy as sp
import logging
import subprocess
import os

RED = "\033[91m"
PURPLE = "\033[35m"
RESET = "\033[0m"
PERMISSION_ERROR_STR = " is being used by other processes and cannot be deleted. Close it before attempting to rerun the worksheet generation process."
PROCESS_ERROR_STR =" LaTeX failed to process. This is mostly likely due to a mistake in the LaTeX syntax or the output files can't be overwritten. See the log file for more details.\n\n An attempt will now be made to delete the output files to prevent issues when rerunning the code.\n"
I_HAT_LATEX = r"\mathbf{{\hat{{i}}}}"
J_HAT_LATEX = r"\mathbf{{\hat{{j}}}}"
K_HAT_LATEX = r"\mathbf{{\hat{{k}}}}"
VECT_FIELD_LATEX = r"\mathbf{{F}}"

def configure_log():
    level = logging.DEBUG
    format = "[%(levelname)s] - %(message)s"
    logging.basicConfig(level = level, format = format)


def reformat_vector_field_latex(latex: str):
    vector_field_latex_dic = {r"\left(": "", r"\right)": "", "_{C}": "", r"\mathbf{{x}}": "x", r"\mathbf{{y}}": "y", r"\mathbf{{z}}": "z",}
    for i, j in vector_field_latex_dic.items():
        latex = latex.replace(i, j)
    return rf"${VECT_FIELD_LATEX}(x, y, z)={latex}$"

def format_curve_latex(curve: ParametricRegion):
    curve_def_x = sp.latex(curve.definition[0])
    curve_def_y = sp.latex(curve.definition[1])
    curve_def_z = sp.latex(curve.definition[2])
    curve_lower_lim = curve.limits[t][0]
    curve_upper_lim = curve.limits[t][1]
    return rf"$\mathbf{{r}}(t)={curve_def_x}{I_HAT_LATEX}+{curve_def_y}{J_HAT_LATEX}+{curve_def_z}{K_HAT_LATEX}$ for ${curve_lower_lim}\le t\le {curve_upper_lim}$"

def fill_preamble(doc: Document, title: str, author: str = "", date: str =""):
    doc.preamble.append(Command("usepackage", "geometry", "left=2.5cm, right=2.5cm"))
    doc.preamble.append(Command("title", title))
    doc.preamble.append(Command("author", author))
    doc.preamble.append(Command("date", date))
    doc.append(NoEscape(r"\maketitle"))

def format_question_latex(vector_field_latex: str, curve_latex: str):
    return NoEscape(rf"Let ${VECT_FIELD_LATEX}$ be the vector field {vector_field_latex} and $C$ the curve given by {curve_latex}. Calculate $\displaystyle\int_C{VECT_FIELD_LATEX}\cdot\mathbf{{dr}}$.")

def try_delete_file(file_name: str):
    try:
        os.remove(file_name)
    except PermissionError as e:
        logging.error(f"{PURPLE}{type(e).__name__}{RESET}: {file_name}{PERMISSION_ERROR_STR}")

if __name__ == "__main__":
    configure_log()
    doc = Document()
    question: Question = create_question("vector_calculus", "line_integral")
    fill_preamble(doc, "Line Integral Questions")
    while True:
        n = input("Enter number of questions:")
        try:
            n = int(n)
            break
        except:
            print("That is not a valid input. Please try again.")
    with doc.create(Enumerate()) as enum:
        for i in range(n):
            """ C = CoordSys3D("C")
            curve = ParametricRegion((t, t, 2*t**2), (t, 0, 1))
            F = C.y*C.i + C.x*C.j + C.z*C.k
            vector_field_latex = reformat_vector_field_latex(sp.latex(F))
            curve_latex = format_curve_latex(curve)
            enum.add_item(format_question_latex(vector_field_latex, curve_latex)) """
            enum.add_item(question.generate_question_latex())
    
    try:
        doc.generate_tex("output") 
        doc.generate_pdf("output", clean_tex=False)
    except subprocess.CalledProcessError as e:
        logging.error(f"{PURPLE}{type(e).__name__}{RESET}:{PROCESS_ERROR_STR}")
        try_delete_file("output.fdb_latexmk")
        try_delete_file("output.pdf")
        try_delete_file("output.tex")