from tkinter import Event, Tk
from ttkbootstrap import Button, Frame, Scrollbar, Treeview
from question.question import Question
from question.question_registry import TOPIC_REGISTRY, QUESTION_REGISTRY

# TODO: Have left most column full list of questions, column to the right questions is current ProblemSheet, with "add" and "remove" buttons.
# TODO: Double click moves question to selected questions.
# TODO: Questions list have tick boxes, pressing "add" adds all selected questions.
# TODO: Have method of adding topics and subtopics to questions list.
# TODO: Give users ability to edit questions in question selecter
class QuestionSelecterBuilder():


    def __init__(self, root: Tk):
        self._root = root
        self._selecter_frame = Frame(root)
        self._selecter_frame.pack(side = "top", anchor = "nw")

    @property
    def question_tree(self) -> Treeview:
        return self._question_tree

    @property
    def selection_tree(self) -> Treeview:
        return self._selected_tree

    def build(self) -> None:
        self._question_tree: Treeview = self._build_question_tree("Questions")
        self._populate_question_tree(self._question_tree)

        self._selected_tree: Treeview = self._build_question_tree("Selected Questions")

    @staticmethod
    def _populate_question_tree(tree: Treeview) -> None:
        question_types: list[Question] = sorted(list(TOPIC_REGISTRY.keys())[1:])
        for name in question_types:
            tree.insert("", "end", name, text = name)

            topics = QUESTION_REGISTRY[name].subtopics.keys()
            for topic in topics:
                tree.insert(name, "end", topic, text = topic)

                subtopics = TOPIC_REGISTRY[name][topic]
                for subtopic in subtopics:
                    tree.insert(topic, "end", f"{topic}_{subtopic}", text = subtopic)


    def _build_question_tree(self, title: str) -> Treeview:
        tree_frame: Frame = Frame(self._selecter_frame)
        tree_frame.pack(side = "left")

        button = Button(tree_frame,
                        text = "add" if title == "Questions" else "remove")
        button.pack(side = "bottom", anchor = "se")

        tree = Treeview(tree_frame, show = "tree headings")
        tree.heading("#0", text = title)
        tree.pack(side = "left")

        vertical_scroll = Scrollbar(tree_frame, orient = "vertical", command = tree.yview)
        vertical_scroll.pack(side = "right", fill = "y")

        tree.configure(yscrollcommand = vertical_scroll.set)

        tree.bind("<Double-1>", self._double_click)

        tree.widget_id = f"{title.replace(" ", "_").lower()}_tree"

        return tree

    def _double_click(self, event: Event):
        print(event.widget.widget_id)
        widget: Treeview = event.widget
        print(widget.identify_row(event.y))