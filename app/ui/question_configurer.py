from tkinter import Tk
from ttkbootstrap import Button, Frame, Label, Labelframe

class QuestionConfigurer():


    def __init__(self, root: Tk):
        self._root = root
        self._config_frame = Labelframe(root, text = "Configuration")
        self._config_frame.pack(side = "top", anchor = "nw")


    def build(self):
        Label(self._config_frame, text = "Questions").grid(row = 0, column = 0)