from dataclasses import dataclass
from tkinter import Tk, Widget, messagebox
from re import search
from ttkbootstrap import Button, Checkbutton, Entry, IntVar, Label, Labelframe, StringVar
from core.sheet_generator import SheetGenerator


@dataclass
class SheetConfig():
    problem_title: str = "Questions"
    problem_filename: str = "Problem_Sheet"
    answer_title: str = "Answers"
    answer_filename: str = "Answer_Sheet"
    generate_tex_int: int = 1 # 1 is True, 0 is False
    num_questions: int = 1
    author: str = ""
    date: str = ""
    margin_left: str = "2.5cm"
    margin_right: str = "2.5cm"

class QuestionConfigurer():

    def __init__(self, root: Tk):
        self._root = root

        self._config_frame = Labelframe(root, text = "Configuration")
        self._config_frame.pack(side = "top", anchor = "nw")

        self._config: SheetConfig = SheetConfig()

        self._filenames_valid: bool = True

        config_vars: list[str] = [key for key in self._config.__dict__.keys()]
        self._problem_filename_entry_id: str = config_vars[1]
        self._answer_filename_entry_id: str = config_vars[3]
        self._tex_check_id: str = config_vars[4]

    def _generate_sheets(self) -> None:
        if not self._filenames_valid:
            messagebox.showwarning("Warning", "Filenames are not valid. Rename them before generating.")
            return

        generator: SheetGenerator = SheetGenerator(self._config)
        generator.generate(self._config.num_questions, bool(self._config.generate_tex_int))

        self._root.focus()

    def _save_config_value(self, widget: Widget | str) -> None:
        if not isinstance(widget, Widget):
            widget = self._root.nametowidget(widget)

        value = widget.getvar(widget.id)

        if isinstance(value, str):
            value = value.strip()

        setattr(self._config, widget.id, value)

    def _validate_filename(self, widget_str: str) -> bool:
        widget: Entry = self._root.nametowidget(widget_str)
        filename: str = widget.get()

        reserved_filenames: list[str] = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4",
                                         "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2",
                                         "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]

        if search('[\\\/<>:"|*?]', filename):
            self._filenames_valid = False
            messagebox.showwarning("Warning", 'Filenames can\'t contain any of the following characters: \\ / < > : " | * ?')
            return True

        elif filename in reserved_filenames:
            self._filenames_valid = False
            messagebox.showwarning("Warning", f"{filename} is a reserved filename is windows.")
            return True

        self._filenames_valid = True
        self._save_config_value(widget)

        return True

    def build(self) -> None:
        validate_filename = self._root.register(self._validate_filename)
        save_config_val = self._root.register(self._save_config_value)

        Label(self._config_frame, text = "Problem sheet filename: ").grid(row = 0, column = 0)
        self._problem_filename_var: StringVar = StringVar(
            value = self._config.problem_filename,
            name = self._problem_filename_entry_id
        )
        self._problem_filename_entry: Entry = Entry(
            self._config_frame,
            textvariable = self._problem_filename_var,
            validate = "focusout"
        )
        self._problem_filename_entry.config(validatecommand = (validate_filename, "%W"))
        self._problem_filename_entry.id = self._problem_filename_entry_id
        self._problem_filename_entry.grid(row = 0, column = 1, padx = 2, pady = 2)

        Label(self._config_frame, text = "Answer sheet filename: ").grid(row = 1, column = 0)
        self._answer_filename_var: StringVar = StringVar(
            value = self._config.answer_filename,
            name = self._answer_filename_entry_id
        )
        self._answer_filename_entry: Entry = Entry(
            self._config_frame,
            textvariable = self._answer_filename_var,
            validate = "focusout"
        )
        self._answer_filename_entry.config(validatecommand = (validate_filename, "%W"))
        self._answer_filename_entry.id = self._answer_filename_entry_id
        self._answer_filename_entry.grid(row = 1, column = 1, padx = 2, pady = 2)

        self._tex_var: IntVar = IntVar(
            value = self._config.generate_tex_int,
            name = self._tex_check_id
        )
        self._tex_check = Checkbutton(
            self._config_frame,
            text = "Generate tex file",
            variable = self._tex_var,
            onvalue = 1,
            offvalue = 0
        )
        self._tex_check.configure(command = (save_config_val, self._tex_check))
        self._tex_check.id = self._tex_check_id
        self._tex_check.grid(row = 2, column = 0, pady = 2)

        self._generate_button = Button(
            self._config_frame,
            text = "Generate Problem Sheet",
            command = self._generate_sheets
        )
        self._generate_button.grid(row = 3, column = 1, padx = 4, pady = 4)


