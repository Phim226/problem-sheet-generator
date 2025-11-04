from tkinter import Tk
from app.ui.question_selecter_builder import QuestionSelecterBuilder

class ProblemSheetGeneratorApp():


    def __init__(self, root: Tk):
        root.title("Problem Sheet Generator")
        root.geometry("500x500")
        self._root = root

    @property
    def root(self):
        return self._root

    def build(self):
        QuestionSelecterBuilder(self._root).build()