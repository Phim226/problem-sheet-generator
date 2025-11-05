from tkinter import Tk
from ttkbootstrap import Style
from app.ui.question_selecter_builder import QuestionSelecterBuilder

THEME: str = "darkly"

class ProblemSheetGeneratorApp():


    def __init__(self, root: Tk):
        root.title("Problem Sheet Generator")
        root.geometry("500x500")
        self._root = root

    def build(self):
        self._configure_style()
        QuestionSelecterBuilder(self._root).build()

    @staticmethod
    def _configure_style():
        style = Style(theme = THEME)
        style.configure(
        "Treeview.Heading",
        background="#36434E",
        foreground="#CFCFCF",
        font=("Segoe UI", 9, "bold")
    )