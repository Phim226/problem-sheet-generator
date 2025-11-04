from tkinter import Tk
from tkinter.ttk import Treeview

# TODO: Have left most column full list of questions, column to the right questions is current ProblemSheet, with "add" and "remove" buttons.
# TODO: Double click moves question to selected questions.
# TODO: Questions list have tick boxes, pressing "add" adds all selected questions.
# TODO: Have method of adding topics and subtopics to questions list.
class QuestionSelecterBuilder():


    def __init__(self, root: Tk):
        self._root = root

    @property
    def root(self):
        return self._root

    def build(self):
        self._build_question_tree()
        self._selected_question_tree()

    def _build_question_tree(self):
        question_tree = Treeview(self._root, show = "tree headings")
        question_tree.heading("#0", text = "Questions")
        question_tree.insert("", "end", "vect_calc", text = "Vector Calculus")
        question_tree.insert("vect_calc", "end", "line_integral", text = "Line integrals")
        question_tree.insert("line_integral", "end", "vector_field", text = "Vector fields")
        question_tree.insert("line_integral", "end", "scalar_field", text = "Scalar fields")
        question_tree.grid(row = 0, column = 0)
        self._question_tree: Treeview = question_tree

    def _selected_question_tree(self):
        selected_tree = Treeview(self._root, show = "tree headings")
        selected_tree.heading("#0", text = "Selected questions")
        selected_tree.grid(row = 0, column = 1)
        self._selected_tree: Treeview = selected_tree