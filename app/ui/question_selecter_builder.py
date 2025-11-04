from tkinter import Tk
from tkinter.ttk import Treeview
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

    def build(self):
        self._build_question_tree()
        self._selected_question_tree()



    def _build_question_tree(self):
        question_tree: Treeview = Treeview(self._root, show = "tree headings")
        question_tree.heading("#0", text = "Questions")

        question_types: list[Question] = sorted(list(TOPIC_REGISTRY.keys())[1:])
        for name in question_types:
            question_tree.insert("", "end", name, text = name)

            topics = QUESTION_REGISTRY[name].subtopics.keys()
            for topic in topics:
                question_tree.insert(name, "end", topic, text = topic)

                subtopics = TOPIC_REGISTRY[name][topic]
                for subtopic in subtopics:
                    question_tree.insert(topic, "end", f"{topic}_{subtopic}", text = subtopic)

        question_tree.grid(row = 0, column = 0)
        self._question_tree: Treeview = question_tree

    def _selected_question_tree(self):
        selected_tree = Treeview(self._root, show = "tree headings")
        selected_tree.heading("#0", text = "Selected Questions")
        selected_tree.grid(row = 0, column = 1)
        self._selected_tree: Treeview = selected_tree