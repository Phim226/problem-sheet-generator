from dataclasses import dataclass, field
from tkinter import Tk, Widget, messagebox
from re import search
from ttkbootstrap import Button, Checkbutton, Entry, IntVar, Label, Labelframe, StringVar
from app.ui.sheet_creation.question_selector import QuestionSelector
from core.sheet_generator import SheetGenerator


@dataclass
class SheetConfig():
    problem_title: str = "Questions"
    problem_filename: str = "Problem_Sheet"
    answer_title: str = "Answers"
    answer_filename: str = "Answer_Sheet"
    num_questions: int = 1
    author: str = ""
    date: str = ""
    margin_left: str = "2.5cm"
    margin_right: str = "2.5cm"

    _generate_tex_int: int = field(default=1, repr=False)

    @property
    def generate_tex_int(self) -> int:
        return self._generate_tex_int

    @generate_tex_int.setter
    def generate_tex_int(self, value: int):
        if value not in (0, 1):
            raise ValueError("generate_tex_int must be 0 or 1")
        self._generate_tex_int = value

# TODO: Connect selecter information to config
class QuestionConfigurator():

    def __init__(self, root: Tk, selector: QuestionSelector):
        self._root = root

        self._selector = selector

        self._config_frame = Labelframe(root, text = "Configuration")
        self._config_frame.pack(side = "top", anchor = "nw")

        self._config: SheetConfig = SheetConfig()

        self._problem_filename_valid: bool = True
        self._answer_filename_valid: bool = True

        config_vars: list[str] = [key for key in self._config.__dict__.keys()]
        self._problem_filename_entry_id: str = config_vars[1]
        self._answer_filename_entry_id: str = config_vars[3]
        self._tex_check_id: str = config_vars[4]

    def _generate_sheets(self) -> None:
        self._generation_label.config(text = "Generating...")
        self._generation_label.update_idletasks()

        if not (self._problem_filename_valid and self._answer_filename_valid):
            msg = "Filenames are not valid. Rename them before generating."
            messagebox.showwarning("Warning", msg)
            self._generation_label.config(text = "")
            self._generation_label.update_idletasks()
            return

        selected_questions_dict = self._selector.selected_questions
        if not selected_questions_dict:
            msg = "No questions have been selected."
            messagebox.showwarning("Warning", msg)
            self._generation_label.config(text = "")
            self._generation_label.update_idletasks()
            return

        selected_questions = list(selected_questions_dict.values())
        generator: SheetGenerator = SheetGenerator(self._config)
        generator.generate(selected_questions, bool(self._config.generate_tex_int))

        self._root.focus()

        self._generation_label.config(text = "Generation complete!")
        self._generation_label.update_idletasks()
        return

    def build(self) -> None:
        validate_filename = self._root.register(self._validate_filename)
        self._build_entry(
            "Problem sheet filename: ",
            self._config.problem_filename,
            self._problem_filename_entry_id,
            0,
            validate_filename
        )

        self._build_entry(
            "Answer sheet filename: ",
            self._config.answer_filename,
            self._answer_filename_entry_id,
            1,
            validate_filename
        )

        self._build_tex_checkbox()

        self._build_generate_button()

    def _build_entry(
            self, label_text: str, default_value: str, id: str, row: int, validation_register: str
    ) -> None:
        Label(self._config_frame, text = label_text).grid(row = row, column = 0)

        entry_type: str = label_text.split()[0].lower()

        var: StringVar = StringVar(value = default_value, name = id)
        var_attr_name: str = f"_{entry_type}_filename_var"
        setattr(self, var_attr_name, var)

        entry_attr_name: str = f"_{entry_type}_filename_entry"
        entry: Entry = Entry(
            self._config_frame,
            textvariable = getattr(self, var_attr_name),
            validate = "focusout"
        )
        setattr(self, entry_attr_name, entry)

        widget: Entry = getattr(self, entry_attr_name)
        widget.config(validatecommand = (validation_register, "%W"))
        widget.id = id
        widget.grid(row = row, column = 1, padx = 2, pady = 2)

    def _build_tex_checkbox (self):
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
        save_config_val = self._root.register(self._save_config_value)
        self._tex_check.configure(command = (save_config_val, self._tex_check))
        self._tex_check.id = self._tex_check_id
        self._tex_check.grid(row = 2, column = 0, pady = 2)

    def _build_generate_button(self):
        self._generate_button = Button(
            self._config_frame,
            text = "Generate Problem Sheet",
            command = self._generate_sheets
        )
        self._generate_button.grid(row = 4, column = 0, pady = 4)

        self._generation_label = Label(self._config_frame, anchor = "w", justify = "left", width = 20)
        self._generation_label.grid(row = 4, column = 1)

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

        if search(r'[\\\/<>:"|*?]', filename):
            setattr(self, f"_{widget.id}_valid", False)

            msg = 'Filenames can\'t contain any of the following characters: \\ / < > : " | * ?'
            messagebox.showwarning("Warning", msg)
            return True

        elif filename in reserved_filenames:
            setattr(self, f"_{widget.id}_valid", False)
            messagebox.showwarning("Warning", f"{filename} is a reserved filename in Windows.")
            return True

        setattr(self, f"_{widget.id}_valid", True)
        self._save_config_value(widget)

        return True