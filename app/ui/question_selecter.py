from tkinter import Event, Tk
from ttkbootstrap import Button, Frame, Scrollbar, Treeview
from question.question import Question
from question.question_registry import TOPIC_REGISTRY, QUESTION_REGISTRY

# TODO: Write docstrings
# TODO: Have left most column full list of questions, column to the right questions is current ProblemSheet, with "add" and "remove" buttons.
# TODO: Double click moves question to selected questions.
# TODO: Questions list have tick boxes, pressing "add" adds all selected questions.
# TODO: Have method of adding topics and subtopics to questions list.
# TODO: Give users ability to edit questions in question selecter
class QuestionSelecter():

    _question_tree_title: str = "Question Topics"
    _question_tree_id: str = "questions_tree"

    _selected_tree_title: str = "Selected Topics"
    _selected_tree_id: str = "selected_questions_tree"


    def __init__(self, root: Tk):
        self._root = root
        self._selecter_frame = Frame(root)
        self._selecter_frame.pack(side = "top", anchor = "nw")

    @property
    def question_tree(self) -> Treeview:
        return self._question_tree

    @property
    def selected_tree(self) -> Treeview:
        return self._selected_tree

    @property
    def question_tree_id(self) -> str:
        return self._question_tree_id

    @property
    def selected_tree_id(self) -> str:
        return self._selected_tree_id

    def build(self) -> None:
        self._question_tree: Treeview = self._build_question_tree(
            self._question_tree_title,
            self._question_tree_id
        )
        self._populate_question_tree(self._question_tree)

        self._selected_tree: Treeview = self._build_question_tree(
            self._selected_tree_title,
            self._selected_tree_id
        )

    @staticmethod
    def _populate_question_tree(tree: Treeview) -> None:
        question_types: list[Question] = sorted(list(TOPIC_REGISTRY.keys())[1:])
        for name in question_types:
            tree.insert("", "end", iid = name, text = name)

            topics = QUESTION_REGISTRY[name].subtopics.keys()
            for topic in topics:
                tree.insert(name, "end", iid = topic, text = topic)

                subtopics = TOPIC_REGISTRY[name][topic]
                for subtopic in subtopics:
                    tree.insert(topic, "end", iid = f"{topic}_{subtopic}", text = subtopic)


    def _build_question_tree(self, title: str, id: str) -> Treeview:
        tree_frame: Frame = Frame(self._selecter_frame)
        tree_frame.pack(side = "left")

        button = Button(
            tree_frame,
            text = "add" if title == self._question_tree_title else "remove",
            command = self._add if title == self._question_tree_title else self._remove
        )
        button.tree_button_id = id
        button.pack(side = "bottom", anchor = "se")

        tree = Treeview(tree_frame, show = "tree headings")
        tree.heading("#0", text = title)
        tree.pack(side = "left")

        vertical_scroll = Scrollbar(tree_frame, orient = "vertical", command = tree.yview)
        vertical_scroll.pack(side = "right", fill = "y")

        tree.configure(yscrollcommand = vertical_scroll.set)

        tree.widget_id = id

        return tree

    def _get_root_item_id(self, tree: Treeview, item_id: str) -> str:
        parent = tree.parent(item_id)

        if not parent:
            return item_id
        else:
            return self._get_root_item_id(tree, parent)

    def _copy_children(
            self,
            source_tree: Treeview,
            destination_tree: Treeview,
            item_id: str,
            parent_id: str = "",
            children: list[str] = []
    ) -> list[str]:
        text = source_tree.item(item_id)["text"]
        id = destination_tree.insert(parent_id, "end", iid = item_id, text = text)

        item_children = source_tree.get_children(item_id)
        if item_children:
            for child_id in item_children:
                children.append(child_id)
                self._copy_children(source_tree, destination_tree, child_id, id, children)
            return children
        return children

    def _add(self) -> None:
        selection: list[str] = list(self._question_tree.selection())
        if selection:
            children = []
            for item_id in selection:
                if not item_id in children:
                    children += self._copy_children(
                        source_tree = self._question_tree,
                        destination_tree = self._selected_tree,
                        item_id = item_id,
                        parent_id = "",
                        children = []
                    )



    def _remove(self) -> None:
        print("remove pressed")