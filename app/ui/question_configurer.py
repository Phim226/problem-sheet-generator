from dataclasses import dataclass
from tkinter import Tk
from ttkbootstrap import Button, Checkbutton, Entry, IntVar, Label, Labelframe, StringVar
from core.sheet_generator import SheetGenerator


@dataclass
class SheetConfig():
    problem_title: str = "Questions"
    problem_filename: str = "Problem_Sheet"
    answer_title: str = "Answers"
    answer_filename: str = "Answer_Sheet"
    generate_tex: bool = True
    num_questions: int = 1
    author: str = ""
    date: str = ""
    margin_left: str = "2.5cm"
    margin_right: str = "2.5cm"

# TODO: Validate problem and answer names.
class QuestionConfigurer():

    _problem_name_entry_id: str = "problem_name_entry"
    _answer_name_entry_id: str = "answer_name_entry"
    _tex_check_id: str = "tex_check"

    _problem_name_default: str = "Problem_Sheet"
    _answer_name_default: str = "Answer_Sheet"
    _tex_check_int_default: int = 1


    def __init__(self, root: Tk):
        self._root = root

        self._config_frame = Labelframe(root, text = "Configuration")
        self._config_frame.pack(side = "top", anchor = "nw")

        self._config: SheetConfig = SheetConfig()


    @property
    def problem_name_entry(self) -> Entry:
        return self._problem_filename_entry

    @property
    def answer_name_entry(self) -> Entry:
        return self._answer_filename_entry

    @property
    def tex_check(self) -> bool:
        return self._tex_check

    def _generate_sheets(self):
        generator: SheetGenerator = SheetGenerator(self._config)
        generator.generate(self._config.num_questions)

    def _validate(self):
        pass

    def build(self) -> None:
        Label(self._config_frame, text = "Problem sheet filename: ").grid(row = 0, column = 0)
        self._problem_filename_var: StringVar = StringVar(value = self._config.problem_filename)
        self._problem_filename_entry: Entry = Entry(
            self._config_frame,
            textvariable = self._problem_filename_var,
            validate = "focusout",
            validatecommand = self._validate
        )
        self._problem_filename_entry.grid(row = 0, column = 1, padx = 2, pady = 2)

        Label(self._config_frame, text = "Answer sheet filename: ").grid(row = 1, column = 0)
        self._answer_filename_var: StringVar = StringVar(value = self._config.answer_filename)
        self._answer_filename_entry: Entry = Entry(
            self._config_frame,
            textvariable = self._answer_filename_var,
            validate = "focusout",
            validatecommand = self._validate
        )
        self._answer_filename_entry.grid(row = 1, column = 1, padx = 2, pady = 2)

        self._tex_var: IntVar = IntVar(value = int(self._config.generate_tex))
        self._tex_check = Checkbutton(
            self._config_frame,
            text = "Generate tex file",
            variable = self._tex_var,
            onvalue = 1,
            offvalue = 0,
            command = self._validate
        )
        self._tex_check.grid(row = 2, column = 0, pady = 2)

        button = Button(
            self._config_frame,
            text = "Generate Problem Sheet",
            command = self._generate_sheets
        )
        button.grid(row = 3, column = 1, padx = 4, pady = 4)


