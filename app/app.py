from tkinter import Event, Tk, Widget
from ttkbootstrap import Style, Treeview
from app.ui.question_selecter import QuestionSelecter
from app.ui.question_configurer import QuestionConfigurer
from core.sheet_generator import SheetGenerator

THEME: str = "darkly"

# TODO: Put placement data here and pass to objects so there is a higher level view of panel placement.
class ProblemSheetGeneratorApp():


    def __init__(self, root: Tk, generator: SheetGenerator):
        root.title("Problem Sheet Generator")
        root.geometry("500x500")
        root.bind_all("<Button-1>", self._global_mouse_click, add = "+")
        self._root = root

        self._question_selecter = QuestionSelecter(root)

        self._question_configurer = QuestionConfigurer(root, generator)

    def build(self) -> None:
        self._configure_style()
        self._question_selecter.build()
        self._question_configurer.build()

    @staticmethod
    def _configure_style() -> None:
        style = Style(theme = THEME)
        style.configure(
        "Treeview.Heading",
        background="#36434E",
        font=("Segoe UI", 9, "bold")
    )

    def _global_mouse_click(self, event: Event) -> None:
        widget = event.widget

        self._deselect_treeviews(widget, event)

    def _deselect_treeviews(self, widget: Widget, event: Event) -> None:

        # Prevents the question treeviews from being deselected when "add" or "removed" is pressed.
        if hasattr(widget, "tree_button_id") and widget.tree_button_id in (
             self._question_selecter.question_tree_id,
             self._question_selecter.selected_tree_id
        ):
             return

        treeviews = [
                self._question_selecter.question_tree,
                self._question_selecter.selected_tree
            ]

        if isinstance(widget, Treeview):
            treeviews.remove(widget)
            row = widget.identify_row(event.y)
            if row:
                for tree in treeviews:
                    tree.selection_remove(tree.selection())
                return
            else:
                widget.selection_remove(widget.selection())

        for tree in treeviews:
                    tree.selection_remove(tree.selection())

