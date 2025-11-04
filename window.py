from logging import info
from tkinter import Button, Canvas, Tk
from tkinter.ttk import Treeview
from main import create_document
from question.question_registry import KEYWORD_REGISTRY, QUESTION_REGISTRY
from utilities.misc import configure_log

# TODO: Design UI.
# TODO: Add number of questions functionality.
# TODO: Have method of adding topics and subtopics to questions list.
# TODO: Make pdf of questions and answers viewable in the app.
# TODO: Temporarily store files and give option to save or export them for permanant storage.
# TODO: Have problem sheet templates with typical collections of questions.
# TODO: Each problem sheet stored in a ProblemSheet object containing #questions, question topics etc.
# TODO: Have left most column full list of questions, column to the right questions is current ProblemSheet, with "add" and "remove" buttons.
if __name__ == "__main__":
    configure_log()

    info(f"Question registry: {QUESTION_REGISTRY}")
    info(f"Keyword registry: {KEYWORD_REGISTRY}")

    root = Tk()
    root.title("Problem Sheet Generator")
    root.geometry("500x500")

    """ button = Button(
        root,
        text = "Generate Problem Sheet",
        command = create_document
    )
    button.grid() """

    question_tree = Treeview(root, show = "tree headings")
    question_tree.heading("#0", text = "Questions")
    question_tree.insert("", "end", "vect_calc", text = "Vector Calculus")
    question_tree.insert("vect_calc", "end", "line_integral", text = "Line integrals")
    question_tree.insert("line_integral", "end", "vector_field", text = "Vector fields")
    question_tree.insert("line_integral", "end", "scalar_field", text = "Scalar fields")
    question_tree.grid(row = 0, column = 0)

    selected_tree = Treeview(root, show = "tree headings")
    selected_tree.heading("#0", text = "Selected questions")
    selected_tree.grid(row = 0, column = 1)

    root.mainloop()