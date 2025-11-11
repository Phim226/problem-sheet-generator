from tkinter import Tk
from ttkbootstrap import Button, Checkbutton, Entry, IntVar, Label, Labelframe
from core.sheet_generator import SheetGenerator

class QuestionConfigurer():


    def __init__(self, root: Tk, generator: SheetGenerator):
        self._root = root

        self._generator = generator

        self._config_frame = Labelframe(root, text = "Configuration")
        self._config_frame.pack(side = "top", anchor = "nw")

    @property
    def problem_name_entry(self) -> Entry:
        return self._problem_name_entry

    @property
    def answer_name_entry(self) -> Entry:
        return self._answer_name_entry

    @property
    def tex_check(self) -> bool:
        return self._tex_check


    def build(self) -> None:
        Label(self._config_frame, text = "Problem sheet name: ").grid(row = 0, column = 0)
        self._problem_name_entry: Entry = Entry(self._config_frame)
        self._problem_name_entry.insert(0, "Problem_Sheet")
        self._problem_name_entry.grid(row = 0, column = 1, padx = 2, pady = 2)

        Label(self._config_frame, text = "Answer sheet name: ").grid(row = 1, column = 0)
        self._answer_name_entry: Entry = Entry(self._config_frame, text = "Answer_Sheet")
        self._answer_name_entry.insert(0, "Answer_Sheet")
        self._answer_name_entry.grid(row = 1, column = 1, padx = 2, pady = 2)

        self._tex_var = IntVar(value = 1)
        self._tex_check = Checkbutton(
            self._config_frame,
            text = "Generate tex file",
            variable = self._tex_var,
            onvalue = 1,
            offvalue = 0
        )
        self._tex_check.grid(row = 2, column = 0, pady = 2)

        button = Button(
            self._config_frame,
            text = "Generate Problem Sheet",
            command = self._generator.generate_sheets
        )
        button.grid(row = 3, column = 1, padx = 4, pady = 4)


